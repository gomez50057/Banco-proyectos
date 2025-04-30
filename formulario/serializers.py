from rest_framework import serializers
from .models import NivelacionTierra, ArchivoPDF

class NivelacionTierraSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = NivelacionTierra
        fields = '__all__'

# class ArchivoPDFSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArchivoPDF
#         fields = '__all__'


class ArchivoPDFSerializer(serializers.ModelSerializer):
    # Definimos el campo como CharField para recibir el folio literal
    nivelacion = serializers.CharField()

    class Meta:
        model = ArchivoPDF
        fields = '__all__'

    def to_internal_value(self, data):
        # Obtiene los valores internos mediante la implementación por defecto
        internal_data = super().to_internal_value(data)
        # Obtiene el folio literal enviado
        folio_literal = data.get('nivelacion')
        try:
            # Busca la instancia de NivelacionTierra que tiene ese folio
            nivelacion_instance = NivelacionTierra.objects.get(folio=folio_literal)
        except NivelacionTierra.DoesNotExist:
            raise serializers.ValidationError({
                'nivelacion': f'No se encontró una Nivelación con folio "{folio_literal}".'
            })
        # Asigna la instancia obtenida al campo interno
        internal_data['nivelacion'] = nivelacion_instance
        return internal_data