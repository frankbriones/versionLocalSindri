from datetime import datetime

from django.db.models import Count, Max, Min, Sum, F, Q, When, Subquery


from import_export import resources
from import_export.fields import Field
from .models import OrdenTrabajo, SolicitudTrabajo, DetalleSolicitud, SolicitudesPiedras, DetalleOrden
from est.models import Tiendas
from usr.models import Usuarios, UsuariosTiendas
from ctg.models import Items, Categorias, DetalleItems, PiezasDetalles, Piezas


class OrdenesResource(resources.ModelResource):
    secuencia = Field(
        attribute='secuencia',
        column_name='Número de orden'
    )
    codigo_tienda = Field(
        column_name='Código tienda'
    )
    nombre_tienda = Field(
        column_name='Nombre tienda'
    )
    fabricante = Field(
        column_name='Fabricante'
    )
    tipo_catalogo = Field(
        attribute='categoria__division__tipo_catalogo__descripcion',
        column_name='Tipo orden'
    )
    categoria = Field(
        attribute='categoria__descripcion',
        column_name='Categoría'
    )
    origen_material__descripcion = Field(
        attribute='origen_material__descripcion',
        column_name='Origen de material'
    )
    peso_final = Field(
        attribute='peso_final',
        column_name='Peso final de la órden'
    )
    pago_aprobado = Field(
        column_name='Estado de pago'
    )
    subtotal_envio = Field(
        column_name='Subtotal envío'
    )
    subtotal_taller = Field(
        attribute='subtotal_taller',
        column_name='Subtotal fabricación'
    )
    subtotal_acumulado = Field(
        column_name='Subtotales fabricacion y envio'
    )

    impuestos_taller = Field(
        attribute='impuestos_taller',
        column_name='Impuestos Fabricacion'
    )

    impuesto_envio = Field(
        column_name='Impuestos de envio'
    )

    impuesto_acumulado = Field(
        column_name='Impuestos fabricacion y envio'
    )

    costo_envio = Field(
        attribute='costo_envio',
        column_name='Costo Envio'
    )
    total_taller = Field(
        attribute='total_taller',
        column_name='Costo fabricación'
    )
    total_pagar = Field(
        column_name='Total a pagar'
    )
    numero_factura = Field(
        attribute='numero_factura',
        column_name='Número de factura'
    )
    fecha_aprueba_pago = Field(
        attribute='fecha_aprueba_pago',
        column_name='Fecha aprobación'
    )
    fecha_pago = Field(
        attribute='fecha_pago',
        column_name='Fecha pago'
    )
    fecha_facturacion = Field(
        attribute='fecha_facturacion',
        column_name='Fecha facturación'
    )



    class Meta:
        model = OrdenTrabajo
        fields = (
            'secuencia', 'precio_adicionales',
            'fabricante', 'origen_material__descripcion',
            'sku', 'peso_final', 'costo_envio', 'pago_aprobado', 'total_taller',
            'precio_piedras', 'fecha_aprueba_pago',
            'nombre_tienda', 'numero_factura', 'subtotal_envio',
            'fecha_facturacion', 'fecha_pago'

        )

    def dehydrate_fabricante(self, OrdenTrabajo):
        if OrdenTrabajo.externa:
            return OrdenTrabajo.proveedor.nombres + \
                ' ' + OrdenTrabajo.proveedor.apellidos
        else:
            return OrdenTrabajo.taller.nombre

    def dehydrate_pago_aprobado(self, OrdenTrabajo):
        if OrdenTrabajo.orden_pagada:
            return 'PAGADO'
        elif OrdenTrabajo.orden_facturada:
            return 'FACTURADO'
        elif OrdenTrabajo.pago_aprobado:
            return 'APROBADO'
        else:
            return 'PENDIENTE'

    def dehydrate_total_pagar(self, OrdenTrabajo):
        costo_envio = OrdenTrabajo.costo_envio
        total_taller = OrdenTrabajo.total_taller
        total_pagar = total_taller + costo_envio
        return round((total_pagar), 2)

    def dehydrate_nombre_tienda(self, OrdenTrabajo):
        return OrdenTrabajo.tienda.nombre

    def dehydrate_codigo_tienda(self, OrdenTrabajo):
        return OrdenTrabajo.tienda.codigo

    def dehydrate_subtotal_envio(self, OrdenTrabajo):
        prct_impuestos = float(OrdenTrabajo.prct_impuestos_ta)
        if OrdenTrabajo.costo_envio:
            costo_envio = float(OrdenTrabajo.costo_envio)
        else:
            costo_envio = 0
        return round((costo_envio / (1+(prct_impuestos/100))), 2)


    def dehydrate_impuesto_envio(self, OrdenTrabajo):
        prct_impuestos = float(OrdenTrabajo.prct_impuestos_ta)
        if OrdenTrabajo.costo_envio:
            costo_envio = float(OrdenTrabajo.costo_envio)
        else:
            costo_envio = 0
        subtotal_envio = round((costo_envio / (1+(prct_impuestos/100))), 2)
        impuesto_envio = float(costo_envio) - float(subtotal_envio)
        return impuesto_envio

    def dehydrate_impuesto_acumulado(self, OrdenTrabajo):
        prct_impuestos = float(OrdenTrabajo.prct_impuestos_ta)
        if OrdenTrabajo.costo_envio:
            costo_envio = float(OrdenTrabajo.costo_envio)
        else:
            costo_envio = 0
        subtotal_envio = round((costo_envio / (1+(prct_impuestos/100))), 2)
        impuesto_envio = float(costo_envio) - float(subtotal_envio)

        impuesto_fabricacion = float(OrdenTrabajo.impuestos_taller)
        return (impuesto_fabricacion + impuesto_envio)

    def dehydrate_subtotal_acumulado(self, OrdenTrabajo):
        prct_impuestos = float(OrdenTrabajo.prct_impuestos_ta)
        if OrdenTrabajo.costo_envio:
            costo_envio = float(OrdenTrabajo.costo_envio)
        else:
            costo_envio = 0
        subtotal_envio = round((costo_envio / (1+(prct_impuestos/100))), 2)
        subtotal_taller = float(OrdenTrabajo.subtotal_taller)
        return float(subtotal_taller + subtotal_envio)



        




    


