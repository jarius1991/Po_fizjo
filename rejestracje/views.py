#-*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
# Create your views here.
from django.utils import timezone
import datetime
from django.core import serializers
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
import re
import pickle
from django.contrib import messages

def main_page(request):
    return render(request, 'rejestracje/main.html', {})  #tutaj renderujemy okreslony html z naszymi danymi

def rozpocznijPrzegladanie(request):
    file=open("imie_nazwisko", 'wb')
    pickle.dump([],file)
    file.close()
    print("utworzylismy nowy pickle!")
    return render(request, 'rejestracje/oferta.html',{})

def przegladanie(request):
    pobrana_data=''
    dict={}
    komunikat=''

    try:
        pobrana_data=request.GET['data']
        dict['data']=pobrana_data
    except Exception:
        pass


    if(pobrana_data):
        pobrana_data=[int(i) for i in pobrana_data.split('-')]
        a=datetime.datetime(pobrana_data[0],pobrana_data[1],pobrana_data[2],0,0,0,1)
        b=timezone.make_naive(timezone.now())
        if(a<b):
            komunikat="Wybrana data musi byc po dzisiejszym dniu."
        else:
            godziny_baza=GodzinyPrzyjec.objects.filter(data__year=pobrana_data[0]).filter( data__month=pobrana_data[1]).filter( data__day=pobrana_data[2])
            potencjalni_fizjoterapeuci=["",]
            for i in godziny_baza:
                if not i.ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta in potencjalni_fizjoterapeuci:
                    potencjalni_fizjoterapeuci.append(i.ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta)
            dict["fizjoterapeuci"]=potencjalni_fizjoterapeuci
            godziny=generowanieGodzin(godziny_baza)
            dict["godziny"]=godziny
    dict['komunikat']=komunikat
    return render(request, 'rejestracje/oferta.html',dict)





