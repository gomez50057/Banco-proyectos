from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views
from .views import BulkCreateProjects, project_list_view, ProjectView, current_user, redirect_to_home

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Home page
    path('', TemplateView.as_view(template_name='index.html')),
    
    # Admin project list view
    path('admin/projects/', project_list_view, name='project-list'),
    
    # User authentication URLs
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),

    # Project-related URLs
    path('guardar-proyecto/', views.create_project, name='create_project'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),
    path('ver-proyectos-tabla/', ProjectView.as_view(), name='ver-proyectos-tabla'),
    path('proyecto/<int:pk>/', ProjectView.as_view(), name='project-detail'),
    path('proyecto/', ProjectView.as_view(), name='project-create'),
    
    # API URL to get the current user
    path('api/current_user/', current_user, name='current_user'),

    # Template views
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('table/', TemplateView.as_view(template_name='index.html'), name='table'),
    
    # Catch-all URL to redirect to home
    re_path(r'^.*$', redirect_to_home),
]
