# # urls.py

# from django.contrib import admin
# from django.views.generic import TemplateView
# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views
# from .views import BulkCreateProjects
# from .views import project_list_view
# from .views import ProjectView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='index.html')),
#     path('admin/projects/', project_list_view, name='project-list'),

#     # URLs relacionadas con el usuario
#     # path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
#     path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),

#     path('guardar-proyecto/', views.create_project, name='create_project'),
#     path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),

#     # path('ver-proyectos-tabla/', views.ver_proyectos_tabla, name='ver_proyectos_tabla'),
#     path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),

#     path('ver-proyectos-tabla/', ProjectView.as_view(), name='ver-proyectos-tabla'),
#     path('proyecto/<int:pk>/', ProjectView.as_view(), name='project-detail'),
#     path('proyecto/', ProjectView.as_view(), name='project-create'),  
# ] 


# urls.py

from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    inicio_sesion,
    create_project,
    BulkCreateProjects,
    project_list_view,
    ProjectView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),

    # URLs relacionadas con proyectos
    path('admin/projects/', project_list_view, name='project-list'),
    path('masivacarga/', BulkCreateProjects.as_view(), name='bulk-create-projects'),
    path('ver-proyectos-tabla/', ProjectView.as_view(), name='ver-proyectos-tabla'),
    path('proyecto/<int:pk>/', ProjectView.as_view(), name='project-detail'),
    path('proyecto/', ProjectView.as_view(), name='project-create'),

    # URLs relacionadas con el usuario
    path('inicio-sesion/', inicio_sesion, name='inicio_sesion'),
    path('guardar-proyecto/', create_project, name='create_project'),
    path('login/', auth_views.LoginView.as_view(template_name='LoginLayout'), name='login'),
]