def rejestracja(request):
    dict={}
    s=request.POST.get("wybor","")
    dzien=request.POST.get("data","")

    if(s=="anuluj"):
        resetujPrzypisaniaWizyt()
        return render(request,"rejestracje/oferta.html",{"message":u"Przerwano rejestrację."})
       # return render(request, 'rejestracje/main.html')

    dict['data']=dzien
    pobrana_data=[int(i) for i in dzien.split('-')]
    godziny_baza=GodzinyPrzyjec.objects.filter(data__year=pobrana_data[0]).filter( data__month=pobrana_data[1]).filter( data__day=pobrana_data[2])
    potencjalni_fizjoterapeuci=["",]

    for i in godziny_baza:
        if not i.ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta in potencjalni_fizjoterapeuci:
            potencjalni_fizjoterapeuci.append(i.ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta)
    dict["fizjoterapeuci"]=potencjalni_fizjoterapeuci
    print("potencjalnifizjo", potencjalni_fizjoterapeuci)
    godziny=generowanieGodzin(godziny_baza)
    dict["godziny"]=godziny




    lista_g=[]
    for key in request.POST:
            if(key.split(',')[0]=='godz'):
                lista_g.append(int(key.split(',')[1]))#print ("godzinki")

    preferowany=request.POST.get("preferowany_fizjoterapeuta","")
    miasto=request.POST.get("miasto","")
    ulica=request.POST.get("ulica","")
    dom=request.POST.get("dom","")
                                                    #################walidacja parametrow???????????????????????? czy som dobre
    dict["dom"]=dom
    dict['miasto']=miasto
    dict['ulica']=ulica
    dict['preferowany']=preferowany
    print ("preferowany",preferowany)
    #sprawdzenie czy wybrano godziny
    if not lista_g:
        #lista pusta
        print("lista godzin pusta!")
        dict['brakGodzin']=True
        #przkaż wybrane parametry aby byly konownie domyślnie zainicjowane jeżeli ich nie ma to
        return render(request, 'rejestracje/oferta.html', dict  )

    #sprawdzenie czy miasto ulica i dom są dobre
    adresNiepoprawny=""

    miastoWzorzec=re.compile(u"^[A-ZŁŻÓĘN]{1}[a-złżóęńśźć]+([ ][A-ZŁŻÓĘN]{1}[a-złżóęńśźć]+){0,1}$")
    czyMiastoPasuje=bool(miastoWzorzec.match(miasto))

    ulicaWzorzec=re.compile(u"^[A-ZŁŻÓĘN]{1}[a-złżóęńśźć]+([ |-][A-ZŁŻÓĘN]{1}[a-złżóęńśźć]+){0,1}$")
    czyUlicaPasuje=bool(ulicaWzorzec.match(ulica))

    domWzorzec=re.compile(u"^[0-9]+[a-z]{0,1}$")
    czyDomPasuje=bool(domWzorzec.match(dom))

    if not czyMiastoPasuje:
        dict["miasto"]=''
        dict['adresNiepoprawny']="No niepoprawny kurcze"

    if not czyUlicaPasuje  :
        dict["ulica"]=''
        dict['adresNiepoprawny']="No niepoprawny kurcze"

    if not czyDomPasuje  :
        dict["dom"]=''
        dict['adresNiepoprawny']="No niepoprawny kurcze"

    dict['wybraneGodziny']= lista_g
    if not czyMiastoPasuje or  not czyUlicaPasuje or not czyDomPasuje :
        #dict['wybraneGodziny']= lista_g
        return render(request, 'rejestracje/oferta.html', dict )




    #sprawdzenie czy fisjoterapeuta jest dostępny w tych godzinach
    czyJest=jestWtedyFizjoterapeuta(preferowany,pobrana_data,lista_g)
    print('czyjest',czyJest)
    if not czyJest :
        dict['nieMaTegoFizjoterapeuty']="Nie ma go"
        dict['poprzedniWybor']=s
        if request.POST.get("bezFizjoterapeutyWybor","")=='nie':
            dict['preferowany']=''
            dict['nieMaTegoFizjoterapeuty']=''
            dict['poprzedniWybor']=''
            return render(request, 'rejestracje/oferta.html', dict )
        elif request.POST.get("bezFizjoterapeutyWybor","")=='':
            return render(request, 'rejestracje/oferta.html', dict )



    wizyta=WizytaWpis(dzien,lista_g,preferowany, miasto,ulica,dom)
   # print("wizyta po utworzeniu"); print(wizyta.__str__())

    file=open("imie_nazwisko",'rb')
    wizyty=pickle.load(file)
    file.close()

    wizyty.append(wizyta)
    #sprawdzenie co jest w wizytach
    #for i in wizyty:
    #    print(i.__unicode__())

    file=open("imie_nazwisko","wb")
    pickle.dump(wizyty, file)
    file.close()


    #print (s)
    if(s=="kolejny"):
        return render(request, 'rejestracje/oferta.html',{})

    else:
        #return render(request, 'rejestracje/szczegolyRejestracji.html',{})
        #print('zaraz wyrzucimy do szczegolow')
        uslugi=UslugiTyp.objects.all()
        dict2={"uslugi":uslugi}
        cena=oblicz_cene("")
        dict2['cena']=cena
        return render(request,'rejestracje/szczegolyRejestracji.html',dict2)
       # szczegoly(request)

def oblicz_cene(priorytet):
    doPobraniaCeny=UslugiTyp.objects.get(typ=u"Masaż")
    cena=doPobraniaCeny.cena
    if priorytet:
        cena=cena+20
    osoba=Osoba.objects.get(imie="imie",nazwisko="nazwisko")
    rabat=Pacjent.objects.get(osobaKontoNumerKonta=osoba).rabat
    cena=round(cena*((100-rabat)/100),2)
    return cena

def szczegoly(request):
    wybor=request.POST.get("wybor","")

        #nowa strona z cena rodzajem usugi, czy priorytet i tam pobieramy wizyty obrabiamy
        #i dodajemy do bazy
    dict={}
    uslugi=UslugiTyp.objects.all()
    dict["uslugi"]=uslugi
    print("odsiwezenie po kliknieciu selecta")
    wybranaUsluga=request.POST.get("wybranaUsluga","")
    print(wybranaUsluga)
    dict["wybranaUsluga"]=wybranaUsluga

    priorytet=request.POST.get("priorytet","")
    print("priorytet",priorytet)
    dict['priorytet']=priorytet

    #jeżeli wiecej niż 10 wizyt to zmizka
    #+20zl jezeli priorytet
    #cena z wybranego pola
    doPobraniaCeny=UslugiTyp.objects.get(typ=wybranaUsluga)
    print ('doPograniaCeny',doPobraniaCeny.cena)
    cena=0
    cena=doPobraniaCeny.cena
    if priorytet:
        cena=cena+20
    osoba=Osoba.objects.get(imie="imie",nazwisko="nazwisko")
    rabat=Pacjent.objects.get(osobaKontoNumerKonta=osoba).rabat
    cena=round(cena*((100-rabat)/100),2)
    dict['cena']=cena

    if wybor=="anuluj":
        resetujPrzypisaniaWizyt()
        return render(request,"rejestracje/oferta.html",{"message":u"Przerwano rejestrację."})
        #return render(request, 'rejestracje/main.html')
    elif wybor=="zatwierdz":

        file=open("imie_nazwisko",'rb')
        wizyty=pickle.load(file)
        file.close()
        for wizyta in wizyty:
           # for godzina in wizyta.godziny:
                wizyta.godziny.sort()

        #alternatywna mozliwosc utowrzenia wizyt na kazda godzine
        wizyty=utworzGodzinySet(wizyty)

        dict['wizyty']=wizyty

        return render(request, "rejestracje/zatwierdzenie.html",dict)
    #jeszcze trzeba dodac elementy tabeli
    return render(request,'rejestracje/szczegolyRejestracji.html',dict)

