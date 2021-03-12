from rest_framework import serializers

from .models import OrdenTrabajo, SolicitudTrabajo, \
    DetalleSolicitud, SolicitudesImagenes, \
    OrdenesImagenes, SolicitudRubros, Facturas, \
    DetallesFacturas
from ctg.models import ItemsImagenes
from usr.models import Usuarios
from clt.models import Clientes


class OrdenesSerializer(serializers.ModelSerializer):

    estado_nombre = serializers.CharField(source='estado.descripcion')
    solicita = serializers.SerializerMethodField()
    colorestado = serializers.SerializerMethodField()
    usuario_aprueba_pago = serializers.SerializerMethodField()
    usuario_registra_facturacion = serializers.SerializerMethodField()
    usuario_registra_pago_orden = serializers.SerializerMethodField()
    # usuario_registra_revision_orden = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        fields = ('fecha_creacion', 'usuario_crea', 'secuencia', 'colorestado',
                  'id_orden', 'estado', 'estado_nombre', 'solicita',
                  'pago_aprobado', 'fecha_recibe_prod', 'fecha_aprueba_pago',
                  'usuario_aprueba_pago', 'orden_facturada',
                  'fecha_facturacion', 'usuario_registra_facturacion',
                  'orden_pagada', 'fecha_pago', 'usuario_registra_pago_orden',
                  'numero_factura'
                  )
        # fields = '__all__'

    def get_solicita(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_crea).first()
        return str(usuario)

    def get_usuario_aprueba_pago(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_aprueba_pago).first()
        return str(usuario)

    def get_usuario_registra_facturacion(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_registra_factura).first()
        return str(usuario)

    def get_usuario_registra_pago_orden(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_registra_pago).first()
        return str(usuario)

    # def get_usuario_registra_revision_orden(self, obj):
    #     usuario = Usuarios.objects.only('username').\
    #         filter(id=obj.usuario_registra_revision).first()
    #     return str(usuario)

    def get_colorestado(self, obj):
        estado = str(obj.estado)
        colores = {
            'INGRESADO': '#87CEFA',
            'PENDIENTE INICIO': '#f0ad4e',
            'TRABAJO TERMINADO': '#008B8B',
            'EN PROCESO': '#f0ad4e',
            'MATERIAL ENVIADO': '#000080',
            'CANCELADO': '#d9534f',
            'FINALIZADO': '#32CD32',
            'PRODUCTO ENVIADO': '#FF00FF',
            'PRODUCTO RECIBIDO': '#8B008B',
        }
        color = colores.get(estado, '#000000')
        return str(color)


class OrdenDetallesSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source='estado.descripcion')
    cliente_nombre = serializers.SerializerMethodField()
    solicita = serializers.SerializerMethodField()
    origen_descripcion = serializers.\
        CharField(source='origen_material.descripcion')
    colorestado = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        fields = '__all__'
        extra_fields = ['estado_nombre']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(OrdenDetallesSerializer, self).\
            get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_solicita(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_crea).first()
        return str(usuario)

    def get_cliente_nombre(self, obj):
        cliente = Clientes.objects.\
            filter(id_cliente=obj.cliente_id).first()
        return str(cliente.nombres + ' ' + cliente.apellidos)

    def get_colorestado(self, obj):
        estado = str(obj.estado)
        colores = {
            'INGRESADO': '#87CEFA',
            'PENDIENTE INICIO': '#f0ad4e',
            'TRABAJO TERMINADO': '#008B8B',
            'EN PROCESO': '#f0ad4e',
            'MATERIAL ENVIADO': '#000080',
            'CANCELADO': '#d9534f',
            'FINALIZADO': '#32CD32',
            'PRODUCTO ENVIADO': '#FF00FF',
            'PRODUCTO RECIBIDO': '#8B008B',
        }
        color = colores.get(estado, '#000000')
        return str(color)


class OrdenImagenesSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenesImagenes
        fields = '__all__'


