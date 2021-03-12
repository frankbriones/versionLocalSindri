from celery import shared_task
from django.core.mail import EmailMessage

from django.http import FileResponse, HttpResponse
from django.conf import settings
from io import StringIO
from datetime import datetime, timezone, timedelta
import os
import requests

import io
import json

import itertools
from random import randint
from statistics import mean

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

from .models import OrdenTrabajo, DetalleOrden, SolicitudTrabajo, \
    DetalleSolicitud, SolicitudesImagenes
from ctg.models import Categorias, Adicionales, Items, DetalleItems,\
    Tallas, DetallePiedras, ItemsImagenes
from usr.models import Usuarios, GruposPermisos
from est.models import Talleres
from cfg.models import ConfiguracionApiSMS
from django.contrib.auth.models import Permission


@shared_task
def enviarCorreo(correos):
    correos = json.loads(correos)
    print(correos)
    subject = "prueba"
    # to = ["jamoran21@hotmail.com", ]
    to = correos
    desde = settings.EMAIL_HOST_USER
    from_email = desde
    message = "Este es un correo de prueba"

    email = EmailMessage(subject, message, bcc=to, from_email=from_email)
    email.content_subtype = "text"
    email.send()


@shared_task
def enviarReporte(correos, usuario):
    correos = json.loads(correos)
    subject = "Reporte mensual de órdenes de trabajo"
    to = correos
    desde = settings.EMAIL_HOST_USER
    from_email = desde
    message = "Este es un correo de prueba"
    archivo = generarReporteOrdenes(usuario)
    contenido = open(archivo, 'rb').read()
    attachment = ('reporte_ordenes.pdf', contenido, 'application/pdf')

    email = EmailMessage(subject, message, bcc=to, from_email=from_email,
                         attachments=[attachment, ])
    email.content_subtype = "text"
    # email.attachments(filename='reporte_ordenes', content=archivo,
    #                   mimetype='application/pdf')
    email.send()


@shared_task
def enviarCorreoCliente(id_orden):
    orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
    detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
        exclude(id_solicitud=None).first()
    sintalla = Tallas.objects.filter(talla=0).first()

    adicionales_lista = []
    adicionales = DetalleOrden.objects.filter(orden_id=id_orden)
    costo_adicionales = 0.00
    for adicional in adicionales:
        if adicional.id_adicional:
            item_adicional = Adicionales.objects.\
                filter(id_adicional=adicional.id_adicional).first()
            adicional_detalle = [
                str(adicional.id_detalle_orden),
                str(item_adicional.descripcion),
                str(item_adicional.precio),
                str(adicional.cantidad)
            ]
            adicionales_lista.append(adicional_detalle)
            costo_adicionales += \
                (float(item_adicional.precio)*float(adicional.cantidad))
        if adicional.id_piedra:
            item_adicional = DetallePiedras.objects.\
                filter(id_detalle_piedra=adicional.id_detalle_piedra).\
                first()
            adicional_detalle = [
                str(adicional.id_detalle_orden),
                str(item_adicional.piedra.descripcion),
                str(item_adicional.precio),
                str(adicional.cantidad)
            ]
            adicionales_lista.append(adicional_detalle)
            costo_adicionales += \
                (float(item_adicional.precio)*float(adicional.cantidad))
    costo_adicionales = round(costo_adicionales, 2)

    if detalleitem:
        item = SolicitudTrabajo.objects.\
            filter(pk=detalleitem.id_solicitud).first()
        detalleSolicitud = DetalleSolicitud.objects.\
            filter(solicitud_id=item.id_solicitud).first()
        detalle = DetalleItems.objects.\
            filter(
                pk=detalleitem.id_detalle_item

            ).first()
        imagenes = SolicitudesImagenes.objects.\
            filter(solicitud=item)
    else:
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_item=None).first()
        item = Items.objects.filter(pk=detalleitem.id_item).first()
        detalle = DetalleItems.objects.\
            filter(id_item_id=item.id_item).first()
        detalleSolicitud = None
        imagenes = ItemsImagenes.objects.\
            filter(item=item)
    precio_final = float(orden.precio_final_venta) \
        + float(orden.costo_envio)

    contexto = {
                'orden': orden,
                'item': item,
                'detalle': detalle,
                'detalleSolicitud': detalleSolicitud,
                'sintalla': sintalla,
                'costo_adicionales': costo_adicionales,
                'adicionales_lista': adicionales_lista,
                'precio_final': precio_final,
                'sUrl': os.getcwd(),
                'imagenes': imagenes,
                'sitio': settings.SITIO
                }
    subject = "Información sobre orden de trabajo"
    to = [orden.cliente.correo]
    desde = settings.EMAIL_HOST_USER
    from_email = desde
    message = get_template('trn/correo_cliente.html').render(contexto)
    email = EmailMessage(subject, message, bcc=to, from_email=from_email)
    email.content_subtype = "html"
    email.send()

