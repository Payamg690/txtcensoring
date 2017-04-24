# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .forms import NachrichtForm, KeyForm, PassForm
from .models import Message
from .functions import censorTextFinal, generatePassword, saveMessage, retrieveMessage
from bs4 import BeautifulSoup as bs
from django.core.mail import send_mail
from django.template import loader

def index(request):
    return HttpResponse("Hello, world. You're at the secureMail index.")

def alice1(request):
    return render(request, 'alice1.html')


def alice2(request):
    form = NachrichtForm()
    pssform = PassForm()
    p = ""
    txt = ""
    ps = generatePassword()
    if request.POST:
        if '_censor' in request.POST:
            p = NachrichtForm(request.POST)
            source = str(p)
            sr1 = bs(source, "lxml").textarea.string
            print sr1
            sr2 = censorTextFinal(sr1)
            #txt = bs(sr2, "lxml").p.string

            Email = ""
            Betreff = p.cleaned_data['Betreff']
            #saveMessage(sr1, ps, Betreff, Email)
            return render(request, 'alice2.html', {'btn': "<input type='submit' style='float: right'  class='btn btn-primary' value='Verschlüsseln' name='_encrypt' />", 'form': p, 'pssform': ps, 'didi': sr2, 'link': "<a href='http://127.0.0.1:8000/secureMail/bob1'>Plaintext</a>"})
        elif '_encrypt' in request.POST:
            p = NachrichtForm(request.POST)
            if p.is_valid():
                Email = p.cleaned_data['Email']
                Betreff = p.cleaned_data['Betreff']
            source = str(p)
            sr1 = bs(source, "lxml").textarea.string
            saveMessage(sr1, ps, Betreff, Email)
            email_list = [Email]
            # making the html msg to send via mail
            html_message = 'this is your password: ' + ps + sr1 + " <a href='http://127.0.0.1:8000/secureMail/bob1'>decrypt your text under the following link<a>"
            # sending the email
            #send_mail('Text Encryption - ' + Betreff, 'this is the password', 'test@test.de', email_list,
            #         fail_silently=False, html_message=html_message)
            query = ""
            query = Message.objects.get(pwd=ps)
            cyTXT = query.__getattribute__('cyphertext')
            print cyTXT
            return render(request, 'alice3.html',
                          {'cyTXT': cyTXT,'form': form, 'pssform': ps, 'didi': "Der Prozess ist erfolgreich abgeschlossen.", 'link': "<a href='http://127.0.0.1:8000/secureMail/bob1'>the link to bob 1</a>"})

    return render(request, 'alice2.html', {'form': form, 'didi': txt})



def bob1(request):
    kform = KeyForm(request.POST or None)
    if kform.is_valid():
        ps = kform.cleaned_data['Passwort']
        query= ""
        try:
            query = Message.objects.get(pwd=ps)
            txt = query.__getattribute__('msg_hash')
            btrf = query.__getattribute__('btrf')
            return render(request, 'bob2.html',{'msg': str(retrieveMessage(txt, ps)).replace("<s>", "").replace("</s>", ""), 'btrf': btrf})
        except Message.DoesNotExist:
            return render(request, 'bob1.html', {'kform': kform, 'error': "there is no record!!"})
    return render(request, 'bob1.html', {'kform': kform})


def bob2(request):
    return render(request, 'bob2.html')



# class Post():
#     def __init__(self):
#         self.form = NachrichtForm()
#         self.txt = ""
#     def req_zensieren(self, request):
#         pssform = PassForm()
#         p = ""
#         self.ps = generatePassword()
#         if request.POST:
#             if '_censor' in request.POST:
#                 p = NachrichtForm(request.POST)
#                 source = str(p)
#                 sr1 = bs(source, "lxml").textarea.string
#                 sr2 = censorTextFinal(sr1)
#                 txt = bs(sr2, "lxml").p.string
#                 return render(request, 'alice2.html', {'form': p, 'pssform': self.ps, 'didi': self.txt})
#
#     def req_verschluesseln(self, request):
#         if '_encrypt' in request.POST:
#             p = NachrichtForm(request.POST)
#             if p.is_valid():
#                 Email = p.cleaned_data['Email']
#                 Betreff = p.cleaned_data['Betreff']
#             source = str(p)
#             sr1 = bs(source, "lxml").textarea.string
#             saveMessage(sr1, self.ps, Betreff, Email)
#             email_list = [Email]
#             # making the html msg to send via mail
#             html_message = 'this is your password: ' + self.ps + sr1 + " <a href='http://127.0.0.1:8000/secureMail/bob1'>decrypt your text under the following link<a>"
#             # sending the email
#             send_mail('Text Encryption - ' + Betreff, 'this is the password', 'test@test.de', email_list, fail_silently=False, html_message=html_message)
#
#             return render(request, 'alice3.html',{'form': self.form, 'pssform': self.ps, 'didi': "Der Prozess ist erfolgreich abgeschlossen."})