def utworzGodzinySet(wizyty):
    tabela=[]
    for wizyta in wizyty:
        for godzina in wizyta.godziny:
            temp=WizytaWpis(wizyta.dzien,godzina,wizyta.fizjoterapeuta,wizyta.miasto,wizyta.ulica,wizyta.dom)#(self, dzien, godziny,fizjoterapeuta,miasto,ulica, dom):
            dodac=True
            for elem in tabela:
                if temp.dzien==elem.dzien and temp.godziny==elem.godziny:
                    dodac=False
                    break

            if dodac :
                tabela.append(temp)

    return tabela

def resetujPrzypisaniaWizyt():
    file=open("imie_nazwisko", 'wb')
    pickle.dump([],file)
    file.close()

def zatwierdzenie(request):
    sterowanie=request.POST.get("wybor")
    if sterowanie=="anuluj":
        pass
        #return render(request,"rejestracje/main.html")
    else:
        file=open("imie_nazwisko",'rb')
        wizyty=pickle.load(file)
        file.close()
        wizyty=utworzGodzinySet(wizyty)

        #dodaj wszystkie wizyty tak jak bozia przykazala
        #tu trzeba dodac elementy do bazy danych
        konto=Osoba.objects.get(imie="imie", nazwisko="nazwisko")
        pacjent=Pacjent.objects.get(osobaKontoNumerKonta=konto)
        priorytet=True
        if request.POST.get("priorytet",""):
            priorytet=True
        else:
            priorytet=False
        #priorytet=request.POST.get("priorytet","")
        rejestracja=Rejestracja(pacjentOsobaKontoNumerKonta=pacjent,priorytet=priorytet )
        #do rejestracji tworzymy wiele miejsc i terminów
        rejestracja.save()


        for wizyta in wizyty:
              #pobieranie fizjoterapeuty
            print("wizyta: ",wizyta)
            if wizyta.fizjoterapeuta:
                fizjoOsoba=Osoba.objects.get(imie=wizyta.fizjoterapeuta.split()[0],nazwisko=wizyta.fizjoterapeuta.split()[1])
                fizjoFizko=Fizjoterapeuta.objects.get(osobaKontoNumerKonta=fizjoOsoba)
            else:
                fizjoFizko=None
            mit=MiejsceITermin(     miasto=wizyta.miasto,
                                    ulica=wizyta.ulica,
                                    numerBudynkuMieszkania=wizyta.dom,
                                    data=wizyta.dzien,
                                    odGodziny=wizyta.godziny,
                                    doGodziny=wizyta.godziny+1,
                                    osoba2NerRejestracji=rejestracja,
                                    preferowanyFizjoterapeuta=fizjoFizko)
            mit.save()

    resetujPrzypisaniaWizyt()
    return render(request,"rejestracje/oferta.html",{"message":u"Dodano poprawnie rejestrację"})



def aktywne(request):
    dict={}
    wizyty=generowanieAktywnychWizyt()
    dict["wizyty"]=wizyty
    print(wizyty)
    return render(request, "rejestracje/historia.html",dict)

