# models.py
from django.db import models
from django.contrib.auth.models import User
import os

# class FormProjectHistory(models.Model):
#     project = models.ForeignKey('FormProject', on_delete=models.CASCADE, related_name='history')
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     changes = models.JSONField()  # Guardará los cambios en formato JSON

#     def __str__(self):
#         return f"Historial de {self.project.nombre_proyecto} - {self.timestamp}"

def document_upload_to(instance, filename):
    """
    Construye la ruta de almacenamiento para un documento.
    Se intenta obtener el valor del campo 'project_id' (campo custom) del proyecto relacionado;
    si no está disponible, se usa 'unknown' como valor.
    Ya no se agrega "Documents" ya que esto esta hiendo definido en MEDIA_ROOT donde se establece
    Ruta: 'Documents/bancoProyectos/<project_custom_id>/<document_type>/<filename>'
    """
    try:
        # Intentamos obtener el campo custom 'project_id' del proyecto relacionado
        project_custom_id = instance.project.project_id
        if not project_custom_id:
            project_custom_id = 'unknown'
    except Exception:
        project_custom_id = 'unknown'
    return f"bancoProyectos/{project_custom_id}/{instance.document_type}/{filename}"


class FormProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    area_adscripcion = models.CharField(max_length=255, null=True, blank=True, default="")
    nombre_registrante = models.CharField(max_length=255, null=True, blank=True, default="")
    apellido_paterno = models.CharField(max_length=255, null=True, blank=True, default="")
    apellido_materno = models.CharField(max_length=255, null=True, blank=True, default="")
    correo = models.EmailField(max_length=255, null=True, blank=True, default="")
    telefono = models.CharField(max_length=10, null=True, blank=True, default="")
    telefono_ext = models.CharField(max_length=10, null=True, blank=True, default="")

    fecha_registro = models.DateField(auto_now_add=True)


    # Campos con pareja: campo principal, isBlocked y observacion
    nombre_proyecto = models.CharField(max_length=255)
    isBlocked_nombre_proyecto = models.BooleanField(default=False)
    observacion_nombre_proyecto = models.TextField(null=True, blank=True)

    sector = models.CharField(max_length=255)
    isBlocked_sector = models.BooleanField(default=False)
    observacion_sector = models.TextField(null=True, blank=True)

    tipo_proyecto = models.CharField(max_length=255)
    isBlocked_tipo_proyecto = models.BooleanField(default=False)
    observacion_tipo_proyecto = models.TextField(null=True, blank=True)

    tipo_entidad = models.CharField(max_length=255)
    isBlocked_tipo_entidad = models.BooleanField(default=False)
    observacion_tipo_entidad = models.TextField(null=True, blank=True)

    dependencia = models.CharField(max_length=255, null=True, blank=True)
    isBlocked_dependencia = models.BooleanField(default=False)
    observacion_dependencia = models.TextField(null=True, blank=True)

    organismo = models.CharField(max_length=255, null=True, blank=True)
    isBlocked_organismo = models.BooleanField(default=False)
    observacion_organismo = models.TextField(null=True, blank=True)

    municipio_ayuntamiento = models.CharField(max_length=255, null=True, blank=True)
    isBlocked_municipio_ayuntamiento = models.BooleanField(default=False)
    observacion_municipio_ayuntamiento = models.TextField(null=True, blank=True)

    unidad_responsable = models.CharField(max_length=255)
    isBlocked_unidad_responsable = models.BooleanField(default=False)
    observacion_unidad_responsable = models.TextField(null=True, blank=True)

    unidad_presupuestal = models.CharField(max_length=255)
    isBlocked_unidad_presupuestal = models.BooleanField(default=False)
    observacion_unidad_presupuestal = models.TextField(null=True, blank=True)

    inversion_federal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    isBlocked_inversion_federal = models.BooleanField(default=False)
    observacion_inversion_federal = models.TextField(null=True, blank=True)

    inversion_estatal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    isBlocked_inversion_estatal = models.BooleanField(default=False)
    observacion_inversion_estatal = models.TextField(null=True, blank=True)

    inversion_municipal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    isBlocked_inversion_municipal = models.BooleanField(default=False)
    observacion_inversion_municipal = models.TextField(null=True, blank=True)

    inversion_otros = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    isBlocked_inversion_otros = models.BooleanField(default=False)
    observacion_inversion_otros = models.TextField(null=True, blank=True)

    inversion_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    isBlocked_inversion_total = models.BooleanField(default=False)
    observacion_inversion_total = models.TextField(null=True, blank=True)

    ramo_presupuestal = models.CharField(max_length=255)
    isBlocked_ramo_presupuestal = models.BooleanField(default=False)
    observacion_ramo_presupuestal = models.TextField(null=True, blank=True)

    descripcion = models.TextField()
    isBlocked_descripcion = models.BooleanField(default=False)
    observacion_descripcion = models.TextField(null=True, blank=True)

    situacion_sin_proyecto = models.TextField()
    isBlocked_situacion_sin_proyecto = models.BooleanField(default=False)
    observacion_situacion_sin_proyecto = models.TextField(null=True, blank=True)

    objetivos = models.TextField()
    isBlocked_objetivos = models.BooleanField(default=False)
    observacion_objetivos = models.TextField(null=True, blank=True)

    metas = models.TextField()
    isBlocked_metas = models.BooleanField(default=False)
    observacion_metas = models.TextField(null=True, blank=True)

    gasto_programable = models.CharField(max_length=255)
    isBlocked_gasto_programable = models.BooleanField(default=False)
    observacion_gasto_programable = models.TextField(null=True, blank=True)

    tiempo_ejecucion = models.IntegerField(null=True, blank=True)
    isBlocked_tiempo_ejecucion = models.BooleanField(default=False)
    observacion_tiempo_ejecucion = models.TextField(null=True, blank=True)

    modalidad_ejecucion = models.CharField(max_length=255)
    isBlocked_modalidad_ejecucion = models.BooleanField(default=False)
    observacion_modalidad_ejecucion = models.TextField(null=True, blank=True)

    programa_presupuestario = models.CharField(max_length=255)
    isBlocked_programa_presupuestario = models.BooleanField(default=False)
    observacion_programa_presupuestario = models.TextField(null=True, blank=True)

    beneficiarios = models.IntegerField(null=True, blank=True)
    isBlocked_beneficiarios = models.BooleanField(default=False)
    observacion_beneficiarios = models.TextField(null=True, blank=True)

    normativa_aplicable = models.TextField()
    isBlocked_normativa_aplicable = models.BooleanField(default=False)
    observacion_normativa_aplicable = models.TextField(null=True, blank=True)

    region = models.JSONField()
    isBlocked_region = models.BooleanField(default=False)
    observacion_region = models.TextField(null=True, blank=True)

    municipio = models.JSONField()
    isBlocked_municipio = models.BooleanField(default=False)
    observacion_municipio = models.TextField(null=True, blank=True)

    localidad = models.CharField(max_length=255)
    isBlocked_localidad = models.BooleanField(default=False)
    observacion_localidad = models.TextField(null=True, blank=True)

    barrio_colonia = models.CharField(max_length=255)
    isBlocked_barrio_colonia = models.BooleanField(default=False)
    observacion_barrio_colonia = models.TextField(null=True, blank=True)

    tipo_localidad = models.CharField(max_length=255)
    isBlocked_tipo_localidad = models.BooleanField(default=False)
    observacion_tipo_localidad = models.TextField(null=True, blank=True)

    latitud = models.FloatField()
    isBlocked_latitud = models.BooleanField(default=False)
    observacion_latitud = models.TextField(null=True, blank=True)

    longitud = models.FloatField()
    isBlocked_longitud = models.BooleanField(default=False)
    observacion_longitud = models.TextField(null=True, blank=True)

    plan_nacional = models.CharField(max_length=255)
    isBlocked_plan_nacional = models.BooleanField(default=False)
    observacion_plan_nacional = models.TextField(null=True, blank=True)

    plan_estatal = models.CharField(max_length=255)
    isBlocked_plan_estatal = models.BooleanField(default=False)
    observacion_plan_estatal = models.TextField(null=True, blank=True)

    plan_municipal = models.TextField(null=True, blank=True)
    isBlocked_plan_municipal = models.BooleanField(default=False)
    observacion_plan_municipal = models.TextField(null=True, blank=True)

    acuerdos_transversales= models.CharField(max_length=255, null=True, blank=True)
    isBlocked_acuerdos_transversales = models.BooleanField(default=False)
    observacion_acuerdos_transversales = models.TextField(null=True, blank=True)

    ods = models.CharField(max_length=255)
    isBlocked_ods = models.BooleanField(default=False)
    observacion_ods = models.TextField(null=True, blank=True)

    programas_SIE = models.CharField(max_length=255)
    isBlocked_programas_SIE = models.BooleanField(default=False)
    observacion_programas_SIE = models.TextField(null=True, blank=True)

    indicadores_estrategicos = models.CharField(max_length=255)
    isBlocked_indicadores_estrategicos = models.BooleanField(default=False)
    observacion_indicadores_estrategicos = models.TextField(null=True, blank=True)

    indicadores_socioeconomicos = models.CharField(max_length=255)
    isBlocked_indicadores_socioeconomicos = models.BooleanField(default=False)
    observacion_indicadores_socioeconomicos = models.TextField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)
    isBlocked_observaciones = models.BooleanField(default=False)
    observacion_observaciones = models.TextField(null=True, blank=True)

    porcentaje_avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    isBlocked_porcentaje_avance = models.BooleanField(default=False)
    observacion_porcentaje_avance = models.TextField(null=True, blank=True)

    retroalimentacion = models.TextField(null=True, blank=True)
    isBlocked_retroalimentacion = models.BooleanField(default=False)
    observacion_retroalimentacion = models.TextField(null=True, blank=True)

    estatus = models.CharField(max_length=50, choices=[('Atendido', 'Atendido'), ('En Proceso', 'En Proceso'), ('Registrado', 'Registrado')], default='Registrado')
    isBlocked_estatus = models.BooleanField(default=False)
    observacion_estatus = models.TextField(null=True, blank=True)

    situacion = models.CharField(max_length=50, choices=[('Vigente', 'Vigente'), ('Antecedente', 'Antecedente'), ('Cancelado', 'Cancelado')], default='Vigente')
    isBlocked_situacion = models.BooleanField(default=False)
    observacion_situacion = models.TextField(null=True, blank=True)


    # Campos adicionales sin campo principal previo, agrupados en pareja
    isBlocked_project = models.BooleanField(default=True, verbose_name='¿Liberar Formulario?', help_text='Marca esta casilla para habilitar la edición al usuario en los campos permitidos.')

    # Documentos

    isBlocked_estudios_factibilidad = models.BooleanField(default=False)
    observacion_estudios_factibilidad = models.TextField(null=True, blank=True)

    isBlocked_analisis_alternativas = models.BooleanField(default=False)
    observacion_analisis_alternativas = models.TextField(null=True, blank=True)

    isBlocked_validacion_normativa = models.BooleanField(default=False)
    observacion_validacion_normativa = models.TextField(null=True, blank=True)

    isBlocked_liberacion_derecho_via = models.BooleanField(default=False)
    observacion_liberacion_derecho_via = models.TextField(null=True, blank=True)

    isBlocked_analisis_costo_beneficio = models.BooleanField(default=False)
    observacion_analisis_costo_beneficio = models.TextField(null=True, blank=True)

    isBlocked_proyecto_ejecutivo = models.BooleanField(default=False)
    observacion_proyecto_ejecutivo = models.TextField(null=True, blank=True)

    isBlocked_manifestacion_impacto_ambiental = models.BooleanField(default=False)
    observacion_manifestacion_impacto_ambiental = models.TextField(null=True, blank=True)

    isBlocked_render = models.BooleanField(default=False)
    observacion_render = models.TextField(null=True, blank=True)

    isBlocked_otros_estudios = models.BooleanField(default=False)
    observacion_otros_estudios = models.TextField(null=True, blank=True)


    # # Campos para auditoría
    # last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_modified_projects')
    # last_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_proyecto
    

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('estudios_factibilidad', 'Estudios de Factibilidad'),
        ('analisis_alternativas', 'Análisis de Alternativas'),
        ('validacion_normativa', 'Validación Normativa'),
        ('liberacion_derecho_via', 'Liberación Derecho Vía'),
        ('analisis_costo_beneficio', 'Análisis Costo Beneficio'),
        ('proyecto_ejecutivo', 'Proyecto Ejecutivo'),
        ('manifestacion_impacto_ambiental', 'Manifestación Impacto Ambiental'),
        ('render', 'Render'),
        ('otros_estudios', 'Otros Estudios'),
    )
    
    project = models.ForeignKey(FormProject, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to=document_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.project_id} - {self.document_type}"





