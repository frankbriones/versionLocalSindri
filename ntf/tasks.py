from celery import shared_task

from .models import Notificaciones
from usr.models import Usuarios
from trn.models import SolicitudTrabajo, DetalleSolicitud, \
    OrdenTrabajo, DetalleOrden
from django.contrib.auth.models import Group, Permission

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from est.models import Talleres
from ctg.models import Items


@shared_task
def crearNotificacionTaller(id_usuario_genera, id_taller, producto, principal,
                            id_usuario_recib, postergada, id_transaccion,
                            tipo_transaccion, id_estado):
    if id_taller == 1:
        taller = Talleres.objects.filter(nombre='NEUTRO').first()
        id_taller = taller.id

    infoNotificacion = Notificaciones(
        usuario_genera_id=id_usuario_genera,
        usuario_recibe=id_usuario_recibe,
        taller_id=id_taller,
        nombre_producto=producto,
        principal=principal,
        postergada=postergada,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
        estado_id=id_estado
    )
    if infoNotificacion:
        infoNotificacion.save()


@shared_task
def NotificacionSolicitudCreada(id_usuario_genera, id_usuario_recibe,
                                id_taller, producto, principal, postergada,
                                id_transaccion, tipo_transaccion, id_estado, tipo_notificacion):

    if id_taller == 1:
        taller = Talleres.objects.filter(nombre='NEUTRO').first()
        id_taller = taller.id

    infoNotificacion = Notificaciones(
        usuario_genera_id=id_usuario_genera,
        tienda_id=id_usuario_recibe,
        taller_id=id_taller,
        nombre_producto=producto,
        principal=principal,
        postergada=postergada,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
        estado_id=id_estado,
        tipo_notificacion=tipo_notificacion
    )
    if infoNotificacion:
        infoNotificacion.save()

@shared_task
def NotificacionSolicitudCreada(id_usuario_genera, id_usuario_recibe,
                                id_taller, producto, principal, postergada,
                                id_transaccion, tipo_transaccion, id_estado, tipo_notificacion):

    if id_taller == 1:
        taller = Talleres.objects.filter(nombre='NEUTRO').first()
        id_taller = taller.id

    infoNotificacion = Notificaciones(
        usuario_genera_id=id_usuario_genera,
        tienda_id=id_usuario_recibe,
        taller_id=id_taller,
        nombre_producto=producto,
        principal=principal,
        postergada=postergada,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
        estado_id=id_estado,
        tipo_notificacion=tipo_notificacion
    )
    if infoNotificacion:
        infoNotificacion.save()





@shared_task
def NotificacionSolicitudCotizada(id_usuario_genera, tienda_id,
                                  taller_id, producto, principal, postergada,
                                  id_transaccion, tipo_transaccion, id_estado, tipo_notificacion):

    solicitud = SolicitudTrabajo.objects.\
        filter(id_solicitud=id_transaccion).first()

    notificaciones = Notificaciones.objects.filter(
        taller_id=taller_id,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
    )
    for notificacion in notificaciones:
        notificacion.estado_id = id_estado
        notificacion.vista = True
        notificacion.save()

    infoNotificacion = Notificaciones(
        usuario_genera_id=id_usuario_genera,
        taller_id=taller_id,
        tienda_id=tienda_id,
        nombre_producto=producto,
        principal=principal,
        postergada=postergada,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
        estado_id=id_estado,
        tipo_notificacion=tipo_notificacion
    )
    if infoNotificacion:
        infoNotificacion.save()
    if solicitud.pais:
        grupo = 'ws_' + str(solicitud.pais).lower()
    else:
        grupo = 'ws_neutro'
    channel_layer = get_channel_layer()
    print(grupo)
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        grupo,
        {
            'type': 'chat_message',
            'message': 'nuevo registro'
        }
    )


@shared_task
def NotificacionSolicitudActualizar(id_taller, id_transaccion,
                                    tipo_transaccion, id_estado):
    notificaciones = Notificaciones.objects.filter(
        taller_id=id_taller,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
    )
    for notificacion in notificaciones:
        notificacion.vista = True
        notificacion.estado_id = id_estado
        notificacion.save()


