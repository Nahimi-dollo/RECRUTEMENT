from django.urls import path
from .views import test
from .views import bonjour

urlpatterns =[
    path('hello',test,name='hello'),
    path('test2',bonjour,name='bonjour')
]