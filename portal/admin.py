from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

class Profileadmin(admin.ModelAdmin):
    list_display = ["RegNo" , "display_pic" ,"user"]


class LogUsageadmin(admin.ModelAdmin):
    list_display = ["profile","ip_address_used","device_used","website_visited","date"]

admin.site.register(UserProfile,Profileadmin)
admin.site.register(Log_Usage ,LogUsageadmin)
