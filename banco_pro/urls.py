from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from .views import BulkCreateProjects, project_list_view, ProjectView, current_user

from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import redirect_to_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),

    path('admin/projects/', project_list_view, name='project-list'),
    
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('guardar-proyecto/', views.create_project, name='create_project'),
    path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),
    
    path('ver-proyectos-tabla/', ProjectView.as_view(), name='ver-proyectos-tabla'),
    path('proyecto/<int:pk>/', ProjectView.as_view(), name='project-detail'),
    path('proyecto/', ProjectView.as_view(), name='project-create'),
    
    # URL para obtener el usuario actual
    path('api/current_user/', current_user, name='current_user'),



  
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('table/', TemplateView.as_view(template_name='index.html'), name='table'),
    re_path(r'^.*$', redirect_to_home),
]
