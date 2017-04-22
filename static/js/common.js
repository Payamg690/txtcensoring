'use strict';
var bi = bi || {};

bi.products = bi.products || {};
bi.products.top = new Set([558]);

bi.selections = {};
bi.selections.channels = {
  "directChannel": 'direct',
  "coopChannel": 'coop',
  "dis_directChannel": 'Dis_Direct',
  "dis_gdnChannel": "dis_gdn",
  "dis_pnChannel": "dis_pn",
  "dis_retargetingChannel": "dis_retargeting",
  "sea_non_brandChannel": 'sea_non_brand',
  "sea_brandChannel": 'sea_brand',
  "dis_socialChannel": 'dis_social',
  "seoChannel": 'seo',
  "emailChannel": 'email',
  "refererChannel": "referer"
};

bi.filter = {"products": new Set([]), "channels": new Set()};

bi.reload = function(){
  var data = {};
  if(bi.filter.products.size){
    data.products = Array.from(bi.filter.products).join(',');
  }
  if(bi.filter.channels.size){
    data.channels = Array.from(bi.filter.channels).join(',');
  }
  $.get({"url": '/api/all', "success": bi.render, "data": data})
    .fail(function(){alert("Data could not be fetched from server :(");});
};

bi.renderer = [];

bi.data = undefined;

bi.render = function(data){
  bi.data = data;
  for(var i in bi.renderer){
    bi.renderer[i](data);
  }
};

bi.registerRenderer = function(func){
  bi.renderer.push(func);
  if(bi.data){
    func(bi.data);
  }
};

bi.taggify = function(str){
  str = str.toLowerCase().replace(/(\s+)|(&)/g, '');
  return str.replace(/ü/g, 'u').replace(/ö/, 'o').replace(/ä/g, 'a').replace(/ß/g, 's');
};

var renderAvailableProducts = function(){
  var searchTag = bi.taggify($("#productSearch").val());
  var matchSearch = function(itemTag){return searchTag.length < 3 || itemTag.match(searchTag)};
  $('#availableProducts ul li').each(function(){
    var $this = $(this);
    var itemTag = $this.attr('data-search-tag');
    var $button = $($this.find('button'));
    if(!bi.filter.products.has(parseInt($button.val())) && matchSearch(itemTag)){
      $this.show();
    } else {
      $this.hide();
    }
  });
};

var renderSelectedProducts = function(){
  $('#selectedProducts ul li').each(function(){
    var $this = $(this);
    var $button = $($this.find('button'));
    if(bi.filter.products.has(parseInt($button.val()))){
      $this.show();
    } else {
      $this.hide();
    }
  });
};

(function(){
  $(document).ready(function(){
    bi.reload();
    $('#availableProducts button').click(function(){
      var id = parseInt($(this).val());
      bi.filter.products.add(id);
      $('#productFilter').trigger("updated");
    });
    $('#selectedProducts button').click(function(){
      var id = parseInt($(this).val());
      bi.filter.products.delete(id);
      $('#productFilter').trigger("updated");
    })
    renderSelectedProducts();

    $("#productFilter").on("updated", renderSelectedProducts);

    $('#productFilter').on("updated", renderAvailableProducts);

    $('#productSearch').keyup(renderAvailableProducts);

    $('#topProducts').change(function(){
      if($(this).is(':checked')){
        bi.filter.products = bi.products.top;
      } else {
        bi.filter.products = new Set([]);
      }
      $("#productFilter").trigger("updated");
    });

    for(var buttonID in bi.selections.channels){
      var channel = bi.selections.channels[buttonID];
      $('#' + buttonID).change((function(c){
        return function(){
          if($(this).is(":checked")){
            bi.filter.channels.add(c);
          } else {
            bi.filter.channels.delete(c);
          }
        };
      })(channel));
    }
    $('#filterButton').click(function(){
      $('#filterDialog').modal('hide');
      bi.reload();
    });
  });
})();
$(document).ready(function(){
    $('#censor').click(function(){
       var text = $("foo").val(); 
    });
   });

$(document).ready(function () {
            $('[data-toggle="tooltip"]').tooltip();     
       });
            