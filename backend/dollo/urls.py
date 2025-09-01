from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ==================== OFFRES ====================
    path('api/offres/', views.liste_offres, name='liste_offres'),
    path('api/offres/ajout/', views.ajout_offre, name='ajout_offre'),
    path('api/offres/<int:offre_id>/modifier/', views.modifier_offre, name='modifier_offre'),
    path('api/offres/<int:offre_id>/supprimer/', views.supprimer_offre, name='supprimer_offre'),

    # ==================== CANDIDATURES ====================
    path('api/candidatures/', views.liste_candidatures, name='liste_candidatures'),
    path('api/candidatures/ajout/', views.ajout_candidature, name='ajout_candidature'),
    path('api/candidatures/<int:candidature_id>/modifier/', views.modifier_candidature, name='modifier_candidature'),
    path('api/candidatures/<int:candidature_id>/supprimer/', views.supprimer_candidature, name='supprimer_candidature'),

    # ==================== EVALUATIONS ====================
    path('api/evaluations/', views.liste_evaluations, name='liste_evaluations'),
    path('api/evaluations/ajout/', views.ajout_evaluation, name='ajout_evaluation'),
    path('api/evaluations/<int:evaluation_id>/modifier/', views.modifier_evaluation, name='modifier_evaluation'),
    path('api/evaluations/<int:evaluation_id>/supprimer/', views.supprimer_evaluation, name='supprimer_evaluation'),
    path('api/evaluations/<int:evaluation_id>/send_email/', views.send_evaluation_email_to_all, name='send_email_evaluation'),
  

    # ==================== RESULTATS ====================
    path('api/resultats/', views.liste_resultats, name='liste_resultats'),
    path('api/resultats/ajout/', views.ajout_resultat, name='ajout_resultat'),
    path('api/resultats/<int:resultat_id>/modifier/', views.modifier_resultat, name='modifier_resultat'),
    path('api/resultats/<int:resultat_id>/supprimer/', views.supprimer_resultat, name='supprimer_resultat'),

]

# ==================== MEDIA FILES ====================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
