from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random, base64, string, re

def center_login(request):
    return render(request, 'center/login.html')
