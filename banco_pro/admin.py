from django.contrib import admin
from .models import FormProject, Document
from .models import CedulaRegistro
from django import forms
from django.utils.safestring import mark_safe

# Lista de nombres de usuario que NO deben tener acceso al admin original
ALLOWED_USERS = ['fer.proyectos', 'armando.proyectos', 'godo.proyectos', 'Thanos.proyectos']

# Sobrescribimos el has_permission del admin original para negar acceso a usuarios de ALLOWED_USERS
def custom_has_permission(self, request):
    return request.user.is_active and request.user.is_staff and request.user.username not in ALLOWED_USERS

# Asignamos nuestro método al objeto admin.site
admin.site.has_permission = custom_has_permission.__get__(admin.site, admin.site.__class__)


# Elimina el registro duplicado si existe
try:
    admin.site.unregister(FormProject)
except admin.sites.NotRegistered:
    pass

class DocumentInlineForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        labels = {
            'document_type': 'Tipo de documento',
            'file': 'Ruta del archivo',
            'uploaded_at': 'Subido el',
        }

class DocumentInline(admin.TabularInline):
    model = Document
    form  = DocumentInlineForm
    verbose_name = "Documento Anexado"
    verbose_name_plural = "Documentos Anexados"

    extra = 0
    fields = ('document_type', 'file', 'file_preview', 'uploaded_at')
    readonly_fields = ('file_preview', 'uploaded_at')

    def file_preview(self, obj):
        if obj.file:
            return mark_safe(f'<a href="{obj.file.url}" target="_blank">Ver archivo</a>')
        return "-"
    file_preview.short_description = "Archivo"

class FormProjectAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
    list_display = (
        'project_id','user', 'nombre_proyecto', 'sector', 'tipo_proyecto', 'tipo_entidad',
        'dependencia', 'organismo', 'municipio_ayuntamiento', 'fecha_registro',
    )

    list_filter = ('user__username', 'sector', 'tipo_proyecto', 'tipo_entidad', 'dependencia', 'organismo', 'municipio_ayuntamiento', 'fecha_registro')

    search_fields = ('nombre_proyecto', 'project_id',)

    readonly_fields = ('fecha_registro',)

    def get_fields(self, request, obj=None):
        # Recojo solo los campos editables, columna directa y que NO sean PK,
        #    ni observaciones ni isBlocked.
        base_fields = []
        for f in self.model._meta.get_fields():
            # descartamos relaciones M2M/M2O
            if not getattr(f, 'column', None):
                continue
            # descartamos PK y no editables
            if f.primary_key or not f.editable:
                continue
            # descartamos observaciones y banderas
            if f.name.startswith('observacion_') or f.name.startswith('isBlocked_'):
                continue
            base_fields.append(f.name)

        # Emparejo cada campo con su isBlocked_ si existe
        fields = []
        # saco de nuevo todos los nombres para poder comprobar existencia
        all_names = [f.name for f in self.model._meta.get_fields()]
        for name in base_fields:
            paired = f'isBlocked_{name}'
            if paired in all_names:
                fields.append((name, paired))
            else:
                fields.append(name)

        # Añado “a mano” cualquier bandera que no emparejó
        if 'isBlocked_project' in all_names:
            fields.append('isBlocked_project')

        # Finalmente los campos read‐only
        fields.append('fecha_registro')
        return fields

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        # 1) Si es isBlocked_XXX, quitamos el texto del label excepto isBlocked_project
        if db_field.name.startswith('isBlocked_') and db_field.name != 'isBlocked_project':
            formfield.label = ''
        # 2) Si es uno de los campos de list_display, aplicamos tu clase CSS
        if db_field.name in self.list_display:
            formfield.widget.attrs.update({'class': 'field-name'})
        return formfield
admin.site.register(FormProject, FormProjectAdmin)

# class DocumentInline(admin.TabularInline):
#     """
#     Permite editar los documentos asociados a un proyecto
#     directamente desde la interfaz de administración del proyecto.
#     """
#     model = Document
#     extra = 1  # Número de formularios adicionales que se muestran por defecto

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Document.
    Permite ver y filtrar los documentos subidos.
    """
    list_display = ('project', 'document_type', 'file', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('project__project_id', 'document_type')

class CedulaRegistroAdmin(admin.ModelAdmin):
    list_display = ('projInvestment_id', 'user', 'nombre_proyecto', 'dependencia', 'organismo', 'unidad_responsable', 'fecha_registro', 'ejercicio_fiscal')

    # Añadir filtros por algunos de los campos
    list_filter = ('user__username' ,'unidad_responsable', 'dependencia', 'organismo', 'ejercicio_fiscal')

    # Hacer que algunos campos se puedan buscar
    search_fields = ('nombre_proyecto', 'projInvestment_id',)
admin.site.register(CedulaRegistro, CedulaRegistroAdmin)