def custom_upload_to(instance, filename):
    # Obtener el ID del proyecto y el tipo de anexo
    project_id = instance.cedula.projInvestment_id  # Se obtiene de la relación ForeignKey
    tipo_anexo = instance.get_tipo_anexo_display()  # Mostrar la representación legible del tipo de anexo
    
    # Construir la ruta: 'Documents/investmentform2025/projInvestment_id/tipo_anexo/'
    return os.path.join('Documents', 'investmentform2025', project_id, tipo_anexo, filename)

class AnexoProyecto(models.Model):
    TIPOS_ANEXO = [
        ('estudios_factibilidad', 'Estudios de Factibilidad'),
        ('analisis_alternativas', 'Análisis de Alternativas'),
        ('validacion_normativa', 'Validación Normativa'),
        ('liberacion_derecho_via', 'Liberación de Derecho de Vía'),
        ('analisis_costo_beneficio', 'Análisis Costo-Beneficio'),
        ('expediente_tecnico_docu', 'Expediente Técnico'),
        ('proyecto_ejecutivo', 'Proyecto Ejecutivo'),
        ('manifestacion_impacto_ambiental', 'Manifestación de Impacto Ambiental'),
        ('fotografia_render_proyecto', 'Fotografía Render del Proyecto'),
        ('otros_estudios', 'Otros Estudios'),
    ]

    cedula = models.ForeignKey('CedulaRegistro', related_name='anexos_proyectos', on_delete=models.CASCADE)
    tipo_anexo = models.CharField(max_length=50, choices=TIPOS_ANEXO, default='otros_estudios')
    archivo = models.FileField(upload_to=custom_upload_to)  # Usa la función personalizada para guardar el archivo
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_anexo_display()} - {self.archivo.name}"