def generowanieAktywnychWizyt():
    osoba=Osoba.objects.get(imie="imie",nazwisko='nazwisko')
    pacjent=Pacjent.objects.get(osobaKontoNumerKonta=osoba)
    rejestracje=Rejestracja.objects.filter(pacjentOsobaKontoNumerKonta=pacjent)
    #jezeli rejestracja ma wizyte to trzeba z wizyty to zrobic
    wizyty=[]
    for rejestracja in rejestracje:
        #jezeli rejestracja jest w wizytach

        terminPierwszy=MiejsceITermin.objects.filter(osoba2NerRejestracji=rejestracja).filter(data__gt=timezone.now()).order_by('date').order_by('odGodziny').first()
        wizyty.append(terminPierwszy)
    return wizyty


def anulowanie(request,pk):
    print (pk)
    wizyty=MiejsceITermin.objects.filter(osoba2NerRejestracji=pk)
    print("wizyty: ",wizyty)
    dict={"wizyty":wizyty  }
    dict["pk"]=pk

    return render(request, "rejestracje/anulowanie.html",dict)



def anulowanieWizyty(request):
    wybor=request.POST.get("wybor","")
   # print("wybor",wybor)
    pk=request.POST.get("pk","")
   # print("pk",pk)

    if wybor=="Edytuj" :
        pass
    elif wybor=="Usun pojedyncze godziny" :
        pass
    elif wybor==u"Usun całą rejestrację" :
       # print("weszło w usuwanie rejestracji")
        rejestracja=Rejestracja.objects.get(nrRejestracji=pk)

        rejestracja.delete()
        wizyty=generowanieAktywnychWizyt()
        dict2={}
        dict2["wizyty"]=wizyty
        dict2["message"]="Usunięto rejestrację"
        messages.info(request, u"Usunięto rejestrację")
        return render(request, "rejestracje/historia.html",dict2)

    elif wybor=="Cofnij":
        print ("wesło")
        wyj=aktywne(request)
        return wyj

    return render(request, "rejestracje/main.html")



def jestWtedyFizjoterapeuta(fizjoterapeuta,pobrana_data, wybraneGodziny):

    if not fizjoterapeuta:
       return True
    bazaFizjoterapeuta=Osoba.objects.get(imie=fizjoterapeuta.split()[0],nazwisko=fizjoterapeuta.split()[1])
   # print("baza fizjoterapeuta",bazaFizjoterapeuta)
    szukanyFizjoterapeuta=Fizjoterapeuta.objects.get(osobaKontoNumerKonta=bazaFizjoterapeuta)
    godziny_baza=GodzinyPrzyjec.objects.filter(data__year=pobrana_data[0]).filter( data__month=pobrana_data[1]).filter( data__day=pobrana_data[2]).filter(ficjoterapeutaOsobaKontoNumerKonta=szukanyFizjoterapeuta)
   # print (godziny_baza)
    wygenerowaneGodziny=generowanieGodzin(godziny_baza)
   # print("wygenerowaneGodziny",wygenerowaneGodziny)
   # print("wybraneGodziny",wybraneGodziny)
    for key,value in wygenerowaneGodziny:
       # print(key)
        if key in wybraneGodziny:
            return True
    return False


def pobierz_godziny(request):
    request.POST.get("",)

def generowanieGodzin(godziny):
        list={}
        for i in godziny:

            for j in range(i.odGodziny,i.doGodziny):
                list[j]= str(j)+":00 - " +str(j+1)+":00 "
        return sorted(list.items())
















def przegladanieData1(request,value):
    print (value)
    hours=GodzinyPrzyjec.objects.filter(data__gte=timezone.now())
    list=[]


    for j in range(hours[0].odGodziny,hours[0].doGodziny):
        list.append( (str(j)+":00 - " +str(j+1)+":00    do "+ hours[0].ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta.imie + " " + hours[0].ficjoterapeutaOsobaKontoNumerKonta.osobaKontoNumerKonta.nazwisko ))

    return render(request, 'rejestracje/oferta.html', {"hours":hours, "list":list})




class WizytaWpis():
    def __init__(self, dzien, godziny,fizjoterapeuta,miasto,ulica, dom):
        self.dzien=dzien
        self.godziny=godziny
        self.fizjoterapeuta=fizjoterapeuta
        self.miasto=miasto
        self.ulica=ulica
        self.dom=dom

    def __unicode__(self):
        return u'%s %s %s %s %s %s '%(self.dzien, self.godziny, self.fizjoterapeuta, self.miasto, self.ulica, self.dom)

class MyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Wizyta):
            return force_text(obj)
        return super(MyEncoder, self).default(obj)