class OrdenesListaResource(resources.ModelResource):
    secuencia = Field(
        attribute='secuencia',
        column_name='Número de orden'
    )
    estado__descripcion = Field(
        attribute='estado__descripcion',
        column_name='Estado'
    )
    nombre_tienda = Field(
        attribute='tienda__nombre',
        column_name='Nombre tienda'
    )
    codigo = Field(
        column_name="Codigo tienda"
        )

    taller__nombre = Field(
        attribute='taller__nombre',
        column_name='Fabricante'
    )

    clasificacion_item = Field(
        column_name="Clasificacion Item"
    )

    sku = Field(
        column_name='SKU'
    )

    item = Field(
        column_name='Item'
    )
    color = Field(
        attribute="color__descripcion",
        column_name="Color"
    )

    categoria = Field(
        attribute='categoria__descripcion',
        column_name='Categoria'
    )

    tipo_catalogo = Field(
        column_name='Tipo Item'
    )
    # talla, color, acabado
    talla = Field(
        column_name='Talla/Longitud'
    )

    acabado = Field(
        column_name='Acabado'
    )

    parte_interna = Field(
        column_name='Parte Interna'
    )


    origen_material__descripcion = Field(
        attribute='origen_material__descripcion',
        column_name='Origen de material'
    )

    costo_envio = Field(
        attribute='costo_envio',
        column_name='Costo del Envio'
    )


    subtotal_taller = Field(
        attribute='subtotal_taller',
        column_name='Subtotal fabricación'
    )
    impuestos_taller = Field(
        attribute='impuestos_taller',
        column_name='Impuestos'
    )
    total_taller = Field(
        attribute='total_taller',
        column_name='Costo total fabricación'
    )
    costo_total_fabricacion_ta = Field(
        attribute="costo_total_fabricacion_ta",
        column_name="Costo Total Fabricacion Taller"
        )

    precio_fabricacion_total = Field(
        attribute="precio_fabricacion_total",
        column_name="Precio Fabricacion Total"
        )

    util_sobre_fabrica_ta = Field(
        attribute="util_sobre_fabrica_ta",
        column_name="Utilidad sobre fabrica taller"
        )

    prct_util_sobre_fabrica_ta = Field(
        attribute="prct_util_sobre_fabrica_ta",
        column_name="Prct Utili. fabricacion Taller"
        )

    peso_solicitado = Field(
        attribute='peso_solicitado',
        column_name='Peso solicitado'
    )
    gramos_enviados = Field(
        attribute='gramos_enviados',
        column_name='Gramos enviados'
    )
    gramos_recibidos = Field(
        attribute='gramos_recibidos',
        column_name='Gramos recibidos'
    )
    
    peso_final = Field(
        attribute='peso_final',
        column_name='Peso final de órden'
    )
    diferencia_gramos = Field(
        attribute='diferencia_gramos',
        column_name='Diferencia de gramos'
    )
    fecha_creacion = Field(
        attribute='fecha_creacion',
        column_name='Fecha de creación'
    )
    fecha_fin_trabajo = Field(
        attribute='fecha_fin_trabajo',
        column_name='Fecha fabricación'
    )
    # nuevos campos agregados
    fecha_envio_mat = Field(
        attribute='fecha_envio_mat',
        column_name='Fecha envio material'

    )

    fecha_recibe_mat = Field(
        attribute= "fecha_recibe_mat",
        column_name= "Fecha recibe material"
    )

    fecha_anulacion = Field(
        attribute="fecha_anulacion",
        column_name="Fecha anulacion"
    )

    fecha_envio_prod = Field(
        attribute="fecha_envio_prod",
        column_name="Fecha envio producto"
    )

    fecha_recibe_prod = Field(
        attribute="fecha_recibe_prod",
        column_name="Fecha recibe producto"
    )

    fecha_venta= Field(
        attribute="fecha_venta",
        column_name="Fecha venta"
        )

    fecha_aprueba_pago = Field(
        attribute="fecha_aprueba_pago",
        column_name="Fecha aprueba pago"
        )

    fecha_facturacion = Field(
        attribute="fecha_facturacion",
        column_name="Fecha facturacion"
        )

    class Meta:
        model = OrdenTrabajo
        fields = (
            'secuencia', 'nombre_tienda', 'taller__nombre',
            'origen_material__descripcion', 'sku','item',  'costo_envio', 'gramos_enviados',
            'gramos_recibidos', 'peso_solicitado',
            'peso_final', 'diferencia_gramos', 'fecha_creacion',
            'fecha_fin_trabajo', 'estado__descripcion', 'categoria', 'tipo_catalogo'
        )


    def dehydrate_diferencia_gramos(self, OrdenTrabajo):
        peso_solicitado = float(OrdenTrabajo.peso_solicitado)
        peso_final = 0
        diferencia = 0
        if OrdenTrabajo.peso_final == None:
            peso_final = float(peso_final)
        else:
            peso_final = float(OrdenTrabajo.peso_final)
            diferencia = peso_solicitado - peso_final
            diferencia = abs(diferencia)
        return diferencia

    def dehydrate_sku(self, OrdenTrabajo):
        sku = 'SKU no encontrado'

        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
        if detalle_obj:
            item_id = detalle_obj.id_item
            if not item_id:
                detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
                item_id = detalle_solicitud.item_id
            item_obj = Items.objects.filter(id_item=item_id).first()
            if item_obj :
                sku = item_obj.sku
        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle------------')
        # print(sku)
        return sku

    def dehydrate_item(self, OrdenTrabajo):
        descripcion = "item no encontrado"
        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
        if detalle_obj:
            item_id = detalle_obj.id_item
            if not item_id:
                detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
                item_id = detalle_solicitud.item_id
            item_obj = Items.objects.filter(id_item=item_id).first()
            if item_obj :
                descripcion = item_obj.descripcion
        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle/item------------')
        # print(descripcion)
        return descripcion

    def dehydrate_total_taller(self, OrdenTrabajo):
            if OrdenTrabajo.total_taller_recalculado != None:
                return OrdenTrabajo.total_taller_recalculado
            else:
                return OrdenTrabajo.total_taller
            

    def dehydrate_tipo_catalogo(self, OrdenTrabajo):
        descripcion = 'Sin tipo catalogo'
        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
        if detalle_obj:
            item_id = detalle_obj.id_item
            if not item_id:
                detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
                item_id = detalle_solicitud.item_id
            item_obj = Items.objects.filter(id_item=item_id).first()
            if item_obj :
                descripcion = item_obj.tipo_catalogo.descripcion
        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle/item------------')
        # print(descripcion)
        return descripcion


    def dehydrate_codigo(self, OrdenTrabajo):
            return OrdenTrabajo.tienda.codigo

    def dehydrate_fecha_creacion(self, OrdenTrabajo):
        formato_fecha = "%d/%m/%Y - %H:%M:%S"
        registro = (OrdenTrabajo.fecha_creacion)
        if registro != None:
            fecha_creacion = datetime.strftime(registro, formato_fecha)
        else:
            fecha_creacion = "No tenemos registro."
        return fecha_creacion

    def dehydrate_talla(self, OrdenTrabajo):
        talla = ''
        estandar = ''
        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
        if detalle_obj:
            detalle_item = DetalleItems.objects.\
                filter(id_detalle_item=detalle_obj.id_detalle_item).first()
            if detalle_item:
                talla = float(detalle_item.medida)
                estandar = detalle_item.estandar
            else:
                item = SolicitudTrabajo.objects.\
                    filter(pk=detalle_obj.id_solicitud).first()
                if item:
                    talla = item.talla.talla
                    estandar = item.talla.estandar.descripcion

        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle/item------------')
        # print(talla)

        return str('{}-{}'.format(talla, estandar))

    def dehydrate_acabado(self, OrdenTrabajo):
        acabado = ''
        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).exclude(id_solicitud=None).first()
        if detalle_obj:
            detalle_item = DetalleItems.objects.\
                filter(id_detalle_item=detalle_obj.id_detalle_item).first()
            if detalle_item:
                item = Items.objects.filter(pk=detalle_item.id_item).first()
                if item:
                    acabado = item.acabado
            else:
                detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
                if detalle_solicitud:
                    item_solicitud = Items.objects.filter(id_item=detalle_solicitud.item_id).first()
                    if item_solicitud:
                        acabado = item_solicitud.acabado
        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle/item------------')
        # print(acabado)
        return acabado

    def dehydrate_parte_interna(self, OrdenTrabajo):
        parte_interna = ''
        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).exclude(id_solicitud=None).first()
        if detalle_obj:
            detalle_item = DetalleItems.objects.\
                filter(id_detalle_item=detalle_obj.id_detalle_item).first()
            if detalle_item:
                item = Items.objects.filter(pk=detalle_item.id_item_id).first()
                if item:
                    parte_interna = item.parte_interna
            else:
                detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
                if detalle_solicitud:
                    item_solicitud = Items.objects.filter(id_item=detalle_solicitud.item_id).first()
                    if item_solicitud:
                        parte_interna = item_solicitud.parte_interna
        else:
            orden_id = OrdenTrabajo.id_orden
            # print(orden_id, '-------------orden sin detalle/item------------')
        # print(parte_interna)
        return parte_interna

    def dehydrate_clasificacion_item(self, OrdenTrabajo):

        detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
        # orden = OrdenTrabajo.objects.filter(id_orden=detalle_obj.orden_id).first()
        categoria  = Categorias.objects.filter(id_categoria=OrdenTrabajo.categoria_id).first()
        if categoria.permite_solicitud:
            return 'Especial'
        else:
            return 'Catalogo'
   



