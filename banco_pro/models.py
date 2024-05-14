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

# class Project(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class ProyectoDependencia(models.Model):
    projectName = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')  # Donde 'uploads/' es la carpeta donde se guardarán los archivos

    def __str__(self):
        return self.projectName
    

