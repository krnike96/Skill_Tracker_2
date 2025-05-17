from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_skill, name='add_skill'),
    path('edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('export/<str:format>/', views.export_profile, name='export_profile'),
]