from usr.models import UsuariosGruposEmpresariales, UsuariosTiendas
from est.models import Zonas, GruposEmpresariales
@shared_task
def enviarCorreoZonal(id_orden):
    orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
    detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
        exclude(id_solicitud=None).first()
    sintalla = Tallas.objects.filter(talla=0).first()
    zona  = Zonas.objects.filter(id_zona=orden.tienda.zona.id_zona).first()
    usuario = Usuarios.objects.filter(
            zona=zona.id_zona,
            rol__zonal=True
            ).first()


    adicionales_lista = []
    adicionales = DetalleOrden.objects.filter(orden_id=id_orden)
    costo_adicionales = 0.00
    for adicional in adicionales:
        if adicional.id_adicional:
            item_adicional = Adicionales.objects.\
                filter(id_adicional=adicional.id_adicional).first()
            adicional_detalle = [
                str(adicional.id_detalle_orden),
                str(item_adicional.descripcion),
                str(item_adicional.precio),
                str(adicional.cantidad)
            ]
            adicionales_lista.append(adicional_detalle)
            costo_adicionales += \
                (float(item_adicional.precio)*float(adicional.cantidad))
        if adicional.id_piedra:
            item_adicional = DetallePiedras.objects.\
                filter(id_detalle_piedra=adicional.id_detalle_piedra).\
                first()
            adicional_detalle = [
                str(adicional.id_detalle_orden),
                str(item_adicional.piedra.descripcion),
                str(item_adicional.precio),
                str(adicional.cantidad)
            ]
            adicionales_lista.append(adicional_detalle)
            costo_adicionales += \
                (float(item_adicional.precio)*float(adicional.cantidad))
    costo_adicionales = round(costo_adicionales, 2)

    if detalleitem:
        item = SolicitudTrabajo.objects.\
            filter(pk=detalleitem.id_solicitud).first()
        detalleSolicitud = DetalleSolicitud.objects.\
            filter(solicitud_id=item.id_solicitud).first()
        detalle = DetalleItems.objects.\
            filter(
                pk=detalleitem.id_detalle_item

            ).first()
    else:
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_item=None).first()
        item = Items.objects.filter(pk=detalleitem.id_item).first()
        detalle = DetalleItems.objects.\
            filter(id_item_id=item.id_item).first()
        detalleSolicitud = None
    precio_final = float(orden.precio_final_venta) \
        + float(orden.costo_envio)

    contexto = {
                'orden': orden,
                'item': item,
                'detalle': detalle,
                'detalleSolicitud': detalleSolicitud,
                'sintalla': sintalla,
                'costo_adicionales': costo_adicionales,
                'adicionales_lista': adicionales_lista,
                'precio_final': precio_final,
                'sUrl': os.getcwd()
                }
    subject = "Información sobre orden de trabajo"
    to = [usuario.email]
    desde = settings.EMAIL_HOST_USER
    from_email = desde
    message = get_template('trn/correo_producto_recibido.html').\
        render(contexto)
    email = EmailMessage(subject, message, bcc=to, from_email=from_email)
    email.content_subtype = "html"
    email.send()


def generarReporteOrdenes(usuario):
    template_name = "trn/reporte_lista_ordenes.html"
    contexto = {}
    opcion = 5

    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    ultimo_dia_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    fecha_inicio = ultimo_dia_mes_anterior.replace(
        day=ahora.day,
        hour=0,
        minute=0,
        second=0
        )
    fecha_fin = ahora.replace(
        hour=0,
        minute=0,
        second=0
        )

    usuario = Usuarios.objects.filter(username=usuario).first()
    taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
    if usuario.tipo_usuario_id == 2:
        path = settings.MEDIA_ROOT + "/reportes/reporte_ordenes_taller.pdf"
    else:
        path = settings.MEDIA_ROOT + "/reportes/reporte_ordenes_ope.pdf"
    print(path)
    if usuario.tipo_usuario_id == 3:
        taller = None
        usuario = usuario
        ordenes = OrdenTrabajo.objects.\
            filter(
                tienda__sociedad__grupo_empresarial=usuario.grupo_empresarial(),
                fecha_creacion__gte=fecha_inicio,
                fecha_creacion__lte=fecha_fin
            ).order_by('estado__orden', '-fecha_modificacion')
        solicitudes = SolicitudTrabajo.objects.filter(
            tienda__sociedad__grupo_empresarial=usuario.grupo_empresarial(),
            estado__descripcion='ESPERA COTIZACION TALLER'
        ) | SolicitudTrabajo.objects.filter(
            tienda__sociedad__grupo_empresarial=usuario.grupo_empresarial(),
            estado__descripcion='ESPERA DE EVALUACION'
        )
        solicitudes = solicitudes.\
            order_by('estado__orden', '-fecha_modificacion')
    else:
        taller = usuario.taller()
        usuario = None
        ordenes = OrdenTrabajo.objects.\
            filter(
                taller_id=taller.id_taller,
                fecha_creacion__gte=fecha_inicio,
                fecha_creacion__lte=fecha_fin
            ).order_by('estado__orden', '-fecha_modificacion')
        solicitudes = SolicitudTrabajo.objects.filter(
            taller_id=taller.id_taller,
            estado__descripcion='ESPERA COTIZACION TALLER'
        ) | SolicitudTrabajo.objects.filter(
            taller_id=taller.id_taller,
            estado__descripcion='ESPERA DE EVALUACION'
        )
        solicitudes = solicitudes.\
            order_by('estado__orden', '-fecha_modificacion')

    contexto = {
                'ordenes': ordenes,
                'sUrl': settings.BASE_DIR,
                'taller': taller,
                'usuario': usuario,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'opcion': opcion,
                'solicitudes': solicitudes
                }

    archivo = open(path, 'w+b')
    template = get_template(template_name)
    html = template.render(contexto)

    pisaStatus = pisa.CreatePDF(
            html,
            dest=archivo)

    # close output file
    archivo.close()

    # return True on success and False on errors
    if pisaStatus.err:
        return pisaStatus.err
    return path


