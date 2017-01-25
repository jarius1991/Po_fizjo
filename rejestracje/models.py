from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from decimal import Decimal


# Create your models here.
class Konto(models.Model):
    loginy = models.CharField(max_length=25,unique=True)
    hasla = models.CharField(max_length=25)
    email = models.EmailField(max_length=255,unique=True)
    numerKonta=models.AutoField(primary_key=True)

    def __str__(self):
        return "Login: "+self.loginy


class Osoba(models.Model):
    imie=models.CharField(max_length=25)
    nazwisko=models.CharField(max_length=40)
    telefon=models.IntegerField(max_length=12, validators=[RegexValidator(regex=r'^[0-9]{9,12}$')], )
    miasto=models.CharField(max_length=40)
    ulica=models.CharField(max_length=40)
    numerBudynkuMieszkania=models.CharField(max_length=10)
    kontoNumerKonta=models.ForeignKey(Konto, primary_key=True)

    def __str__(self):
        return "Imie: "+self.imie + ", Nazwisko: "+self.nazwisko



class Pacjent(models.Model):#usunac osobaKontoLoginy=models. z visuala
    rabat=models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('00.00'))#glupi nullable - moze byc po prostu 0
    osobaKontoNumerKonta=models.ForeignKey(Osoba, primary_key=True)

    def __str__(self):
        return "Konto pacjenta: "+self.osobaKontoNumerKonta




class Fizjoterapeuta(models.Model):
    pensja=models.DecimalField(max_digits=7, decimal_places=2)
    osobaKontoNumerKonta=models.ForeignKey(Osoba, primary_key=True)

    def __str__(self):
        return "Konto fizjoterapeuty: "+self.osobaKontoNumerKonta


class Rejestracja(models.Model):
    nrRejestracji=models.AutoField(primary_key=True)
    pacjentOsobaKontoNumerKonta=models.ForeignKey(Pacjent)
    priorytet=models.BooleanField(default=False)
    preferowanyFizjoterapeuta=models.ForeignKey(Fizjoterapeuta, blank=True)

    def __str__(self):
        return "Nr: "+self.nrRejestracji+" Pacjent: "+self.pacjentOsobaKontoNumerKonta



class UslugiTyp(models.Model):
    typ=models.CharField(primary_key=True, max_length=40)
    cena=models.DecimalField(max_digits=5, decimal_places=2, blank=True)# czy aby na pewno?

    def __str__(self):
        return "Typ: "+self.typ


class Wizyta(models.Model):
    nrWizyty=models.AutoField(primary_key=True, max_length=20)
    platnosci=(('po','Pobranie'),('pr','Przelew'))
    rodzajPlatnosci=models.CharField(max_length=2,choices=platnosci ,default='po')
    cena=models.DecimalField(max_digits=5, decimal_places=2, blank=True) #default=decimal('0.00')
    data=models.DateField( blank=True)
    godzina=models.IntegerField(max_length=10,blank=True) # na pewno 10?
    uslugiTyp=models.ForeignKey(UslugiTyp)
    rejestracjaNrRejestracji=models.ForeignKey(Rejestracja)
    fizjoterapeuta=models.ForeignKey(Fizjoterapeuta ,blank=True)

    def __str__(self):
        return "Wizyta: "+self.nrWizyty



class MiejsceITermin(models.Model):
    miasto=models.CharField(max_length=40)
    ulica=models.CharField(max_length=40)
    numerBudynkuMieszkania=models.CharField(max_length=10)
    data=models.DateField()
    odGodziny=models.IntegerField(max_length=2)
    doGodziny=models.IntegerField(max_length=2)
    osoba2NerRejestracji=models.ForeignKey(Rejestracja, primary_key=True)

    def __str__(self):
        return "Miejsce spotkania: "+self.miasto



class GodzinyPrzyjec(models.Model):
    index=models.AutoField(primary_key=True)
    ficjoterapeutaOsobaKontoNumerKonta=models.ForeignKey(Fizjoterapeuta)
    miastoStartowe=models.CharField(max_length=40)
    miastoKoncowe=models.CharField(max_length=40)
    ulicaStartowa=models.CharField(max_length=40)
    ulicaKoncowa=models.CharField(max_length=40)
    nrBudynkuStartowy=models.IntegerField(max_length=10)
    nrBudynkuKoncowy=models.IntegerField(max_length=10)
    data=models.DateField()
    odGodziny=models.IntegerField(max_length=2)
    doGodziny=models.IntegerField(max_length=2)

    def __str__(self):
        return "Godziny przyjec: "+self.index+"  data: "+self.data+"  na godzine:"+self.odGodziny