class CedulaRegistro(models.Model):
    # Agrega el campo para guardar el usuario que envió el formulario
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # ID de proyecto
    projInvestment_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Información del responsable del proyecto
    nombre_dependencia = models.CharField(max_length=255, blank=True, null=True)
    area_adscripcion = models.CharField(max_length=255, blank=True, null=True)
    nombre_registrante = models.CharField(max_length=255, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)

    # Datos generales del proyecto
    fecha_registro = models.DateField(blank=True, null=True)
    ejercicio_fiscal = models.CharField(max_length=4, blank=True, null=True)
    dependencia = models.CharField(max_length=255, blank=True, null=True)
    organismo = models.CharField(max_length=255, blank=True, null=True)
    unidad_responsable = models.CharField(max_length=255, blank=True, null=True)
    unidad_presupuestal = models.CharField(max_length=255, blank=True, null=True)
    nombre_proyecto = models.CharField(max_length=250, blank=True, null=True)
    descripcion_proyecto = models.TextField(max_length=1000, blank=True, null=True)
    situacion_actual = models.TextField(max_length=1000, blank=True, null=True)
    tipo_obra = models.CharField(max_length=50, blank=True, null=True)
    calendario_ejecucion = models.CharField(max_length=50, blank=True, null=True)
    beneficio_social = models.TextField(max_length=500, blank=True, null=True)
    beneficio_economico = models.TextField(max_length=500, blank=True, null=True)
    numero_beneficiarios = models.IntegerField(blank=True, null=True)
    inversion_presupuestada = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    # Cobertura del proyecto
    cobertura = models.CharField(max_length=50, choices=[('Estatal', 'Estatal'), ('Regional', 'Regional'), ('Municipal', 'Municipal')], blank=True, null=True)
    regiones = models.JSONField(blank=True, null=True)
    municipios = models.JSONField(blank=True, null=True)

    # Alineación estratégica
    ods = models.TextField(blank=True, null=True)
    plan_estatal = models.TextField(blank=True, null=True)
    objetivo_ped = models.TextField(blank=True, null=True)
    estrategia_ped = models.TextField(blank=True, null=True)
    linea_accion_ped = models.TextField(blank=True, null=True)
    indicador_ped = models.TextField(blank=True, null=True)
    programa_sectorial = models.TextField(blank=True, null=True)
    objetivo_programa = models.TextField(blank=True, null=True)
    propuesta_campana = models.CharField(max_length=50, blank=True, null=True)
    cual_propuesta = models.TextField(blank=True, null=True)
    prioridad = models.TextField(blank=True, null=True)
    expediente_tecnico = models.CharField(max_length=50, blank=True, null=True)

    # Relación con anexos (múltiples tipos de archivos para cada anexo)
    anexos = models.ManyToManyField(AnexoProyecto, related_name='cedulas', blank=True)

    # Campos de bloqueo
    is_blocked_project = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_proyecto or "Proyecto sin nombre"
