from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.miss_list, name="miss_list"),
    path('vote/<int:miss_id>/', views.vote, name="vote"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
