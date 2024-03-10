from django.contrib import admin
from .models import Account
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "img_profile", "role")

admin.site.register(Account, AccountAdmin)
