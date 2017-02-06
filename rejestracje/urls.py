from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main$',views.main_page, name='main_page'),
    url(r'rozpocznijPrzegladanie',views.rozpocznijPrzegladanie,name="rozpocznijPrzegladanie"),
    url(r'^przegladanie$',views.przegladanie, name='przegladanie'),
    url(r'^rejestracja$',views.rejestracja, name='rejestracja'),
    url(r'^szczegoly$',views.szczegoly, name='szczegoly'),
    url(r'^zatwierdzenie$', views.zatwierdzenie, name="zatwierdzenie"),
    url(r'^aktywne$', views.aktywne, name="aktywne"),
    url(r'^anulowanie/(?P<pk>[0-9]+)/$',views.anulowanie, name="anulowanie"),
    url(r"^anulowanie/(?P<pk>[0-9]+)/anulowanieWizyty$", views.anulowanieWizyty, name="anulowanieWizyty"),
    url(r"^anulowanieWizyty$", views.anulowanieWizyty, name="anulowanieWizyty")
    #url(r'^przegladanie/(?P<value>)/$',views.przegladanieData1, name='przegladanieData1')
    #url(r'^przegladanie/(?P<pk>[0-9]{2}-[0-9]{2}-[0-9]{4})/$',views.przegladanieData, name='przegladanieData')

]