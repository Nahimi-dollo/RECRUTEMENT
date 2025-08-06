from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from .views import AjoutOffre
from .views import modifier_offre
from .views import supprimer_offre
from .views import AjoutCAndidature
from . views import modifier_candidature
from . views import supprimer_candidature

urlpatterns =[
   
    
    path('ajout1',AjoutOffre, name= 'AjoutOffre'),
    path('api/offres/<int:offre_id>/modifier/', modifier_offre, name='modifier_offre'),
    path('api/offres/<int:offre_id>/supprimer/', supprimer_offre, name='supprimer_offre'),

    path('ajout2', AjoutCAndidature, name= 'AjoutCAndidature'),
    path('modifier2', modifier_candidature, name= 'modifier_candidature'),
    path('suprimer2',supprimer_candidature, name= 'supprimer_candidature'),

    

]