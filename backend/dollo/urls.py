from django.urls import path
from .views import test
from .views import bonjour
from .views import ajouter_offre
from .views import candidater
from . import views

urlpatterns =[
    path('hello',test,name='hello'),
    path('test2',bonjour,name='bonjour'),
    path('offres/', views.liste_offres, name='liste_offres'),
    path('offres/<int:pk>/', views.detail_offre, name='detail_offre'),
    path('offres/<int:pk>/modifier/', views.modifier_offre, name='modifier_offre'),
    path('offres/<int:pk>/supprimer/', views.supprimer_offre, name='supprimer_offre'),
    path('admin/ajouter/offre',ajouter_offre,name='ajouter_offre'),
    path('user/candidater',candidater,name='candidater')
]