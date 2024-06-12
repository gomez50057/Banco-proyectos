# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, ProyectoDependencia, Project

class UsuarioSerializer(serializers.ModelSerializer):
    tipo_cuenta = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'tipo_cuenta']

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'tipo_cuenta']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProyectoDependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoDependencia
        fields = ['projectName', 'description', 'file']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