class SolicitudesSerializer(serializers.ModelSerializer):

    estado_nombre = serializers.CharField(source='estado.descripcion')
    solicita = serializers.SerializerMethodField()
    colorestado = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudTrabajo
        fields = ('fecha_creacion', 'usuario_crea', 'secuencia', 'colorestado',
                  'id_solicitud', 'estado', 'estado_nombre',
                  'detalle', 'solicita')
        # fields = '__all__'

    def get_solicita(self, obj):
        usuario = Usuarios.objects.only('username').\
            filter(id=obj.usuario_crea).first()
        return str(usuario)

    def get_colorestado(self, obj):
        estado = str(obj.estado)
        colores = {
            'ESPERA COTIZACION TALLER': '#87CEFA',
            'ESPERA DE EVALUACION': '#f0ad4e',
            'COTIZADO TALLER': '#008B8B',
            'SOLICITADO A EXTERNO': '#f0ad4e',
            'RECHAZADO TALLER': '#d9534f',
            'RECHAZADO CLIENTE': '#d9534f',
            'GENERADO CON EXTERNO': '#FF00FF',
            'GENERADO CON TALLER': '#32CD32',
        }
        color = colores.get(estado, '#000000')
        return str(color)


class DetallesSolicitudSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleSolicitud
        fields = '__all__'


class SolicitudImagenesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitudesImagenes
        fields = '__all__'


class SolicitudRubrosSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitudRubros
        fields = '__all__'


class SolicitarAExternoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitudTrabajo
        fields = ['detalle']


class EnvioMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['comp_envio_op', 'gramos_enviados']


class RecibirMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['gramos_recibidos']


class AnularOrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['obs_recepcion_mat']


class FinalizarTrabajoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = [
            'peso_final']


class EnviarProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = [
            'comp_envio_ta',
            'costo_envio']


class RecibirProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['estado']


class CargarDocTallerSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['factura_taller']


class CargarDocOpSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = [
            'cta_por_pagar',
            'orden_compra'
        ]


class DevolverProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = ['obs_recepcion_prod']


class FinalizarOrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = [
            'obs_venta',
            'factura_vta'
        ]


class FinalizarSinVentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenTrabajo
        fields = [
            'obs_venta'
        ]


class GenerarOrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitudTrabajo
        fields = [
            'peso_solicitado',
            'peso_materia_dividida',
            'peso_cliente_dividido',
            'origen_material_dividido',
            'costo_gramo_base_taller',
            'precio_gramo_base_taller',
            'prct_utilidad_base_taller',
            'utilidad_base_taller',
            'costo_base_total_ta',
            'precio_base_total_ta',
            'costo_fabricacion_unitario',
            'precio_fabricacion_unitario',
            'costo_total_fabricacion_ta',
            'precio_fabricacion_total',
            'prct_util_sobre_fabrica_ta',
            'util_sobre_fabrica_ta',
            'total_rubros',
            'subtotal_taller',
            'prct_impuestos_ta',
            'impuestos_taller',
            'total_taller',
            'costo_gramo_base_op',
            'precio_gramo_base_op',
            'prct_util_sobre_base_op',
            'costo_base_total_op',
            'precio_base_total_op',
            'util_sobre_base_op',
            'prct_util_sobre_fabrica_op',
            'util_sobre_fabrica_op',
            'precio_unitario_op',
            'precio_fabricacion_total_op',
            'subtotal_solicitud',
            'prct_impuestos_op',
            'impuestos_op',
            'descuento_solicitud',
            'precio_sistema',
            'precio_final_venta'
        ]


class FacturasSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source='estado.descripcion')
    taller_nombre = serializers.CharField(source='taller.nombre')
    taller_logo = serializers.ImageField(source='taller.logotipo')

    class Meta:
        model = Facturas
        fields = '__all__'
        extra_fields = [
            'estado_nombre',
            'taller_nombre'
        ]

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(FacturasSerializer, self).\
            get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class DetallesFacturasSerializer(serializers.ModelSerializer):
    orden_secuencia = serializers.CharField(source='orden.secuencia')
    solicita = serializers.CharField(source='orden.tienda.nombre')
    subtotal_orden = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        source='orden.subtotal_taller'
    )
    impuestos_orden = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        source='orden.impuestos_taller'
    )
    total_orden = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        source='orden.total_taller'
    )
    costo_envio = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        source='orden.costo_envio'
    )

    class Meta:
        model = DetallesFacturas
        fields = (
            'orden_id',
            'orden_secuencia',
            'solicita',
            'subtotal_orden',
            'impuestos_orden',
            'total_orden',
            'costo_envio'
        )
