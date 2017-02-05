#-*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import *
#dodawanie elementwo do edycji w Adminie
admin.site.register(Konto)
admin.site.register(Osoba)
admin.site.register(Fizjoterapeuta)
admin.site.register(Pacjent)
admin.site.register(Rejestracja)
admin.site.register(UslugiTyp)
admin.site.register(Wizyta)
admin.site.register(MiejsceITermin)
admin.site.register(GodzinyPrzyjec)