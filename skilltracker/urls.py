from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from skills import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('skills/', include('skills.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)