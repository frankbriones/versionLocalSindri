from rest_framework import serializers

from trn.models import OrdenTrabajo, SolicitudTrabajo
from usr.models import Usuarios


class OrdenesSerializer(serializers.ModelSerializer):

    # estado_nombre = serializers.CharField(source='estado.descripcion')
    dcount = serializers.IntegerField(read_only=True)
    # solicita = serializers.SerializerMethodField()
    # colorestado = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        # fields = ('fecha_creacion', 'usuario_crea', 'secuencia', 'colorestado',
        #           'id_orden', 'estado', 'estado_nombre', 'solicita')
        fields = ('estado', 'dcount')
        # fields = '__all__'

    # def get_solicita(self, obj):
    #     usuario = Usuarios.objects.only('username').\
    #         filter(id=obj.usuario_crea).first()
    #     return str(usuario)

    # def get_colorestado(self, obj):
    #     estado = str(obj.estado)
    #     colores = {
    #         'INGRESADO': '#b9b9b9',
    #         'PENDIENTE INICIO': '#ffc100',
    #         'TRABAJO TERMINADO': '#00e703'
    #     }
    #     color = colores.get(estado, '#000000')
    #     return str(color)
