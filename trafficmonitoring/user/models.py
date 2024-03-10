from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img_profile = models.ImageField(upload_to = "uploads/", blank=True)
    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"