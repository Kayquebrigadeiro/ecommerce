from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.TextField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True)
    email_verification_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username