class UsuariosResource(resources.ModelResource):
    username = Field(
        column_name='Usuarios'
    )
    nombres = Field(
        column_name='Nombres'
    )
    apellidos = Field(
        column_name='Apellidos'
    )
    fecha_ingreso = Field(
        column_name='Fecha Ingreso'
    )
    ultimo_ingreso = Field(
        column_name='Ultimo Ingreso'
    )
    activo = Field(
        column_name='Activo'
    )

    # nombre_tienda = Field(
    #     column_name='Nombre Tienda'
    # )

    contador_ordenes = Field(
        column_name='Contador Ordenes'
    )

    contador_solicitud = Field(
        column_name='Contador Solicitud'
    )

    class Meta:
        model = Usuarios
        fields = (
            'username', 'nombres', 'apellidos',
            'fecha_ingreso', 'ultimo_ingreso',
            'activo', 'nombre_tienda', 'contador_ordenes'
        )
    def dehydrate_username(self, usuarios):
        username = usuarios['username']
        return username
        
    def dehydrate_nombres(self, usuarios):
        nombres = usuarios['first_name']
        return nombres

    def dehydrate_apellidos(self, usuarios):
        apellidos = usuarios['last_name']
        return apellidos
    
    def dehydrate_fecha_ingreso(self, usuarios):
        # fecha_ingreso = str(usuarios['date_joined'])
        formato_fecha = "%d/%m/%Y, %H:%M:%S"
        registro = (usuarios['date_joined'])
        if registro != None:
            fecha_ingreso = datetime.strftime(registro, formato_fecha)
        else:
            fecha_ingreso = "No tenemos registro."
        return fecha_ingreso
    
    def dehydrate_ultimo_ingreso(self, usuarios):
        # ultimo_ingreso = str(usuarios['last_login'])
        formato_fecha = "%d/%m/%Y"
        registro = (usuarios['last_login'])
        if registro != None:
            ultimo_ingreso = datetime.strftime(registro, formato_fecha)
        else:
            ultimo_ingreso = "No tenemos registro."
        return ultimo_ingreso

    def dehydrate_activo(self, usuarios):
        if usuarios['is_active'] == True:
            return 'Si'
        else:
            return 'No'

    # def dehydrate_nombre_tienda(self, usuarios):
    #     registro_id = UsuariosTiendas.objects.filter(usuario_id=usuarios['id'])
    #     for tiendas in registro_id:
    #         nombre_tienda = tiendas.tienda.nombre
    #         return nombre_tienda
    
    def dehydrate_contador_ordenes(self, usuarios):
        registro_id = OrdenTrabajo.objects.filter(usuario_crea=usuarios['id'])
        contador_ordenes = registro_id.count()
        return contador_ordenes

    def dehydrate_contador_solicitud(self, usuarios):
        registro_id = SolicitudTrabajo.objects.filter(usuario_crea=usuarios['id'])
        contador_solicitud = registro_id.count()
        return contador_solicitud


