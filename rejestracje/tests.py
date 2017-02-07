#-*- coding: utf-8 -*-
import datetime
import unittest
from django.test import TestCase
from .views import generowanieGodzin,utworzGodzinySet,WizytaWpis,poprawny_Adres

#generowanieGodzin,utworzGodzinySet,WizytaWpis=views.generowanieGodzin,views.utworzGodzinySet,views.WizytaWpis

class Tests(unittest.TestCase):


    def testGenerowanieGodzinIstnieje(self):
        #self.assertIsNot()
        assert generowanieGodzin != None, "Nie ma funkcji generowanieGodzin"



    def testUtworzGodzinySetJest(self):
        assert utworzGodzinySet !=None, "Nie ma funkcji utworzGodzinySet"


    def testUtworzGodzinySetJedenElement(self):
        wizyta1=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[12],None,None,None,None)#ten sam dzien
        assert utworzGodzinySet([wizyta1])[0].godziny==12 , "Niewygenerowała jednej godziny z listy jednoelementowej"

    def testUtworzGogdzinySetJedenElement(self):
        wizyta1=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[12],None,None,None,None)#ten sam dzien
        wizyta2=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[12],None,None,None,None)
        assert utworzGodzinySet([wizyta1,wizyta2])[0].godziny==12 , "Nie wygenerowała jednej godziny z dwoch list o takich samych dniach i godzinach"

    def testUtworzGodzinySetZbioryCzesciowoWspolne(self):
        wizyta1=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[11,12],None,None,None,None)#ten sam dzien
        wizyta2=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[12,13],None,None,None,None)
        print(utworzGodzinySet([wizyta1,wizyta2])[0])
        assert utworzGodzinySet([wizyta1,wizyta2])[0].godziny==11 and utworzGodzinySet([wizyta1,wizyta2])[1].godziny==12 and utworzGodzinySet([wizyta1,wizyta2])[2].godziny==13 , "Nie obsłużyła list godzin posiadających część wspólną"

    def testUtworzGodzinySetZbioryRozlaczne(self):
        wizyta1=WizytaWpis(datetime.datetime(2012,12,2,0,0,0,1),[13,14],None,None,None,None)#ten sam dzien inna godzina
        wizyta2=WizytaWpis(datetime.datetime(2012,12,1,0,0,0,1),[12],None,None,None,None)#inny dzien ta sama godzina
        wizyta3=WizytaWpis(datetime.datetime(2012,12,5,0,0,0,1),[15],None,None,None,None)#trzecia
        assert utworzGodzinySet([wizyta1,wizyta2,wizyta3])[0].godziny==13 and utworzGodzinySet([wizyta1,wizyta2,wizyta3])[1].godziny==14 and utworzGodzinySet([wizyta1,wizyta2,wizyta3])[2].godziny==12 and utworzGodzinySet([wizyta1,wizyta2,wizyta3])[3].godziny==15, "Nie dodało poprawnie godzin z nienachodzących na siebie list godzin"

    def testPoprawnyAdresPusty(self):
        assert poprawny_Adres("","","") ==[False,False,False], "Funkcja przyjęła puste pola"


    def testPoprawnyAdresDwuczlonowaUlicaPoprawna(self):
        assert poprawny_Adres("","Fleszarowej-Muskat","")==[False,True,False],"Funkcja nie wykryła poprawnie dwuczłonowej ulicy"

    def testPoprawnyAdresNazwyBezCyfr(self):
        assert poprawny_Adres("Mia6o",'U1ic4','')==[False,False,False],"Nie można stosować cyfr w nazwach ulic lub miast"

    def testPoprawnyAdres(self):
        assert poprawny_Adres("","","6a")==[False,False,True], "Nie poprawnie zidentyfikowano adres cyfra litera"

