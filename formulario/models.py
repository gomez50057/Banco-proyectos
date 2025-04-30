from django.contrib.auth import get_user_model
from django.db import models
from .utils import distritos, modulos
from datetime import date
import os

User = get_user_model()

def archivo_pdf_path(instance, filename):
    folio = instance.folio or 'temp'
    return os.path.join('nivelación de tierra', f'{folio}', 'archivos_pdfs', filename)

def constancia_pdf_path(instance, filename):
    folio = instance.folio or 'temp'
    return os.path.join('nivelación de tierra', f'{folio}', 'constancia_pdf', filename)

class NivelacionTierra(models.Model):
    # Datos generales del solicitante
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    curp = models.CharField(max_length=18)
    cuenta_conagua = models.CharField(max_length=100)
    domicilio = models.TextField()
    identificacion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    # Datos de la parcela
    municipio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    distrito_riego = models.CharField(max_length=100)
    modulo_riego = models.CharField(max_length=100)

    superficie_parcela = models.FloatField()
    tiempo_promedio_riego = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    grado_pendiente = models.CharField(max_length=100)
    pedregosidad = models.CharField(max_length=100)
    profundidad_suelo = models.CharField(max_length=100)
    tamano_canaleta = models.FloatField()
    tipo_revestimiento = models.CharField(max_length=100)
    gasto_canales = models.CharField(max_length=100)
    distancia_canaleta = models.FloatField()
    tipo_seccion = models.CharField(max_length=100)

    ha_nivelado = models.CharField(max_length=10)
    anio_nivelacion = models.CharField(max_length=10, blank=True, null=True)
    problemas_drenaje = models.CharField(max_length=10)
    cultivos_dominantes = models.CharField(max_length=100)
    cultivo_actual = models.CharField(max_length=100)
    perene_roturacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_libre_parcela = models.CharField(max_length=100, blank=True, null=True)

    acreditacion_propiedad = models.CharField(max_length=10)
    documento_presentado = models.CharField(max_length=100)
    archivo_pdf = models.FileField(upload_to=archivo_pdf_path, blank=True, null=True)
    curso_sader = models.CharField(max_length=10)
    cuando_toma_sader = models.CharField(max_length=100, blank=True, null=True)
    constancia_pdf = models.FileField(upload_to=constancia_pdf_path, blank=True, null=True)

    firma_digital = models.TextField()  # <-- Aquí se guarda el Base64

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nivelaciones_creadas",
        help_text="Usuario que creó este formulario"
    )

    # Metadatos
    fecha = models.DateField(default=date.today)
    folio = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.folio:
            super().save(*args, **kwargs)
            distrito = distritos.get(self.distrito_riego, '000')
            modulo = modulos.get(self.modulo_riego, '000')
            self.folio = f'SPNT-{distrito}-{modulo}-{self.id}'
            super().save(update_fields=["folio"])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.folio

class ArchivoPDF(models.Model):
    nivelacion = models.OneToOneField(
        'NivelacionTierra',
        on_delete=models.CASCADE,
        related_name='archivo',
    )
    area_atencion_prioritaria = models.CharField(max_length=10, blank=True, null=True)
    convenio_colaboracion_pnh = models.CharField(max_length=10, blank=True, null=True)
    pendiente_promedio = models.CharField(max_length=50, blank=True, null=True)
    volumen_agua_anual = models.FloatField(blank=True, null=True)
    profundidad_suelo_pedregosidad = models.CharField(max_length=50, blank=True, null=True)
    nivel_pedregosidad = models.CharField(max_length=50, blank=True, null=True)
    acreditacion_propiedad = models.CharField(max_length=50, blank=True, null=True)
    constancia_curso = models.CharField(max_length=10, blank=True, null=True)
    tipo_suelo = models.CharField(max_length=100, blank=True, null=True)
    nombre_revisor = models.CharField(max_length=100, blank=True, null=True)
    firma_digital = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Validación de {self.nivelacion.folio}"

