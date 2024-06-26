# urls.py

from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import BulkCreateProjects
from .views import project_list_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),

    path('admin/projects/', project_list_view, name='project-list'),


    # URLs relacionadas con el usuario
    # path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),

    path('guardar-proyecto/', views.create_project, name='create_project'),
    path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),

    path('ver-proyectos-tabla/', views.ver_proyectos_tabla, name='ver_proyectos_tabla'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),

   
] 



