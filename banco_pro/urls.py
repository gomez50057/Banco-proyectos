from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import BulkCreateProjects, ProjectView, ReactAppView, UpdateProjectView
# from .views import BulkCreateProjects, ProjectView, ReactAppView, generate_pdf, UpdateProjectView
from . import views
from .views import project_list_view, current_user
from .views import BulkCreateUsers


urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Home page
    path('', TemplateView.as_view(template_name='index.html')),
    
    # Admin project list view
    path('admin/projects/', project_list_view, name='project-list'),

    path('bulk-create-users/', BulkCreateUsers.as_view(), name='bulk-create-users'),

    
    # User authentication URLs
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    # path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),

    # Project-related URLs
    path('guardar-proyecto/', views.create_project, name='create_project'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),
    path('ver-proyectos-tabla/', ProjectView.as_view(), name='ver-proyectos-tabla'),
    path('proyecto/', ProjectView.as_view(), name='project-create'),
    path('proyecto/<str:project_id>/', ProjectView.as_view(), name='project-detail'),
    # path('proyecto/reporte/<str:project_id>/', generate_pdf, name='project-report'),
    path('update-project/<str:project_id>/', UpdateProjectView.as_view(), name='update-project'),

    path('ver-proyectos-usuario/', views.ver_proyectos_usuario, name='ver_proyectos_usuario'),
   
    # API URL to get the current user
    path('api/current_user/', current_user, name='current_user'),

    # Template views
    path('login/', ReactAppView.as_view(), name='login'),
    path('table/', ReactAppView.as_view(), name='table'),
    path('panel-usuario/', ReactAppView.as_view(), name='panel-usuario'),
    path('consulta/', ReactAppView.as_view(), name='consulta'),

    # Para todas las demás rutas, redirige a la vista de React
    re_path(r'^(?!admin|inicio-sesion|guardar-proyecto|masivacarga|ver-proyectos-tabla|proyecto|api|static).*$',
            ReactAppView.as_view(), name='react-app'),
]
