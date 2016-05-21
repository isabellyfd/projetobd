# -*- coding: utf8 -*-
from django import forms
from django.core import mail
from django.core.mail import send_mail
# SIGNALS	
import datetime

class UploadFileForm(forms.Form):
	historico = forms.FileField()
	curriculum = forms.FileField()
	foto = forms.ImageField()