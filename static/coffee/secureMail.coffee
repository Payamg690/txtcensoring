#stolen from this website
#http://weeknumber.net/how-to/javascript
Date::getWeek ?= () ->
  date = new Date(@getTime())
  date.setHours(0, 0, 0, 0)
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7)
  week1 = new Date(date.getFullYear(), 0, 4)
  1 + Math.ceil ((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7
#end of stealing :)

Date::daysAgo ?= (days) ->
  newDate = new Date(@getTime())
  newDate.setDate(@getDate() + days)
  newDate

class WeekContext
  constructor: (weekID) ->
    @revs = []
    @weekID = weekID

  output: () ->
    @revenues.concat([@totals()])

  output: () ->
    delete r.weekLength for r in @revs
    length = @revs.length
    if length <= 1
      @revs
    else
      @revs[0]['weekLength'] = length
      @revs.concat([@totals()])

  totals: () ->
    {weekID: @weekID, date: @weekID, requests: @sumRequests(), qualified: @sumQual(),
    revenue: @sumRevs(), not_qualified: @sumNotQual(), lar: @sumLAR(),
    total: true}

  sumRequests: () ->
    sum((r.requests for r in @revs))

  sumQual: () ->
    sum((r.qualified for r in @revs))

  sumRevs: () ->
    sum((r.revenue for r in @revs))

  sumNotQual: () ->
    sum((r.not_qualified for r in @revs))

  sumLAR: () ->
    soldLeads = sum((r.lar[0] for r in @revs))
    potSells = sum((r.lar[1] for r in @revs))
    [soldLeads, potSells]

class Revenues
  constructor: (revs) ->
    @values = {}
    for item in revs
      dateString = item.date
      splitted = (parseInt(v) for v in dateString.split('-'))
      date = new Date(splitted[0], splitted[1] - 1, splitted[2])
      @values[dateString] = {
        'revenue': item.revenue
        'qualified': item.qualified
        'requests': item.requests
        'not_qualified': item.not_qualified
        'date': date
        'lar': item.lar
      }

  get: (filter) ->
    dates = Object.keys(@values).sort().reverse()
    outputList = []
    @totals = {}
    for dateKey in dates
      revForDay = @values[dateKey]
      weekID = prettyWeek(revForDay.date)
      context = context || new WeekContext(weekID)
      continue if filter and revForDay.date.getDay() not in filter
      if context.weekID != weekID
        outputList = outputList.concat(context.output())
        weekTotal = context.totals()
        @totals[weekTotal.weekID] = weekTotal
        context = new WeekContext(weekID)
      context.revs.push(revForDay)
    outputList.concat(context.output())

pad = ((number)-> if number < 10 then "0" + number else number.toString())
sum = ((array)-> array.reduce(((pv, cv)-> pv + cv ), 0))
currency = ((amount) -> if amount == Infinity then "N/A" else amount.toFixed(2) + "€")

prettyWeek = (date)->
  if date
    "#{date.getFullYear()}.#{pad date.getWeek()}"
  else
    ""

Handlebars.registerHelper 'prettyWeek', prettyWeek

Handlebars.registerHelper 'prettyDate', (date) ->
  weekDays = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag",
  "Freitag", "Sonnabend"]
  if date
    "#{weekDays[date.getDay()]}, #{pad date.getDate()}.#{pad date.getMonth() + 1}"
  else
    ""

Handlebars.registerHelper 'euro', currency

Handlebars.registerHelper 'revPerReq', () ->
  revPerDay = computeValue(@, 'revPerReq')
  if isNaN(revPerDay) then "N/A" else currency(revPerDay)

Handlebars.registerHelper 'cr2', () ->
  rate = computeValue(@, 'cr2')
  if isNaN(rate) then "N/A" else percentify rate

Handlebars.registerHelper 'lar', (lar) ->
  rate = (lar[0] / lar[1])
  if isNaN(rate) then "N/A" else percentify rate

weekArrows = [1, 4]
Handlebars.registerHelper 'arrows', (key) ->
  output = ''
  for w in weekArrows
    if @total
      [year, weekNumber] = @weekID.split('.').map((value) -> parseInt(value))
      weekNumber -= w
      if weekNumber <= 1
        year -= 1
        # wikipedia says:
        # > The number of weeks in a given year is equal to the corresponding
        # > week number of 28 December.
        # https://en.wikipedia.org/wiki/ISO_week_date#Weeks_per_year
        weekNumber = new Date(year, 12, 28).getWeek() + weekNumber
      other = revenues.totals["#{year}.#{weekNumber}"]
      if other
        oldValue = computeValue(other, key)
        output += renderArrow oldValue, computeValue(@, key), w
    else if @date
      otherDate = @date.daysAgo(-(w * 7))
      dateKey = "#{otherDate.getFullYear()}-#{pad (otherDate.getMonth() + 1)}-#{pad otherDate.getDate()}"
      other = revenues.values[dateKey]
      if other
        oldValue = computeValue(other, key)
        output += renderArrow oldValue, computeValue(@, key), w
  output

renderArrow = (oldValue, newValue, weeks) ->
  relativeDifference = compare(oldValue, newValue)
  title = "Vor #{weeks} Wochen: #{showOld(oldValue)}"
  direction = if relativeDifference <= -0.05
    'down'
  else if relativeDifference >= 0.05
    'up'
  else
    'right'
  '<i class="glyphicon glyphicon-arrow-' + direction + '" title="' + title +
  '"></i>'

computeValue = (row, key) ->
  switch key
    when "cr2" then row.qualified/(row.qualified + row.not_qualified)
    when "revPerReq" then row.revenue/row.qualified
    else row[key]


showOld = (v) ->
  if typeof v == "object"
    percentify(v[0]/v[1])
  else if v < 1
    percentify v
  else if v % 1 == 0
    v
  else
    v.toFixed(2)

compare = ((oldValue, newValue) ->
  if typeof oldValue == "object"
    ((oldValue[0] / oldValue[1]) / (newValue[0] / newValue[1])) - 1
  else
    (newValue/oldValue) - 1)

percentify = ((value) -> (value * 100).toFixed(1) + '%')

rowTemplate = null
revenues = new Revenues([])
rawRevenues = []
rowFilter = null

renderTable = (revs) ->
  if revs and typeof revs[0] == "object"
    rawRevenues = revs
    revenues = new Revenues(revs)
  tbody = $('#turnover-table tbody')
  tbody.empty()
  data = revenues.get(rowFilter)
  html = rowTemplate({rows: data})
  tbody.html(html)

$(document).ready (e) ->
  $('#tableControlsToggle').click () ->
    $("#tableControls").slideToggle()

  $('#tableControls form').submit (e) ->
    e.preventDefault
    weekArrows = (parseInt(w) for w in $("#weeks").val().split(","))
    rowFilter = (d for d in $('#tableControls .checkbox input:checked').map(-> parseInt($(@).val())))
    rowFilter = if rowFilter.length not in [0,7] then rowFilter else null
    renderTable()
    false

  $.get '/static/templates/row.html', (template) ->
    rowTemplate = Handlebars.compile template
    bi.registerRenderer(renderTable)
