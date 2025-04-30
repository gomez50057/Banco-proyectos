from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import admin
from .models import FormProject, Document
from .admin import FormProjectAdmin  # Configuración original de FormProjectAdmin

ALLOWED_USERS = ['myadmin', 'edit', 'fer.proyectos', 'armando.proyectos', 'godo.proyectos', 'Thanos.proyectos']  # Usuarios permitidos

class DocumentInline(admin.TabularInline):
    """
    Permite editar los documentos asociados a un proyecto
    directamente desde la interfaz de administración del proyecto.
    """
    model = Document
    extra = 1  # Número de formularios adicionales que se muestran por defecto

class DocumentAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Document.
    Permite ver y filtrar los documentos subidos.
    """
    list_display = ('project', 'document_type', 'file', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('project__project_id', 'document_type')

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración Proyectos"
    site_title = "Admin Proyectos"
    index_title = "Bienvenido al admin Proyectos"

    def has_permission(self, request):
        # Permite acceso solo a usuarios activos y cuyo nombre de usuario esté en la lista permitida
        return request.user.is_active and request.user.username in ALLOWED_USERS

    def index(self, request, extra_context=None):
        """
        Redirige directamente al listado de FormProject,
        evitando mostrar el panel de control general.
        """
        app_label = FormProject._meta.app_label
        model_name = FormProject._meta.model_name
        # Usamos el namespace del admin personalizado (self.name)
        changelist_url = reverse(f'{self.name}:{app_label}_{model_name}_changelist')
        return redirect(changelist_url)

# Creamos subclases de los ModelAdmin para deshabilitar agregar y borrar

class CustomFormProjectAdmin(FormProjectAdmin):
    def has_add_permission(self, request):
        return False  # Deshabilita la opción de crear

    def has_delete_permission(self, request, obj=None):
        return False  # Deshabilita la opción de borrar

class CustomDocumentAdmin(DocumentAdmin):
    def has_add_permission(self, request):
        return False  # Deshabilita la opción de crear

    def has_delete_permission(self, request, obj=None):
        return False  # Deshabilita la opción de borrar

# Instancia del admin personalizado con el namespace 'custom_admin'
custom_admin_site = CustomAdminSite(name='custom_admin')

# Registra únicamente los modelos deseados en este panel Proyectos con sus respectivos ModelAdmin modificados:
custom_admin_site.register(FormProject, CustomFormProjectAdmin)
custom_admin_site.register(Document, CustomDocumentAdmin)
