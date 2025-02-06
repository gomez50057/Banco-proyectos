# models.py
from django.db import models
from django.contrib.auth.models import User
import os


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
    nombre_proyecto = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    tipo_proyecto = models.CharField(max_length=255)
    tipo_entidad = models.CharField(max_length=255)
    dependencia = models.CharField(max_length=255, null=True, blank=True)
    organismo = models.CharField(max_length=255, null=True, blank=True)
    municipio_ayuntamiento = models.CharField(max_length=255, null=True, blank=True)
    unidad_responsable = models.CharField(max_length=255)
    unidad_presupuestal = models.CharField(max_length=255)
    inversion_federal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    inversion_estatal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    inversion_municipal = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    inversion_otros = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    inversion_total = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True)
    ramo_presupuestal = models.CharField(max_length=255)
    descripcion = models.TextField()
    situacion_sin_proyecto = models.TextField()
    objetivos = models.TextField()
    metas = models.TextField()
    gasto_programable = models.CharField(max_length=255)
    tiempo_ejecucion = models.IntegerField(null=True, blank=True)
    modalidad_ejecucion = models.CharField(max_length=255)
    programa_presupuestario = models.CharField(max_length=255)
    beneficiarios = models.IntegerField(null=True, blank=True)
    normativa_aplicable = models.TextField()
    region = models.JSONField()
    municipio = models.JSONField()
    localidad = models.CharField(max_length=255)
    barrio_colonia = models.CharField(max_length=255)
    tipo_localidad = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    plan_nacional = models.CharField(max_length=255)
    plan_estatal = models.CharField(max_length=255)
    plan_municipal = models.TextField(null=True, blank=True)
    acuerdos_transversales= models.CharField(max_length=255, null=True, blank=True)
    ods = models.CharField(max_length=255)
    programas_SIE = models.CharField(max_length=255)
    indicadores_estrategicos = models.CharField(max_length=255)
    indicadores_socioeconomicos = models.CharField(max_length=255)
    
    situacion_actual = models.ImageField(upload_to='documentos/situacion_actual/', null=True, blank=True)
    expediente_tecnico = models.FileField(upload_to='documentos/expediente_tecnico/', null=True, blank=True)
    estudios_factibilidad = models.FileField(upload_to='documentos/estudios_factibilidad/', null=True, blank=True)
    analisis_alternativas = models.FileField(upload_to='documentos/analisis_alternativas/', null=True, blank=True)
    validacion_normativa = models.FileField(upload_to='documentos/validacion_normativa/', null=True, blank=True)
    liberacion_derecho_via = models.FileField(upload_to='documentos/liberacion_derecho_via/', null=True, blank=True)
    analisis_costo_beneficio = models.FileField(upload_to='documentos/analisis_costo_beneficio/', null=True, blank=True)
    proyecto_ejecutivo = models.FileField(upload_to='documentos/proyecto_ejecutivo/', null=True, blank=True)
    manifestacion_impacto_ambiental = models.FileField(upload_to='documentos/manifestacion_impacto_ambiental/', null=True, blank=True)
    render = models.FileField(upload_to='documentos/render/', null=True, blank=True)
    otros_estudios = models.FileField(upload_to='documentos/otros_estudios/', null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)
    porcentaje_avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    estatus = models.CharField(max_length=50, choices=[('Atendido', 'Atendido'), ('En Proceso', 'En Proceso'), ('Registrado', 'Registrado')], default='Registrado')
    situacion = models.CharField(max_length=50, choices=[('Vigente', 'Vigente'), ('Antecedente', 'Antecedente'), ('Cancelado', 'Cancelado')], default='Vigente')
    retroalimentacion = models.TextField(null=True, blank=True)

    # Campos de bloqueo
    isBlocked_project = models.BooleanField(default=True)
    isBlocked_nombre_proyecto = models.BooleanField(default=False)
    isBlocked_sector = models.BooleanField(default=False)
    isBlocked_tipo_proyecto = models.BooleanField(default=False)
    isBlocked_tipo_entidad = models.BooleanField(default=False)
    isBlocked_dependencia = models.BooleanField(default=False)
    isBlocked_organismo = models.BooleanField(default=False)
    isBlocked_municipio_ayuntamiento = models.BooleanField(default=False)
    isBlocked_unidad_responsable = models.BooleanField(default=False)
    isBlocked_unidad_presupuestal = models.BooleanField(default=False)
    isBlocked_inversion_federal = models.BooleanField(default=False)
    isBlocked_inversion_estatal = models.BooleanField(default=False)
    isBlocked_inversion_municipal = models.BooleanField(default=False)
    isBlocked_inversion_otros = models.BooleanField(default=False)
    isBlocked_inversion_total = models.BooleanField(default=False)
    isBlocked_ramo_presupuestal = models.BooleanField(default=False)
    isBlocked_descripcion = models.BooleanField(default=False)
    isBlocked_situacion_sin_proyecto = models.BooleanField(default=False)
    isBlocked_objetivos = models.BooleanField(default=False)
    isBlocked_metas = models.BooleanField(default=False)
    isBlocked_gasto_programable = models.BooleanField(default=False)
    isBlocked_tiempo_ejecucion = models.BooleanField(default=False)
    isBlocked_modalidad_ejecucion = models.BooleanField(default=False)
    isBlocked_programa_presupuestario = models.BooleanField(default=False)
    isBlocked_beneficiarios = models.BooleanField(default=False)
    isBlocked_normativa_aplicable = models.BooleanField(default=False)
    isBlocked_region = models.BooleanField(default=False)
    isBlocked_municipio = models.BooleanField(default=False)
    isBlocked_localidad = models.BooleanField(default=False)
    isBlocked_barrio_colonia = models.BooleanField(default=False)
    isBlocked_tipo_localidad = models.BooleanField(default=False)
    isBlocked_latitud = models.BooleanField(default=False)
    isBlocked_longitud = models.BooleanField(default=False)
    isBlocked_plan_nacional = models.BooleanField(default=False)
    isBlocked_plan_estatal = models.BooleanField(default=False)
    isBlocked_plan_municipal = models.BooleanField(default=False)
    isBlocked_acuerdos_transversales = models.BooleanField(default=False)
    isBlocked_ods = models.BooleanField(default=False)
    isBlocked_programas_SIE = models.BooleanField(default=False)
    isBlocked_indicadores_estrategicos = models.BooleanField(default=False)
    isBlocked_indicadores_socioeconomicos = models.BooleanField(default=False)


    isBlocked_situacion_actual = models.BooleanField(default=False)
    isBlocked_expediente_tecnico = models.BooleanField(default=False)
    isBlocked_estudios_factibilidad = models.BooleanField(default=False)
    isBlocked_analisis_alternativas = models.BooleanField(default=False)
    isBlocked_validacion_normativa = models.BooleanField(default=False)
    isBlocked_liberacion_derecho_via = models.BooleanField(default=False)
    isBlocked_analisis_costo_beneficio = models.BooleanField(default=False)
    isBlocked_proyecto_ejecutivo = models.BooleanField(default=False)
    isBlocked_manifestacion_impacto_ambiental = models.BooleanField(default=False)
    isBlocked_render = models.BooleanField(default=False)
    isBlocked_otros_estudios = models.BooleanField(default=False)
    
    isBlocked_observaciones = models.BooleanField(default=False)
    isBlocked_porcentaje_avance = models.BooleanField(default=False)
    isBlocked_estatus = models.BooleanField(default=False)
    isBlocked_situacion = models.BooleanField(default=False)
    isBlocked_retroalimentacion = models.BooleanField(default=False)

    # Campos de observación
    observacion_nombre_proyecto = models.TextField(null=True, blank=True)
    observacion_sector = models.TextField(null=True, blank=True)
    observacion_tipo_proyecto = models.TextField(null=True, blank=True)
    observacion_tipo_entidad = models.TextField(null=True, blank=True)
    observacion_dependencia = models.TextField(null=True, blank=True)
    observacion_organismo = models.TextField(null=True, blank=True)
    observacion_municipio_ayuntamiento = models.TextField(null=True, blank=True)
    observacion_unidad_responsable = models.TextField(null=True, blank=True)
    observacion_unidad_presupuestal = models.TextField(null=True, blank=True)
    observacion_inversion_federal = models.TextField(null=True, blank=True)
    observacion_inversion_estatal = models.TextField(null=True, blank=True)
    observacion_inversion_municipal = models.TextField(null=True, blank=True)
    observacion_inversion_otros = models.TextField(null=True, blank=True)
    observacion_inversion_total = models.TextField(null=True, blank=True)
    observacion_ramo_presupuestal = models.TextField(null=True, blank=True)
    observacion_descripcion = models.TextField(null=True, blank=True)
    observacion_situacion_sin_proyecto = models.TextField(null=True, blank=True)
    observacion_objetivos = models.TextField(null=True, blank=True)
    observacion_metas = models.TextField(null=True, blank=True)
    observacion_gasto_programable = models.TextField(null=True, blank=True)
    observacion_tiempo_ejecucion = models.BooleanField(default=False)
    observacion_modalidad_ejecucion = models.TextField(null=True, blank=True)
    observacion_programa_presupuestario = models.TextField(null=True, blank=True)
    observacion_beneficiarios = models.TextField(null=True, blank=True)
    observacion_normativa_aplicable = models.TextField(null=True, blank=True)
    observacion_region = models.TextField(null=True, blank=True)
    observacion_municipio = models.TextField(null=True, blank=True)
    observacion_localidad = models.TextField(null=True, blank=True)
    observacion_barrio_colonia = models.TextField(null=True, blank=True)
    observacion_tipo_localidad = models.TextField(null=True, blank=True)
    observacion_latitud = models.TextField(null=True, blank=True)
    observacion_longitud = models.TextField(null=True, blank=True)
    observacion_plan_nacional = models.TextField(null=True, blank=True)
    observacion_plan_estatal = models.TextField(null=True, blank=True)
    observacion_plan_municipal = models.TextField(null=True, blank=True)
    observacion_acuerdos_transversales = models.TextField(null=True, blank=True)
    observacion_ods = models.TextField(null=True, blank=True)
    observacion_programas_SIE = models.TextField(null=True, blank=True)
    observacion_indicadores_estrategicos = models.TextField(null=True, blank=True)
    observacion_indicadores_socioeconomicos = models.TextField(null=True, blank=True)
    observacion_situacion_actual = models.TextField(null=True, blank=True)
    observacion_expediente_tecnico = models.TextField(null=True, blank=True)
    observacion_estudios_factibilidad = models.TextField(null=True, blank=True)
    observacion_analisis_alternativas = models.TextField(null=True, blank=True)
    observacion_validacion_normativa = models.TextField(null=True, blank=True)
    observacion_liberacion_derecho_via = models.TextField(null=True, blank=True)
    observacion_analisis_costo_beneficio = models.TextField(null=True, blank=True)
    observacion_proyecto_ejecutivo = models.TextField(null=True, blank=True)
    observacion_manifestacion_impacto_ambiental = models.TextField(null=True, blank=True)
    observacion_render = models.TextField(null=True, blank=True)
    observacion_otros_estudios = models.TextField(null=True, blank=True)
    
    observacion_observaciones = models.TextField(null=True, blank=True)
    observacion_porcentaje_avance = models.TextField(null=True, blank=True)
    observacion_estatus = models.TextField(null=True, blank=True)
    observacion_situacion = models.TextField(null=True, blank=True)
    observacion_retroalimentacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre_proyecto

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