@shared_task
def enviarSms(id_transaccion, tipo):
    print('envio de sms ***************')
    if tipo == 1:
        transaccion = OrdenTrabajo.objects.\
            filter(id_orden=id_transaccion).first()
    else:
        transaccion = SolicitudTrabajo.objects.\
            filter(id_solicitud=id_transaccion).first()
    
    permiso = Permission.objects.\
        filter(codename='envio_sms').first()
    grupos = GruposPermisos.objects.\
        filter(permission_id=permiso.id).\
        values('group_id')
    if transaccion.externa:
        usuarios = Usuarios.objects.\
            filter(
                usuariosgruposempresariales=transaccion.tienda.sociedad.grupo_empresarial.id_grupo_empresarial,
                rol__grupo__in=grupos
            )
    else:
        
        usuarios = Usuarios.objects.\
            filter(
                usuariostalleres=transaccion.taller_id,
                rol__grupo__in=grupos
            ) | Usuarios.objects.\
            filter(
                usuariosgruposempresariales__usuario_id=transaccion.usuario_crea,
                rol__grupo__in=grupos
            )
    url_token = ConfiguracionApiSMS.objects.\
        filter(
            clave='URL_TOKEN',
            pais_id=transaccion.pais_id
        ).first()
    usuario_api = ConfiguracionApiSMS.objects.\
        filter(
            clave='client_id',
            pais_id=transaccion.pais_id
        ).first()
    clave_api = ConfiguracionApiSMS.objects.\
        filter(
            clave='client_secret',
            pais_id=transaccion.pais_id
        ).first()
    url_envio = ConfiguracionApiSMS.objects.\
        filter(
            clave='URL_ENVIO_LISTA',
            pais_id=transaccion.pais_id
        ).first()
    contenido_sms = ConfiguracionApiSMS.objects.\
        filter(
            clave='CONTENIDO_SMS',
            pais_id=transaccion.pais_id
        ).first()
    resToken = obtenerToken(
        url_token.valor,
        usuario_api.valor,
        clave_api.valor
    )
    resToken = json.loads(resToken.text)
    token = resToken.get('access_token')
    listaEnvio = []
    for usuario in usuarios:
        elemento = {
            'to_number': usuario.telefono,
            'content': contenido_sms.valor +
            ' Transaccion: ' + transaccion.secuencia +
            ' Sucursal: ' + transaccion.tienda.nombre
        }
        listaEnvio.append(elemento)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    envio = requests.post(
        url=url_envio.valor,
        json=listaEnvio,
        headers=headers
    )


def obtenerToken(url, usuario, clave):
    headers = {
        'Content-Type': 'application/json',
    }
    body = {
        'client_id': usuario,
        'client_secret': clave,
        'grant_type': 'client_credentials'
    }
    respuesta = requests.post(url=url, json=body, headers=headers)
    return respuesta




@shared_task
def enviarTelegram(lista, mensaje_telegram):
    print(lista)
    url_bot = 'https://buzzery.innode.pro/enviar_mensaje/'
    json_usuario = {}
    for username in lista:
        json_usuario = {
            'sistemaNombre': 'SINDRI',
            'username': username,
            'mensaje': mensaje_telegram
        }
        r = requests.post(url_bot, json=json_usuario)
    return r.status_code
