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

class UserRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            user = User.objects.get(username=data)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError(f'No se encontró un usuario con el nombre {data}')

class FormProjectSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects.all())

    class Meta:
        model = FormProject
        fields = '__all__'

class BulkCreateProjectSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects.all())

    class Meta:
        model = FormProject
        fields = '__all__'
        extra_kwargs = {
            'latitud': {'required': False, 'allow_null': True},
            'longitud': {'required': False, 'allow_null': True},
        }

from .models import CedulaRegistro, AnexoProyecto

class AnexoProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoProyecto
        fields = ['id', 'nombre_anexo', 'archivo', 'descripcion']

class CedulaRegistroSerializer(serializers.ModelSerializer):
    anexos = AnexoProyectoSerializer(many=True, required=False)

    class Meta:
        model = CedulaRegistro
        fields = '__all__'

    def create(self, validated_data):
        anexos_data = validated_data.pop('anexos', [])
        cedula = CedulaRegistro.objects.create(**validated_data)
        for anexo_data in anexos_data:
            AnexoProyecto.objects.create(cedula=cedula, **anexo_data)
        return cedula

    def update(self, instance, validated_data):
        anexos_data = validated_data.pop('anexos', [])
        instance = super().update(instance, validated_data)
        for anexo_data in anexos_data:
            AnexoProyecto.objects.create(cedula=instance, **anexo_data)
        return instance