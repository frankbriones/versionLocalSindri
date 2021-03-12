from rest_framework import serializers

from .models import Notificaciones


class NotificacionesSerializer(serializers.ModelSerializer):

    estado_nombre = serializers.CharField(source='estado.descripcion')
    usuario_nombre = serializers.CharField(source='usuario_genera.username')
    taller_nombre = serializers.CharField(source='taller.nombre')
    tienda_nombre = serializers.CharField(source='tienda.nombre')


    class Meta:
        model = Notificaciones
        fields = (
            'id_notificacion',
            'nombre_producto',
            'vista',
            'principal',
            'postergada',
            'id_transaccion',
            'tipo_transaccion',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_genera',
            'estado',
            'taller',
            'tienda_nombre',
            'tienda',
            'estado_nombre',
            'usuario_nombre',
            'taller_nombre',
            'tipo_notificacion'
        )
