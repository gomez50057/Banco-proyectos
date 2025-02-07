# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FormProject, CedulaRegistro, AnexoProyecto, Document


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

# class FormProjectSerializer(serializers.ModelSerializer):
#     user = UserRelatedField(queryset=User.objects.all())

#     class Meta:
#         model = FormProject
#         fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'project', 'document_type', 'file', 'uploaded_at']


class FormProjectSerializer(serializers.ModelSerializer):
    expediente_tecnico = serializers.SerializerMethodField()
    estudios_factibilidad = serializers.SerializerMethodField()
    analisis_alternativas = serializers.SerializerMethodField()
    validacion_normativa = serializers.SerializerMethodField()
    liberacion_derecho_via = serializers.SerializerMethodField()
    analisis_costo_beneficio = serializers.SerializerMethodField()
    proyecto_ejecutivo = serializers.SerializerMethodField()
    manifestacion_impacto_ambiental = serializers.SerializerMethodField()
    render = serializers.SerializerMethodField()
    otros_estudios = serializers.SerializerMethodField()
    
    user = UserRelatedField(queryset=User.objects.all())

    class Meta:
        model = FormProject
        # Se incluyen todos los campos del proyecto (excepto los que se removieron)
        fields = '__all__'
    
    def get_expediente_tecnico(self, obj):
        documents = obj.documents.filter(document_type='expediente_tecnico')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_estudios_factibilidad(self, obj):
        documents = obj.documents.filter(document_type='estudios_factibilidad')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_analisis_alternativas(self, obj):
        documents = obj.documents.filter(document_type='analisis_alternativas')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_validacion_normativa(self, obj):
        documents = obj.documents.filter(document_type='validacion_normativa')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_liberacion_derecho_via(self, obj):
        documents = obj.documents.filter(document_type='liberacion_derecho_via')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_analisis_costo_beneficio(self, obj):
        documents = obj.documents.filter(document_type='analisis_costo_beneficio')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_proyecto_ejecutivo(self, obj):
        documents = obj.documents.filter(document_type='proyecto_ejecutivo')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_manifestacion_impacto_ambiental(self, obj):
        documents = obj.documents.filter(document_type='manifestacion_impacto_ambiental')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_render(self, obj):
        documents = obj.documents.filter(document_type='render')
        return DocumentSerializer(documents, many=True, context=self.context).data

    def get_otros_estudios(self, obj):
        documents = obj.documents.filter(document_type='otros_estudios')
        return DocumentSerializer(documents, many=True, context=self.context).data

class BulkCreateProjectSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects.all())

    class Meta:
        model = FormProject
        fields = '__all__'
        extra_kwargs = {
            'latitud': {'required': False, 'allow_null': True},
            'longitud': {'required': False, 'allow_null': True},
        }

class AnexoProyectoSerializer(serializers.ModelSerializer):
    # Si quieres incluir campos adicionales de la cédula asociada
    projInvestment_id = serializers.CharField(source='cedula.projInvestment_id', read_only=True)
    
    class Meta:
        model = AnexoProyecto
        # fields = ['projInvestment_id', 'tipo_anexo', 'archivo', 'descripcion']
        fields = '__all__'


class CedulaRegistroSerializer(serializers.ModelSerializer):
    anexos = AnexoProyectoSerializer(many=True, required=False)  # Mantiene los anexos
    username = serializers.CharField(source='user.username', read_only=True)  # Añade el username del usuario

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