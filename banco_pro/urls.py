# urls.py

from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import BulkCreateProjects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),

    # URLs relacionadas con el usuario
    # path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),

    path('ver-usuarios/', views.ver_usuarios_registrados, name='ver_usuarios_registrados'),
    # path('ver-proyectos/', views.ver_proyectos_registrados, name='ver_proyectos_registrados'),

    path('guardar-proyecto/', views.create_project, name='create_project'),
    path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),

    path('ver-proyectos-tabla/', views.ver_proyectos_tabla, name='ver_proyectos_tabla'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),


    # path('ver-proyectos-registrados/', views.ver_proyectos_registrados, name='ver_proyectos_registrados'),
    # path('ver-proyectos-tabla/', views.ver_proyectos_en_tabla, name='ver_proyectos_en_tabla'),
] 



