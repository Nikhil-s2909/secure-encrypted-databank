from django.db import models

# Create your models here.
from django.db import models

class Center(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class SecureFile(models.Model):
    owner = models.ForeignKey(Center, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    encrypted = models.BooleanField(default=False)
    secure_key = models.CharField(max_length=50, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
     # 🔐 OTP fields
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created = models.DateTimeField(null=True, blank=True)
    
