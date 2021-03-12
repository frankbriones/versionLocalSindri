from rest_framework import serializers

from .models import Tiendas


class TiendasSerializer(serializers.ModelSerializer):
    sociedad_nombre = serializers.CharField(source='sociedad.nombre')

    class Meta:
        model = Tiendas
        fields = (
            'id_tienda',
            'codigo',
            'nombre',
            'sociedad_id',
            'sociedad_nombre'
            )
