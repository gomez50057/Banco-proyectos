# En models.py

from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_cuenta = models.CharField(max_length=20, choices=[("ciudadano", "Ciudadano"), ("dependencia", "Dependencia"), ("municipio", "Municipio")])

    class Meta:
        app_label = 'banco_pro'  # Agrega esta línea para especificar la aplicación

    def __str__(self):
        return self.usuario.username


class ProyectoDependencia(models.Model):
    projectName = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')  # Donde 'uploads/' es la carpeta donde se guardarán los archivos

    def __str__(self):
        return self.projectName
    


from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    tipo_proyecto = models.CharField(max_length=255)
    dependencia = models.CharField(max_length=255, null=True, blank=True)
    organismo = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    peticion_personal = models.CharField(max_length=255, null=True, blank=True)
    monto_federal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_estatal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_municipal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_otros = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField()
    situacion_sin_proyecto = models.TextField()
    objetivos = models.TextField()
    metas = models.TextField()
    programa_presupuestario = models.CharField(max_length=255)
    beneficiarios = models.IntegerField(null=True, blank=True)
    alineacion_normativa = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    plan_nacional = models.CharField(max_length=255)
    plan_estatal = models.CharField(max_length=255)
    plan_municipal = models.CharField(max_length=255, null=True, blank=True)
    ods = models.CharField(max_length=255)
    plan_sectorial = models.CharField(max_length=255)
    unidad_responsable = models.CharField(max_length=255)
    unidad_presupuestal = models.CharField(max_length=255)
    ramo_presupuestal = models.CharField(max_length=255)
    observaciones = models.TextField(null=True, blank=True)
    gasto_programable = models.CharField(max_length=255)
    indicadores_estrategicos = models.CharField(max_length=255)
    indicadores_tacticos = models.CharField(max_length=255)
    indicadores_desempeno = models.TextField()
    indicadores_rentabilidad = models.TextField()
    estado_inicial = models.ImageField(upload_to='estado_inicial/', null=True, blank=True)
    estado_con_proyecto = models.ImageField(upload_to='estado_con_proyecto/', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Establece la fecha de registro automáticamente

    def __str__(self):
        return self.project_name
