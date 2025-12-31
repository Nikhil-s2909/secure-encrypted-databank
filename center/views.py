from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random, base64, string, re
from .encrypt import encrypt_file
from django.http import HttpResponse


from django.http import FileResponse
from Crypto.Cipher import Blowfish


def center_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            center = Center.objects.get(email=email, password=password)

            # ✅ THIS LINE IS REQUIRED
            request.session['center_id'] = center.id

            print("LOGIN SESSION SET:", request.session['center_id'])  # debug
            return redirect('/center_user/')
        except Center.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('/center_login/')

    return render(request, 'center/login.html')



def center_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Center.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/center_register/')

        Center.objects.create(
            name=name,
            email=email,
            password=password
        )
        messages.success(request, "Registration successful")
        return redirect('/center_login/')

    return render(request, 'center/register.html')


def center_user(request):
    print("SESSION DATA:", dict(request.session))  # debug

    if 'center_id' not in request.session:
        return redirect('/center_login/')

    return render(request, 'center/center_user.html')

def center_logout(request):
    request.session.flush()
    return redirect('/center_login/')


def upload_file(request):
    if 'center_id' not in request.session:
        return redirect('/center_login/')

    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        center = Center.objects.get(id=request.session['center_id'])
        sf = SecureFile.objects.create(
            owner=center,
            file=uploaded_file,
            secure_key=key
        )

        encrypt_file(sf.file.path, key)
        sf.encrypted = True
        sf.save()

        messages.success(request, "File uploaded & encrypted successfully")
        return redirect('/center_user/')

    return render(request, 'center/upload.html')

def my_files(request):
    if 'center_id' not in request.session:
        return redirect('/center_login/')

    center = Center.objects.get(id=request.session['center_id'])
    files = SecureFile.objects.filter(owner=center)

    return render(request, 'center/my_files.html', {'files': files})




def decrypt_and_download(request, file_id):
    if 'center_id' not in request.session:
        return redirect('/center_login/')

    sf = SecureFile.objects.get(id=file_id)

    key = sf.secure_key.encode()
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)

    # Read encrypted file
    with open(sf.file.path, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt + remove padding
    decrypted_data = cipher.decrypt(encrypted_data).rstrip(b"\0")

    # Create proper download response
    response = HttpResponse(
        decrypted_data,
        content_type='application/octet-stream'
    )

    filename = sf.file.name.split('/')[-1]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
