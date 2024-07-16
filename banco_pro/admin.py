from django.contrib import admin
from .models import FormProject

# Elimina el registro duplicado si existe
try:
    admin.site.unregister(FormProject)
except admin.sites.NotRegistered:
    pass

class FormProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_id','user', 'project_name', 'sector', 'tipo_proyecto', 'tipo_entidad',
        'dependencia', 'organismo', 'municipioEnd', 'fecha_registro', 
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.list_display:
            formfield.widget.attrs.update({'class': 'field-name'})
        return formfield

admin.site.register(FormProject, FormProjectAdmin)