class SolicitudListaResource(resources.ModelResource):

    secuencia = Field(
        attribute="secuencia",
        column_name="Secuencia"
        )
    fecha_creacion=Field(
        attribute="fecha_creacion",
        column_name="Fecha creacion"
        )
    fecha_cotizacion=Field(
        attribute="fecha_cotizacion",
        column_name="Fecha cotizacion"
        )
    estado=Field(
        attribute="estado",
        column_name="Estado"
        )
    codigo = Field(
        column_name="Codigo tienda"
        )
    tienda = Field(
        column_name='Nombre Tienda'
    )
    nombre_taller =Field(
        column_name="Nombre taller"
    )

    peso_solicitado = Field(
        attribute="peso_solicitado",
        column_name="Peso Solicitado"
        )

    peso_min=Field(
        attribute="peso_min",
        column_name="Peso minimo"
        )

    peso_max=Field(
        attribute="peso_max",
        column_name="Peso maximo"
        )

    precio_fabricacion_unitario=Field(
        attribute="precio_fabricacion_unitario",
        column_name="Precio fabricacion unitario"
        )

    total_rubros = Field(
        attribute="total_rubros",
        column_name="Total Rubros"
        )
    
    acabado = Field(
        attribute="acabado",
        column_name="Acabado"
        )

    parte_interna = Field(
        attribute="parte_interna",
        column_name="Parte Interna"
    )

    cantidad_piedras = Field(
        attribute="cantidad_piedras",
        column_name="Cantidad piedras"
        )

    tiempo_ent_min = Field(
        attribute="tiempo_ent_min",
        column_name="Tiempo entrega minimo"
        )

    tiempo_ent_max=Field(
        attribute="tiempo_ent_max",
        column_name="Tiempo entrega maximo"
    )

    detalle=Field(
        attribute="detalle",
        column_name="Detalle"
    )
    sku =Field(
        column_name="SKU"
    )
    item =Field(
        column_name="Item"
    )

    categoria = Field(
        column_name="Categoria"
        )
    tipo_catalogo = Field(
        column_name="Tipo catalogo"
        )
    observacion_cotizado = Field(
        attribute="observacion_cotizado",
        column_name="Observacion cotizado"
        )
    observacion_rechazo_cliente = Field(
        attribute="observacion_rechazo_op",
        column_name="Observacion rechazo Cliente"
        )
    observacion_rechazo_ta = Field(
        attribute="observacion_rechazo_ta",
        column_name="Observacion rechazo Taller"
        )
    color = Field(
        attribute="color__descripcion",
        column_name="Color"
        )
    talla = Field(
        attribute="talla",
        column_name="Talla"
        )
    origen_material = Field(
        attribute="origen_material__descripcion",
        column_name="Origen Material"
        )

    costo_total_fabricacion_ta = Field(
        attribute="costo_total_fabricacion_ta",
        column_name="Costo Total Fabricacion Taller"
        )

    precio_fabricacion_total = Field(
        attribute="precio_fabricacion_total",
        column_name="Precio Fabricacion Total"
        )

    util_sobre_fabrica_ta = Field(
        attribute="util_sobre_fabrica_ta",
        column_name="Utilidad sobre fabrica taller"
        )

    prct_util_sobre_fabrica_ta = Field(
        attribute="prct_util_sobre_fabrica_ta",
        column_name="prct_util_sobre_fabrica_ta"
        )

    # costo total de piedras del taller, se toma de la tabla solicitudespiedras
    costo_total_piedras_ta = Field(
        column_name="Costo total Piedras Taller"
        )

    precio_total_piedras_ta = Field(
        column_name = "Precio Total Piedras Taller"
        )

    subtotal_taller = Field(
        attribute="subtotal_taller",
        column_name="Subtotal Taller"
        )
    impuestos_taller = Field(
        attribute="impuestos_taller",
        column_name="Impuestos Taller"
        )

    total_taller = Field(
        attribute="total_taller",
        column_name="total_taller"
        )

    tiempo_cotizacion = Field(
        attribute="tiempo_cotizacion",
        column_name="tiempo_cotizacion"
        )

    clasificacion = Field(
        column_name="Clasificacion"
    )



    class Meta:
        model = SolicitudTrabajo
        fields = (
            'secuencia', 'fecha_creacion', 'fecha_cotizacion',
            'estado', 'codigo', 'tienda', 'nombre_taller', 'peso_solicitado',
            'peso_min', 'peso_max', 'precio_fabricacion_unitario', 'total_rubros',
            'acabado', 'parte_interna', 'cantidad_piedras', 'tiempo_ent_min',
            'tiempo_ent_max', 'detalle', 'sku', 'item', 'categoria', 'tipo_catalogo',
            'observacion_cotizado', 'observacion_rechazo_cliente', 'observacion_rechazo_ta',
            'color', 'talla', 'origen_material', 'costo_total_fabricacion_ta',
            'precio_fabricacion_total',  'util_sobre_fabrica_ta', 'prct_util_sobre_fabrica_ta',
            'costo_total_piedras_ta', 'precio_total_piedras_ta', 'subtotal_taller', 'impuestos_taller',
            'total_taller', 'tiempo_cotizacion', 'clasificacion'
        )


    def dehydrate_codigo(self, SolicitudTrabajo):
        return SolicitudTrabajo.tienda.codigo

    def dehydrate_tienda(self, SolicitudTrabajo):
        return SolicitudTrabajo.tienda.nombre

    def dehydrate_nombre_taller(self, SolicitudTrabajo):
        return SolicitudTrabajo.taller.nombre

    def dehydrate_item(self, SolicitudTrabajo):
        detalle = DetalleSolicitud.objects.filter(solicitud=SolicitudTrabajo).first()
        if detalle != None:
            return detalle.item.descripcion
        else:
            return "no existe item"

    def dehydrate_categoria(self, SolicitudTrabajo):
        detalle = DetalleSolicitud.objects.filter(solicitud=SolicitudTrabajo).first()
        if detalle:
            item = Items.objects.filter(id_item=detalle.item_id).first()
            return item.categoria.descripcion

    def dehydrate_tipo_catalogo(self, SolicitudTrabajo):
        detalle = DetalleSolicitud.objects.filter(solicitud=SolicitudTrabajo).first()
        item = Items.objects.filter(id_item=detalle.item_id).first()
        return item.tipo_catalogo.descripcion

    def dehydrate_costo_total_piedras_ta(self, SolicitudTrabajo):
        costo_piedras = SolicitudesPiedras.objects.filter(solicitud=SolicitudTrabajo).values('costo_piedra_taller', 'cantidad_piedras')
        costo_total = 0
        cantidad =0
        costo = 0
        for i in costo_piedras:
            # suma_costo += costo_total_piedras_ta['subtotal_piedras_taller']
            costo = i['costo_piedra_taller']
            cantidad = i['cantidad_piedras']
            costo_total = cantidad * costo
        return costo_total


    def dehydrate_precio_total_piedras_ta(self, SolicitudTrabajo):
        costo_piedras = SolicitudesPiedras.objects.filter(solicitud=SolicitudTrabajo).values('precio_piedra_taller', 'cantidad_piedras')
        precio_total = 0
        cantidad =0
        precio = 0
        for i in costo_piedras:
            # suma_costo += costo_total_piedras_ta['subtotal_piedras_taller']
            cantidad = i['precio_piedra_taller']
            precio = i['cantidad_piedras']
            precio_total = cantidad * precio
        return precio_total

    def dehydrate_subtotal_taller(self, SolicitudTrabajo):
        subt_taller = SolicitudTrabajo.subtotal_taller
        if subt_taller != None:
            return subt_taller
        else:
            return 0


    def dehydrate_clasificacion(self, SolicitudTrabajo):

        detalle_obj = DetalleSolicitud.objects.filter(solicitud_id=SolicitudTrabajo.id_solicitud).first()
        item_obj = Items.objects.filter(id_item=detalle_obj.item_id).first()
        categoria = Categorias.objects.filter(id_categoria=item_obj.categoria_id).first()
        if categoria.permite_solicitud:
            return 'Especial'
        else:
            return 'Catalogo'


    # def dehydrate_sku(self, OrdenTrabajo):
    #     detalle_obj = DetalleOrden.objects.filter(orden_id=OrdenTrabajo.id_orden).first()
    #     if detalle_obj.id_item == None:
    #         detalle_solicitud = DetalleSolicitud.objects.filter(solicitud_id=detalle_obj.id_solicitud).first()
    #         item_id = detalle_solicitud.item_id
    #     else:
    #         item_id = detalle_obj.id_item
    #     item_sku = Items.objects.filter(id_item=item_id).first()
    #     return item_sku.sku
    def dehydrate_sku(self, SolicitudTrabajo):
        detalle = DetalleSolicitud.objects.filter(solicitud=SolicitudTrabajo).first()
        if detalle != None:
            return detalle.item.sku
        else:
            return "no existe item"







