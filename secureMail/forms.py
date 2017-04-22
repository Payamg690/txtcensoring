from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
from .functions import generatePassword

class NachrichtForm(forms.Form):
    Betreff = forms.CharField(widget=forms.TextInput( attrs={'size':'60'}), label='Betreff', max_length=100)
    Nachricht = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor'))
    Email = forms.EmailField(widget=forms.TextInput( attrs={'size':'60'}), label='Email', max_length=254)
    
class PassForm(forms.Form):
    Passwort = forms.CharField(widget=forms.TextInput( attrs={'size':'60'}), label='Passwort', max_length=255)
    
class KeyForm(forms.Form):
  Passwort = forms.CharField(widget=forms.TextInput( attrs={'size':'60'}), label='Passwort', max_length=255)