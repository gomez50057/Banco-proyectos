from django.contrib import admin
from .models import NivelacionTierra, ArchivoPDF


@admin.register(NivelacionTierra)
class NivelacionTierra(admin.ModelAdmin):
    list_display = (
        'folio', 'nombre', 'apellido_paterno', 'curp',
        'superficie_parcela', 'fecha'
    )
    list_filter = ['municipio', 'distrito_riego']
    search_fields = ('folio', 'nombre', 'apellido_paterno', 'curp')
    readonly_fields = ('folio',)
    date_hierarchy = 'fecha'


@admin.register(ArchivoPDF)
class ArchivoPDFAdmin(admin.ModelAdmin):
    list_display = ('nivelacion',)
    search_fields = ('nivelacion__folio',)
