# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FormProject


class UsuarioSerializer(serializers.ModelSerializer):
    tipo_cuenta = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FormProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormProject
        fields = '__all__'  # Incluye todos los campos del modelo
