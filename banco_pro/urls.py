from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import BulkCreateProjects, ProjectView, ReactAppView, UpdateProjectView
# from .views import BulkCreateProjects, ProjectView, ReactAppView, generate_pdf, UpdateProjectView
from . import views
from .views import project_list_view, current_user, logout_view
from .views import BulkCreateUsers
from .views import CedulaRegistroListCreateView, CedulaRegistroDetailUpdateDeleteView
from .views import refresh_csrf_token
from . import views
from .views import ProjectIdListView  
from .views import AnexosProyectoListView

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

    path('api/logout/', logout_view, name='logout'),

    # Template views usando BrowserRouter
    # path('login/', ReactAppView.as_view(), name='login'),
    # path('table/', ReactAppView.as_view(), name='table'),
    # path('panel-usuario/', ReactAppView.as_view(), name='panel-usuario'),
    # path('consulta/', ReactAppView.as_view(), name='consulta'),
    # path('reporte-inversion/161309240001/', ReactAppView.as_view(), name='reporte-inversion'),

    # cedulas
    path('cedulas/', CedulaRegistroListCreateView.as_view(), name='cedula-list-create'),
    path('cedulas/<str:projInvestment_id>/', CedulaRegistroDetailUpdateDeleteView.as_view(), name='cedula-detail-update-delete'),

    path('api/csrf-token/', refresh_csrf_token, name='refresh_csrf_token'),
    path('api/proyectos_totales/', views.proyectos_totales, name='proyectos_totales'),
    path('api/proyectos_por_unidad_responsable/', views.proyectos_por_unidad_responsable, name='proyectos_por_unidad_responsable'),
    path('api/proyectos_por_usuario/', views.proyectos_por_usuario, name='proyectos_por_usuario'),
    path('api/propuesta_campana/', views.propuesta_campana, name='propuesta_campana'),
    path('api/cual_propuesta/', views.cual_propuesta, name='cual_propuesta'),
    path('api/cobertura_proyecto/', views.cobertura_proyecto, name='cobertura_proyecto'),
    path('api/proj-ids/', ProjectIdListView.as_view(), name='project_id_list'), 
    
    path('todos-anexos/', AnexosProyectoListView.as_view(), name='todos-anexos'),    
    path('cedulas/anexos/<projInvestment_id>/', AnexosProyectoListView.as_view(), name='anexos-proyecto'),

    # Para todas las demás rutas, redirige a la vista de React
    re_path(r'^(?!admin|api|static|media).*$',
        ReactAppView.as_view(), name='react-app'),
]