@shared_task
def NotificacionOrdenes(id_usuario_genera, tienda_id,
                        id_taller, producto, principal, postergada,
                        id_transaccion, tipo_transaccion, id_estado, tipo_notificacion):

    orden = OrdenTrabajo.objects.\
        filter(id_orden=id_transaccion).first()

    infoNotificacion = Notificaciones(
        usuario_genera_id=id_usuario_genera,
        tienda_id=tienda_id,
        taller_id=id_taller,
        nombre_producto=producto,
        principal=principal,
        postergada=postergada,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion,
        estado_id=id_estado,
        tipo_notificacion=tipo_notificacion
    )
    if infoNotificacion:
        infoNotificacion.save()
    if orden.pais:
        grupo = 'ws_' + str(orden.pais).lower()
    else:
        grupo = 'ws_neutro'
    channel_layer = get_channel_layer()
    print(grupo)
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        grupo,
        {
            'type': 'chat_message',
            'message': 'nuevo registro'
        }
    )


@shared_task
def NotificacionEvaluarSolicitud(id_transaccion, user):
    print(user)
    solicitud = SolicitudTrabajo.objects.\
        filter(id_solicitud=id_transaccion).first()
    detalle = DetalleSolicitud.objects.\
        filter(solicitud_id=solicitud.id_solicitud).first()
    taller = Talleres.objects.\
        filter(id_taller=solicitud.taller_id).first()

    if solicitud.estado.descripcion == 'ESPERA DE EVALUACION':
        infoNotificacion = Notificaciones(
            usuario_genera_id = user,
            tienda_id=solicitud.tienda_id,
            taller_id=taller.id_taller,
            nombre_producto=detalle.item.descripcion,
            principal=1,
            postergada=1,
            id_transaccion=id_transaccion,
            tipo_transaccion=1,
            estado_id=3,
            tipo_notificacion=2
        )
        if infoNotificacion:
            infoNotificacion.save()
        if solicitud.pais:
            grupo = 'ws_' + str(solicitud.pais).lower()
        else:
            grupo = 'ws_neutro'
        channel_layer = get_channel_layer()
        print(grupo)
        print(channel_layer)
        async_to_sync(channel_layer.group_send)(
            grupo,
            {
                'type': 'chat_message',
                'message': 'nuevo registro'
            }
        )


@shared_task
def NotificacionLimiteVenta(id_transaccion):
    orden = OrdenTrabajo.objects.\
        filter(id_orden=id_transaccion).first()
    detalleitem = DetalleOrden.objects.filter(orden_id=orden.id_orden).\
        exclude(id_solicitud=None).first()
    if detalleitem:
        solicitud = SolicitudTrabajo.objects.\
            filter(pk=detalleitem.id_solicitud).first()
        detalleSolicitud = DetalleSolicitud.objects.\
            filter(solicitud_id=solicitud.id_solicitud).first()
        producto = detalleSolicitud.item.descripcion
    else:
        detalleitem = DetalleOrden.objects.\
            filter(orden_id=orden.id_orden).\
            exclude(id_item=None).first()
        item = Items.objects.filter(pk=detalleitem.id_item).first()
        producto = item.descripcion

    if orden.estado.descripcion == 'PRODUCTO RECIBIDO':
        infoNotificacion = Notificaciones(
            usuario_genera_id=orden.usuario_id,
            tienda_id=orden.tienda_id,
            taller_id=orden.taller_id,
            nombre_producto=producto,
            principal=1,
            postergada=0,
            id_transaccion=id_transaccion,
            tipo_transaccion=2,
            estado_id=17
        )
        if infoNotificacion:
            infoNotificacion.save()
        if orden.pais:
            grupo = 'ws_' + str(orden.pais).lower()
        else:
            grupo = 'ws_neutro'
        channel_layer = get_channel_layer()
        print(grupo)
        print(channel_layer)
        async_to_sync(channel_layer.group_send)(
            grupo,
            {
                'type': 'chat_message',
                'message': 'nuevo registro'
            }
        )


@shared_task
def NotificacionOrdenesActualizar(tienda_id,
                                  id_taller, id_transaccion,
                                  tipo_transaccion, id_estado):

    notificaciones = Notificaciones.objects.filter(
        tienda_id=tienda_id,
        taller_id=id_taller,
        id_transaccion=id_transaccion,
        tipo_transaccion=tipo_transaccion
    )

    if notificaciones:
        for notificacion in notificaciones:
            if id_estado == 18:
                notificacion.vista=0
                notificacion.tipo_notificacion=1
            notificacion.estado_id = id_estado
            notificacion.save()
