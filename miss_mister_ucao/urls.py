from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.miss_list, name="miss_list"),
    path('vote/<int:miss_id>/', views.vote, name="vote"),
    path('get_results/', views.get_results, name="get_results"),  # Nouvelle URL pour le graphique
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
