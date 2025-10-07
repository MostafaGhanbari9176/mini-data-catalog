from django.db import models

class OTP(models.Model):
    email = models.EmailField(primary_key=True)
    otp = models.CharField(max_length=6)
    invalidate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
