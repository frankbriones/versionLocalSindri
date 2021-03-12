from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
import json
from datetime import datetime, timezone, timedelta
import pdb

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import SolicitudTrabajo, DetalleSolicitud,\
    OrdenTrabajo, DetalleOrden, OrigenMaterial, RubrosAsociados, \
    SolicitudRubros, SolicitudesImagenes, OrdenesImagenes, SolicitudesPiedras, Facturas, \
    DetallesFacturas, OrdenesPiedras, OrdenesAdicionales, SolicitudesAdicionales, \
    ConfiguracionTooltipOperaciones, ConfiguracionRechazoSolicitudOrdenes

from .forms import SolicitudDetalleForm, SolicitudEditarForm, \
    OrdenEnvioMaterialForm, OrdenAnticipoForm
from .serializers import EnvioMaterialSerializer, RecibirMaterialSerializer,\
    AnularOrdenSerializer, FinalizarTrabajoSerializer, \
    EnviarProductoSerializer, DevolverProductoSerializer, \
    FinalizarOrdenSerializer, SolicitarAExternoSerializer, \
    OrdenesSerializer, SolicitudesSerializer, GenerarOrdenSerializer,\
    FinalizarSinVentaSerializer, RecibirProductoSerializer, \
    CargarDocTallerSerializer, CargarDocOpSerializer, FacturasSerializer, \
    DetallesFacturasSerializer, OrdenImagenesSerializer
from ctg.serializers import PiezasPiedrasItemSerializer
from .tasks import enviarCorreo, enviarCorreoCliente, enviarCorreoZonal,\
    enviarSms, enviarTelegram
from ntf.tasks import crearNotificacionTaller, NotificacionSolicitudCreada, \
    NotificacionEvaluarSolicitud, NotificacionSolicitudCotizada, \
    NotificacionOrdenes, NotificacionLimiteVenta, \
    NotificacionOrdenesActualizar, NotificacionSolicitudActualizar
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from ntf.models import Notificaciones

from ctg.models import Items, DetalleItems, ItemsColores, Adicionales,\
    Tallas, Piedras, DetallePiedras, Colores, TiposPrecios, ItemsImagenes,\
    Acabados, Anchuras, PartesInternas, Piezas, PiezasAcabados, \
    PiezasDetalles, PiezasPiedras
from cfg.models import ConfigGeneral, ConfigUtilidadProveedor,\
    ConfigUtilidadTaller
from usr.models import Usuarios, UsuariosTiendas, UsuariosTalleres
from clt.models import Clientes
from prv.models import Proveedores
from cfg.models import ConfiguracionSistema, PoliticasComerciales
from est.models import Talleres, GruposEmpresariales, Tiendas, Zonas, Sociedades

# from trn.forms import ConfiguracionTooltipForm

from bases.views import SinPermisos
from bases.models import Estados

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# reportes
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

from .resources import OrdenesResource, OrdenesListaResource, SolicitudListaResource

# from trn.forms import ConfiguracionTooltipForm

@login_required(login_url='/login/')
def editar_detalle_tooltip(request):
    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        id_nota = request.GET.get("id_nota", None)
        detalle = request.GET.get("detalle", None)
        campo = request.GET.get("campo", None)
        if id_nota:
            try:
                nota_obj = ConfiguracionTooltipOperaciones.objects.filter(id_tooltip=id_nota).first()
                if nota_obj:
                    print(nota_obj, 'llll')
                    nota = ConfiguracionTooltipOperaciones.objects.filter(id_tooltip=id_nota).first()
                    nota.texto = detalle
                    nota.save()
                    estado = 1
            except ConfiguracionTooltipOperaciones.DoesNotExist:
                estado = 0
                agregar = ConfiguracionTooltipOperaciones(

                        texto=detalle,
                        grupo=request.user.grupo_empresarial().id_grupo_empresarial,
                        estado=1,
                        pais=request.user.pais
                    )
                agregar.save()
                return HttpResponseRedirect('/')
        else:
            estado = 0
            obtener_tool = ConfiguracionTooltipOperaciones.objects.\
                filter(
                    campo_orden=campo,
                    grupo=request.user.grupo_empresarial().id_grupo_empresarial,
                    estado=1,
                    pais=request.user.pais_id
                ).first()
            print(obtener_tool)
            if obtener_tool:
                obtener_tool.delete()
            agregar_tooltip = ConfiguracionTooltipOperaciones(
                campo_orden=campo,
                texto=detalle,
                grupo=request.user.grupo_empresarial().id_grupo_empresarial,
                estado=1,
                pais=request.user.pais_id
            )
            agregar_tooltip.save()

        return JsonResponse({"estado": estado})
            # return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)


@login_required(login_url='/login/')
def tooltip(request, grupo_id):
    template_name = "trn/notas_de_ayuda.html"
    if request.method == 'GET':
        grupo =  GruposEmpresariales.objects.filter(id_grupo_empresarial=grupo_id).values('anticipo_fabricacion', 'comprobante_env', 'factura_taller', 'cta_por_pagar', 'orden_compra', 'origen_material')
        config = ConfiguracionTooltipOperaciones.objects.filter(grupo=grupo_id, pais=request.user.pais_id)
        # my_model_fields = [field.name for field in GruposEmpresariales._meta.get_fields()]
        # print(my_model_fields)
        if grupo != None:
            lista_tool = []
            listado = []
            for key, value in grupo[0].items():
                campos = {
                        'texto':key,
                        'clave': value
                    }
                listado.append(campos)
                if key == 'origen_material':
                    if value > 0 :
                        value = True
                tooltip_config = {
                    'id_nota': 0, 
                    'texto':key,
                    'estado': value,
                    'title' : '',
                    'pais': request.user.pais_id,
                    'grupo': grupo_id
                }
                lista_tool.append(tooltip_config)

                for c in config:
                    if str(c.campo_orden) == str(key):
                        tooltip_config['id_nota'] = c.id_tooltip
                        tooltip_config['title'] = c.texto

            lista_campos = [x.get('texto') for x in lista_tool]
            lista_agregada = ConfiguracionTooltipOperaciones.objects.filter(grupo=grupo_id, pais=request.user.pais_id)
            lista_nueva_agregada = []
            for i in lista_agregada:
                infoTool = {
                    'id_nota': i.id_tooltip, 
                    'texto':i.campo_orden,
                    'estado': 1,
                    'title' : i.texto,
                    'pais': request.user.pais_id,
                    'grupo': grupo_id
                }
                lista_nueva_agregada.append(infoTool)
            for tool_nuevos in lista_nueva_agregada:
                if str(tool_nuevos.get('texto')) in lista_campos:
                    pass
                else:
                    lista_campos.append(tool_nuevos.get('texto'))
                    lista_tool.append(tool_nuevos)

            lista_campos = sorted(lista_campos)
            lista_nueva = ConfiguracionTooltipOperaciones.objects.filter(grupo=None, pais=None)
            lista_nueva_tool = []
            for i in lista_nueva:
                info = {
                    'id_nota': i.id_tooltip, 
                    'texto':i.campo_orden,
                    'estado': 1,
                    'title' : '',
                    'pais': '',
                    'grupo': ''
                }
                lista_nueva_tool.append(info)
            print(lista_nueva_tool)
            for tooltip in lista_nueva_tool:
                if str(tooltip.get('texto')) in lista_campos:
                    pass
                else:
                    lista_tool.append(tooltip)

            contexto={
                'lista_tool': listado,
                'lista_activa': lista_tool
            }
            return render(request, template_name, contexto)


        return HttpResponseRedirect('/')


# eliminar tool
def eliminarTool(request):
    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        tool = request.GET.get('tooltip_id', None)
        if tool:
            try:
                tool_obj = ConfiguracionTooltipOperaciones.objects.filter(id_tooltip=tool).first()
                # categoria_items = Items.objects.filter(categoria_id=categoria_obj.id_categoria).exists()
                if tool_obj:
                    tool_obj.delete()
                    estado = 1
                else:
                    estado = 2
            except ConfiguracionTooltipOperaciones.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)




class SolicitudesListaView(SinPermisos, generic.ListView):
    permission_required = "trn.view_solicitudtrabajo"
    model = SolicitudTrabajo
    template_name = "trn/solicitudes_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        tiendas=UsuariosTiendas.objects.filter(usuario=self.request.user).values('tienda_id')
        if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
            return OrdenTrabajo.objects.\
                filter(tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial())
        if self.request.user.rol.zonal == True:
            return OrdenTrabajo.objects.filter(tienda__zona_id=self.request.user.zona)

        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES': 
            return OrdenTrabajo.objects.filter(tienda__in=tiendas)
        else:
            return OrdenTrabajo.objects.filter(taller=self.request.user.taller())


class SolicitudesListaAPIView(APIView):
    def get(self, request):
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            solicitudes=SolicitudTrabajo.objects.\
                filter(tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial())
        else:
            solicitudes=SolicitudTrabajo.objects.\
                filter(taller=self.request.user.taller())
        data = SolicitudesSerializer(solicitudes, many=True).data
        return Response(data)


class SolicitudesListaFechaAPIView(APIView):
    def get(self, request, f_inicio, f_fin, opcion):
        tiendas=UsuariosTiendas.objects.filter(usuario=self.request.user).values('tienda_id')
        ahora = datetime.now(timezone.utc)
        dia_uno_mes_actual = ahora.replace(
            day=1,
            hour=0,
            minute=0,
            second=0
            )
        dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
        dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
            day=1,
            hour=0,
            minute=0,
            second=0
            )
        f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
        f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            if opcion == 1:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial(),
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                                fecha_creacion__gte=dia_uno_mes_actual,
                                fecha_creacion__lte=ahora
                            ).order_by('-fecha_modificacion')
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=dia_uno_mes_actual,
                                fecha_creacion__lte=ahora
                            ).order_by('-fecha_modificacion')
            if opcion == 2:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial(),
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                usuario__user_usuariostiendas__tienda_id__zona_id=self.request.user.zona,
                                fecha_creacion__gte=dia_uno_mes_anterior,
                                fecha_creacion__lte=dia_uno_mes_actual
                            ).order_by('-fecha_modificacion')
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=dia_uno_mes_anterior,
                                fecha_creacion__lte=dia_uno_mes_actual
                            ).order_by('-fecha_modificacion')
            if opcion == 3:
                # tiendas  = UsuariosTiendas.objects.\
                #     filter(
                #         usuario_id=self.request.user.id
                #         ).values('tienda_id')

                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()
                        ).order_by('-fecha_modificacion')[:100]
                else:
                    if self.request.user.rol.zonal:
                        
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona
                            ).order_by('-fecha_modificacion')[:100]
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda_id__in=tiendas
                            ).order_by('-fecha_modificacion')[:100]
            if opcion == 4:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()
                        ).order_by('-fecha_modificacion')[:1000]
                else:
                    if self.request.user.rol.zonal:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona
                            ).order_by('-fecha_modificacion')[:1000]
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__in=tiendas
                            ).order_by('-fecha_modificacion')[:1000]
            if opcion == 5:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial(),
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                                fecha_creacion__gte=f_inicio,
                                fecha_creacion__lte=f_fin + timedelta(days=1)
                            ).order_by('-fecha_modificacion')
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=f_inicio,
                                fecha_creacion__lte=f_fin + timedelta(days=1)
                            ).order_by('-fecha_modificacion')
            if opcion == 6:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    solicitudes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                            ).order_by('-fecha_modificacion')
                    else:
                        solicitudes = SolicitudTrabajo.objects.\
                            filter(
                                tienda__in=tiendas
                            ).order_by('-fecha_modificacion')
        else:
            if opcion == 1:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller_id=self.request.user.taller(),
                        fecha_creacion__gte=dia_uno_mes_actual,
                        fecha_creacion__lte=ahora
                    ).order_by('-fecha_modificacion')
            if opcion == 2:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller(),
                        fecha_creacion__gte=dia_uno_mes_anterior,
                        fecha_creacion__lte=dia_uno_mes_actual
                    ).order_by('-fecha_modificacion')
            if opcion == 3:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')[:100]
            if opcion == 4:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')[:1000]
            if opcion == 5:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller(),
                        fecha_creacion__gte=f_inicio,
                        fecha_creacion__lte=f_fin + timedelta(days=1)
                    ).order_by('-fecha_modificacion')
            if opcion == 6:
                solicitudes = SolicitudTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')
        data = SolicitudesSerializer(solicitudes, many=True).data
        return Response(data)


class TipoSolicitudView(SinPermisos, generic.TemplateView):
    permission_required = "trn.view_solicitudtrabajo"
    template_name = "trn/tipo_solicitud_modal.html"
    login_url = "bases:login"

    def get_context_data(self, **kwargs):
        context = super(TipoSolicitudView, self).get_context_data(**kwargs)
        id_item = self.kwargs['id_item']
        context['item'] = Items.objects.filter(id_item=id_item).first()
        context['proveedores'] = Proveedores.objects.filter(
            taller=1,
            pais_id=self.request.user.pais_id
        ).count()
        print(context)
        return context


@login_required(login_url='/login/')
@permission_required('trn.add_solicitudtrabajo',
                     login_url='bases:sin_permisos')
def SolicitudesCrearView(request, tipo=None, id_item=None):
    if id_item == 1:
        item_obj = Items.objects.filter(categoria__division__tipo_catalogo__descripcion='PRODUCTOS').first()
        id_item = item_obj.id_item

    else:
        item_obj = Items.objects.filter(categoria__division__tipo_catalogo__descripcion='SERVICIOS').first()
        id_item = item_obj.id_item

    # print(id_item)


    template_name = "trn/solicitudes_form.html"
    form = SolicitudDetalleForm(request=request, tipo=tipo, id_item=id_item)
    contexto = {}
    sin_talla = Tallas.objects.filter(talla=0).first()
    sin_color = Colores.objects.filter(descripcion='SIN COLOR').first()
    tienda_user = UsuariosTiendas.objects.filter(usuario_id=request.user.id).first()
    origen_pre = OrigenMaterial.objects.\
        filter(id_origen=request.user.grupo_empresarial().origen_material).first()
    if request.method == 'GET':

        item = Items.objects.filter(id_item=id_item).first()
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
        taller = Talleres.objects.filter(
            pais=request.user.pais
        ).order_by('prioridad').first()

        tiendas_id = UsuariosTiendas.objects.filter(usuario_id=request.user.id).values('tienda_id')
        tiendas_id = Tiendas.objects.filter(id_tienda__in=tiendas_id)
        if request.user.rol.descripcion == 'ADMIN OPERACIONES':
            tiendas_id = Tiendas.objects.filter(sociedad__grupo_empresarial=request.user.grupo_empresarial())

        if item.tipo_catalogo.descripcion == 'PRODUCTOS':
            item = Items.objects.\
                filter(sku='PRO-GEN-001').first()
            tiendas_id = Tiendas.objects.filter(id_tienda__in=tiendas_id)

        else:
            item = Items.objects.\
                filter(sku='SER-GEN-001').first()
            tiendas_id = Tiendas.objects.filter(id_tienda__in=tiendas_id)
            
        administrador = Usuarios.objects.\
            filter(usuariosgruposempresariales__grupo_empresarial_id=request.user.grupo_empresarial().id_grupo_empresarial).\
            filter(rol_id=3).first()
        rubros = RubrosAsociados.objects.\
            filter(usuario_crea=administrador.id)
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        cantidad_max_img = ConfiguracionSistema.objects.\
            filter(clave='CANTIDAD_MAX_IMAGENES').first()
        proveedores = Proveedores.objects.\
            filter(
                zona__grupo_empresarial=request.user.grupo_empresarial(),
                estado__descripcion='ACTIVO'
            )
        tallas = Tallas.objects.filter(
                    taller=taller,
                    estado__descripcion='ACTIVO'
                )
        colores = Colores.objects.filter(
                    taller=taller,
                    estado__descripcion='ACTIVO'
                    )
        tooltips = ConfiguracionTooltipOperaciones.objects.\
            filter(
                estado=1,
                pais=request.user.pais_id,
                grupo=request.user.grupo_empresarial().id_grupo_empresarial
            )

        tool_detalle = ''
        tool_color = ''

        for tool in tooltips:
            if tool.campo_orden == 'solicitud_detalle':
                tool_detalle = tool.texto
            if tool.campo_orden == 'color':
                tool_color = tool.texto
            
        contexto = {
                    'tipo_solicitud': tipo,
                    'item': item,
                    'sin_talla': sin_talla,
                    'rubros': rubros,
                    'peso_max_img': peso_max_img.valor,
                    'ext_perm_img': ext_perm_img,
                    'form': form,
                    'cantidad_max_img': cantidad_max_img,
                    'proveedores': proveedores,
                    'tallas': tallas,
                    'colores': colores,
                    'taller': taller,
                    'PESO_MAX_DATA': settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
                    'origen_material': OrigenMaterial.objects.all().exclude(descripcion='NINGUNO'),
                    'origen_pre': origen_pre,
                    'tiendas': tiendas_id,
                    'tool_detalle': tool_detalle,
                    'tool_color': tool_color
                    }

    if request.method == 'POST':
        if tipo == 1:
            externa = False
            estado_id = 3
            taller_id = request.POST['solicitud-taller']

            proveedor_id = 1
            peso_minimo = 0
            peso_maximo = 0
            costo_fabricacion_unitario = 0
            prct_impuestos_ta = 0
            precio_fabricacion_unitario = 0
            tiempo_ent_min = 0
            tiempo_ent_max = 0
            taller = Talleres.objects.\
                filter(id_taller=taller_id).first()
            registros = str(taller.secuencia_solicitudes+1)
        if tipo == 2:
            externa = True
            estado_id = 6
            taller_id = 1
            proveedor_id = request.POST['solicitud-proveedor']
            peso_minimo = request.POST['solicitud-peso_min']
            peso_maximo = request.POST['solicitud-peso_max']
            costo_fabricacion_unitario = request.\
                POST['solicitud-costo_fabricacion_unitario']
            prct_impuestos_ta = request.\
                POST['solicitud-prct_impuestos_ta']
            precio_fabricacion_unitario = request.\
                POST['solicitud-precio_fabricacion_unitario']
            tiempo_ent_min = request.POST['solicitud-tiempo_ent_min']
            tiempo_ent_max = request.POST['solicitud-tiempo_ent_max']
            proveedor = Proveedores.objects.\
                filter(id=proveedor_id).first()
            registros = str(proveedor.secuencia_solicitudes+1)
        item_id = request.POST['detalle-item']
        origen_material_id = request.POST['solicitud-origen_material']
        detalle_solicitud = request.POST['solicitud-detalle']
        talla_id = request.POST['solicitud-talla']
        tienda_seleccionada = request.POST['tienda']
        fabricacion_interna = request.POST['fabric_interna']

        if talla_id == '0':
            talla_id = sin_talla.id_talla
        longitud = request.POST['solicitud-longitud']

        color_id = request.POST['solicitud-color']
        if color_id == '0':
            color_id = sin_color.id_color

        # acabado = request.POST['solicitud-acabado']

        # parte_interna = request.POST['solicitud-parte_interna']
        cantidad_piedras = request.POST['solicitud-cantidad_piedras']
        # sku_relacionado = request.POST['solicitud-sku_relacionado']
        rubros_lista = request.POST.getlist('rubros_lista[]')
        longitud = len(rubros_lista)
        total_rubros = request.POST['total_rubros']
        imagenes = request.FILES.getlist('imagen')

        # DATOS EXTRAS PARA EL PESO FINAL DIVIDIDO ENTRE EL ESTABLECIMIENTO Y LA JOYERIA.
        ''' variables peso_cliente, registrado por la joyeria 
        el peso de la materia prima del ciente y la variable establecimiento para el definir el origen de la materia
        prima, ta sea taller o la misma joyeria.'''

        peso_cliente = None
        establecimiento = None
        datos_extra = {}
        datos_extra = request.POST['extra']
        datos_extra = json.loads(datos_extra)
        establecimiento_id = None
        for dato in datos_extra:
            peso_cliente = datos_extra.get('pesoCliente')
            establecimiento = datos_extra.get('origenSeleccionado')

        if len(datos_extra) != 0:
            establecimiento_id = OrigenMaterial.objects.filter(descripcion=str(establecimiento)).first()




        while len(registros) < 5:
            registros = '0' + registros
        if externa:
            secuencia = proveedor.identificacion\
                + '-' + registros
        else:
            secuencia = taller.nombre + '-' + registros

        tienda = Tiendas.objects.filter(id_tienda=tienda_seleccionada).first()

        sociedad = Sociedades.objects.filter(id_sociedad=tienda.sociedad_id).first()
        configuracion_op = sociedad
        infoSolicitud = SolicitudTrabajo(
            secuencia=secuencia,
            externa=externa,
            taller_id=int(float(taller_id)),
            proveedor_id=proveedor_id,
            talla_id=talla_id,
            longitud=longitud,
            detalle=detalle_solicitud,
            # acabado=acabado,
            # parte_interna=parte_interna,
            cantidad_piedras=cantidad_piedras,
            sku_relacionado=id_item,
            color_id=color_id,
            peso_min=peso_minimo,
            peso_max=peso_maximo,
            costo_fabricacion_unitario=costo_fabricacion_unitario,
            prct_impuestos_ta=prct_impuestos_ta,
            precio_fabricacion_unitario=precio_fabricacion_unitario,

            costo_gramo_base_op=sociedad.costo_gramo_base,
            precio_gramo_base_op=sociedad.precio_gramo_base,

            tiempo_ent_min=tiempo_ent_min,
            tiempo_ent_max=tiempo_ent_max,
            origen_material_id=origen_material_id,
            total_rubros=total_rubros,
            estado_id=estado_id,
            usuario_crea=request.user.id,
            tienda_id=int(float(tienda.id_tienda)),
            pais=request.user.pais,
            fabricacion_interna=fabricacion_interna,
            origen_material_dividido = establecimiento_id,
            peso_cliente_dividido= peso_cliente,
            peso_materia_dividida = 0
        )
        if infoSolicitud:
            infoSolicitud.save()
            if infoSolicitud.externa:
                infoSolicitud.proveedor.secuencia_solicitudes += 1
                infoSolicitud.proveedor.save()
            else:
                infoSolicitud.taller.secuencia_solicitudes += 1
                infoSolicitud.taller.save()
            infoDetalle = DetalleSolicitud(
                item_id=item_id,
                solicitud=infoSolicitud,
                usuario_crea=request.user.id,
                pais=request.user.pais,
            )
            if infoDetalle:
                infoDetalle.save()
        if longitud > 0:
            rubros = json.loads(rubros_lista[0])
            if rubros:
                for rubro in rubros:
                    id_rubro = rubro.get('id', None)
                    valor = rubro.get('valor', None)
                    infoRubro = SolicitudRubros(
                        rubro_id=id_rubro,
                        valor=valor,
                        solicitud=infoSolicitud,
                        usuario_crea=request.user.id
                    )
                    if infoRubro:
                        infoRubro.save()
        for imagen in imagenes:
            infoImg = SolicitudesImagenes(
                usuario_crea=request.user.id,
                imagen=imagen,
                solicitud=infoSolicitud,
                pais=request.user.pais
            )
            if infoImg:
                infoImg.save()
        if not externa:
            taller = infoSolicitud.taller_id
            producto = infoDetalle.item.descripcion
            principal = True
            postergada = False
            id_transaccion = infoSolicitud.id_solicitud
            tipo_transaccion = 1
            tipo_notificacion = 2
            NotificacionSolicitudCreada.delay(
                request.user.id,
                infoSolicitud.tienda_id,
                taller,
                producto,
                principal,
                postergada,
                id_transaccion,
                tipo_transaccion,
                infoSolicitud.estado_id,
                tipo_notificacion
            )
            # enviarSms.delay(infoSolicitud.id_solicitud, 2)
            mensaje_telegram = "Se ha generado una Solicitud con la secuencia {}, y solicitada por la tienda '{}'.".format(infoSolicitud.secuencia, infoSolicitud.tienda)
            taller_id = Talleres.objects.filter(id_taller=infoSolicitud.taller_id).values('id_taller')
            usuario_t = UsuariosTalleres.objects.filter(taller_id__in=taller_id)
            lista_usuario_telegram = []
            for usuario in usuario_t:
                lista_usuario_telegram.append(usuario.usuario.usuario_telegram)
            # usuario_telegr = Usuarios.objects.filter(id=usuario_t.usuario_id).first()
            # usuario_telegr = usuario_telegr.usuario_telegram
            enviarTelegram.delay(lista_usuario_telegram, mensaje_telegram)

        if infoSolicitud.pais:
            grupo = 'ws_' + str(infoSolicitud.pais).lower()
        else:
            grupo = 'ws_neutro'
        channel_layer = get_channel_layer()
        print(grupo)
        # print(channel_layer)
        async_to_sync(channel_layer.group_send)(
            grupo,
            {
                'type': 'chat_message',
                'message': 'nuevo registro'
            }
        )
        return JsonResponse({'mensaje': 'correcto'}, status=200)
    return render(request, template_name, contexto)


class SolicitudesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "trn.change_solicitudtrabajo"
    model = SolicitudTrabajo
    template_name = "trn/solicitudes_editar_form.html"
    form_class = SolicitudEditarForm
    context_object_name = "obj"
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        registros = str(form.instance.proveedor.secuencia_solicitudes+1)
        while len(registros) < 5:
            registros = '0' + registros
        secuencia = form.instance.proveedor.identificacion\
            + '-' + registros
        form.instance.secuencia = secuencia
        usuario_op = Usuarios.objects.filter(
            pk=form.instance.usuario_crea).first()
        total_rubros = self.request.POST['total_rubros']
        form.instance.total_rubros = total_rubros
        form.instance.proveedor.secuencia_solicitudes += 1
        form.instance.proveedor.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        rubros_lista = self.request.POST.getlist('rubros_lista[]')
        longitud = len(rubros_lista)
        if longitud > 0:
            rubros = json.loads(rubros_lista[0])
            if rubros:
                for rubro in rubros:
                    id_rubro = rubro.get('id', None)
                    valor = rubro.get('valor', None)
                    infoRubro = SolicitudRubros(
                        rubro_id=id_rubro,
                        valor=valor,
                        solicitud_id=self.object.id_solicitud,
                        usuario_crea=self.request.user.id
                    )
                    if infoRubro:
                        infoRubro.save()
        return reverse('trn:solicitudes_lista')

    def get_context_data(self, **kwargs):
        context = super(SolicitudesEditarView, self).get_context_data(**kwargs)
        id_solicitud = self.kwargs['pk']
        context['detalle'] = DetalleSolicitud.objects.\
            filter(solicitud_id=id_solicitud).first()
        context['sin_talla'] = Tallas.objects.filter(talla=0).first()
        administrador = Usuarios.objects.\
            filter(usuariosgruposempresariales=self.request.user.grupo_empresarial().id_grupo_empresarial).\
            filter(rol_id=3).first()
        context['rubros'] = rubros = RubrosAsociados.objects.\
            filter(usuario_crea=administrador.id)
        peso_max_arc = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_ARCHIVO').first()
        ext_perm_arc = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()
        context['peso_max_arc'] = peso_max_arc
        context['ext_perm_arc'] = ext_perm_arc
        context['imagenes'] = SolicitudesImagenes.objects.\
            filter(solicitud=self.object)
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
        context['proveedores'] = Proveedores.objects.\
            filter(
                pais_id=self.request.user.pais_id,
                taller=taller_neutral.id_taller,
                estado__descripcion='ACTIVO'
            )
        return context

    def get_form_kwargs(self):
        kwargs = super(SolicitudesEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['id_item'] = self.kwargs['pk']
        return kwargs


@login_required(login_url='/login/')
@permission_required('trn.change_solicitudtrabajo',
                     login_url='bases:sin_permisos')
def SolicitudDetalleView(request, id_solicitud=None, accion=None):
    template_name = "trn/detalle_solicitud.html"
    form_rol = {}
    contexto = {}
    costo_color_unitario = 0
    rechazos = {}

    solicitud = SolicitudTrabajo.objects.filter(pk=id_solicitud).first()

    color_solicitud_id = solicitud.color
    if color_solicitud_id == 3:
        costo_color_unitario = 0
    else:
        costo_color_unitario = solicitud.color.costo_adicional_ta

    if request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
        rechazos = ConfiguracionRechazoSolicitudOrdenes.objects.\
            filter(
                taller=request.user.taller(),
                pais=request.user.pais,
                estado_id=1
            )
    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
        rechazos = ConfiguracionRechazoSolicitudOrdenes.objects.\
            filter(
                grupo_empresarial=request.user.grupo_empresarial(),
                pais=request.user.pais,
                estado=1
            )

    item = DetalleSolicitud.objects.\
        filter(solicitud=solicitud).first()
    items = (Items.objects.filter(
        categoria__permite_solicitud=True,
        tipo_catalogo__descripcion=item.item.tipo_catalogo.descripcion,
        taller=solicitud.taller,
        estado__descripcion='ACTIVO'
    )).order_by('descripcion')
    rubros_asociados = SolicitudRubros.objects.\
        filter(solicitud_id=solicitud.id_solicitud)
    costo_total_rubros = 0
    if rubros_asociados:
        for rubro in rubros_asociados:
            costo_total_rubros += rubro.valor

    piedras_solicitud = SolicitudesPiedras.objects.\
        filter(solicitud=solicitud)
    precio_total_piedras_taller = 0
    utilidad_piedras_op = 0
    precio_total_piedras_op = 0

    piedras_lista = []
    piedraLista = []
    if piedras_solicitud:
        for piedra in piedras_solicitud:
            prct_utilidad = piedra.piedra.prct_utilidad_op

            precio_op = piedra.\
                precio_piedra_taller * (1 + (prct_utilidad / 100))
            piedra.prct_utilidad_piedra_op = prct_utilidad
            piedra.precio_piedra_op = precio_op
            subtotal_piedras_op = piedra.cantidad_piedras * precio_op
            piedra.subtotal_piedras_op = subtotal_piedras_op
            piedra.save()
            precio_total_piedras_taller += piedra.subtotal_piedras_taller
            precio_total_piedras_op += subtotal_piedras_op
            detalle_piedra = {
                'piedra': piedra.piedra.descripcion,
                'cantidad': piedra.cantidad_piedras,
                'costo_piedra_taller': str(piedra.costo_piedra_taller),
                'precio_piedra_taller': str(piedra.precio_piedra_taller),
                'precio_piedra_operaciones': str(round(precio_op, 2)),
                'subtotal_piedra_taller': str(piedra.subtotal_piedras_taller),
                'subtotal_piedra_operaciones': str(round(subtotal_piedras_op, 2)),
                'prct_utilidad_operaciones': str(round(prct_utilidad, 2)),
                'utilidad': str(round((float(piedra.subtotal_piedras_op) - float(piedra.subtotal_piedras_taller)), 2)) 

            }
            piedra_detalle={
                'cantidad': piedra.cantidad_piedras,
                'costo': str(piedra.costo_piedra_taller),
                'precio_ta': str(piedra.precio_piedra_taller),
                'utilidadTiendaPrct': str(piedra.prct_utilidad_piedra_op),
                'id_piedra': piedra.piedra_id
            }
            piedraLista.append(piedra_detalle)
            piedras_lista.append(detalle_piedra)

        precio_total_piedras_taller = round(precio_total_piedras_taller, 2)
        precio_total_piedras_op = round(precio_total_piedras_op, 2)
        utilidad_piedras_op = round((precio_total_piedras_op - precio_total_piedras_taller),2)

    # adicionales solicitudes
    adicionales_solicitud = SolicitudesAdicionales.objects.\
        filter(solicitud=solicitud)

    precio_total_adicionales_taller = 0
    utilidad_adicionales_op = 0
    precio_total_adicionales_op = 0
    adicionales_lista = []
    adicionalesLista = []
    if adicionales_solicitud:
        for adicional in adicionales_solicitud:
            prct_utilidad = adicional.adicional.utilidad_operaciones
            precio_op = adicional.\
                precio_adicional_taller * (1 + (prct_utilidad / 100))

            precio_op = round(precio_op, 2)

            adicional.prct_utilidad_adicional_op = prct_utilidad
            adicional.precio_adicional_op = round(precio_op, 2)
            subtotal_adicional_op = adicional.cantidad_adicionales * precio_op
            subtotal_adicional_op = round(subtotal_adicional_op, 2)
            adicional.subtotal_adicional_op = subtotal_adicional_op
            adicional.save()
            precio_total_adicionales_taller += adicional.subtotal_adicional_taller
            precio_total_adicionales_op += subtotal_adicional_op
            detalle_adicional = {
                'adicional': adicional.adicional.descripcion,
                'cantidad_adicionales': adicional.cantidad_adicionales,
                'costo_adicional_taller': str(adicional.costo_adicional_taller),
                'precio_adicional_taller': str(adicional.precio_adicional_taller),
                'precio_adicional_operaciones': str(round(precio_op, 2)),
                'subtotal_adicional_taller': str(adicional.subtotal_adicional_taller),
                'subtotal_adicional_operaciones': str(subtotal_adicional_op),
                'prct_utilidad_operaciones': str(round(prct_utilidad, 2)),
                'utilidad': str(round((float(adicional.subtotal_adicional_op) - float(adicional.subtotal_adicional_taller)), 2))

            }
            adicional_detalle={
                'cantidad': adicional.cantidad_adicionales,
                'costo': str(adicional.costo_adicional_taller),
                'precio_ta': str(adicional.precio_adicional_taller),
                'utilidadTiendaPrct': str(adicional.prct_utilidad_adicional_op),
                'id_adicional': str(adicional.adicional_id)
            }
            adicionalesLista.append(adicional_detalle)
            adicionales_lista.append(detalle_adicional)
        precio_total_adicionales_taller = round(precio_total_adicionales_taller, 2)
        precio_total_adicionales_op = round(precio_total_adicionales_op, 2)
        utilidad_adicionales_op = round((precio_total_adicionales_op - precio_total_adicionales_taller), 2)

    if solicitud.externa:
        config = ConfigUtilidadProveedor.objects.filter(
            proveedor_id=solicitud.proveedor_id,
            id_usuario_op=solicitud.usuario_crea
        ).first()
    else:
        config = ConfigUtilidadTaller.objects.filter(
            id_taller=solicitud.taller_id,
            id_usuario_op=solicitud.usuario_crea
        ).first()
    if config:
        utilidad_fab_op = config.utilidad
    else:
        utilidad_fab_op = solicitud.tienda.sociedad.grupo_empresarial.utilidad_sobre_taller
    configuracion_op = solicitud.tienda.sociedad.grupo_empresarial
    configuracion = solicitud.tienda.sociedad
    configuracion_ta = solicitud.taller
    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
        rubros = RubrosAsociados.objects.\
            filter(
                tipo_rubro=2,
                grupo_id= request.user.grupo_empresarial().id_grupo_empresarial
            )

    else:
        rubros = RubrosAsociados.objects.\
            filter(
                tipo_rubro=1,
                taller_id=request.user.taller().id_taller
            )

    imagenes = SolicitudesImagenes.objects.\
        filter(solicitud_id=solicitud.id_solicitud)

    precio_definido_taller = item.item.categoria.precio_taller_obj()
    precio_definido_op = item.item.categoria.precio_empresa_obj()

    if precio_definido_op:
        prct_util_fabricacion_op = precio_definido_op.prct_utilidad

        precio_unitario_op = precio_definido_op.precio
        regla_calculo_op = precio_definido_op.tipo.regla_calculo.descripcion
    else:
        prct_util_fabricacion_op = configuracion_op.utilidad_sobre_taller
        precio_unitario_op = configuracion_op.precio_gramo_final
        tipo_precio = TiposPrecios.objects.\
            filter(id_tipo=configuracion_op.tipo_precio_predefinido).first()
        regla_calculo_op = tipo_precio.regla_calculo.descripcion

    if request.method == 'GET':
        contexto = {
                    'solicitud': solicitud,
                    'item': item,
                    'utilidad_fab_op': utilidad_fab_op,
                    'configuracion': configuracion,
                    'configuracion_op': configuracion_op,
                    'configuracion_ta': configuracion_ta,
                    'rubros': rubros,
                    'rubros_asociados': rubros_asociados,
                    'imagenes': imagenes,
                    'items': items,
                    'precio_definido_taller': precio_definido_taller,
                    'precio_definido_op': precio_definido_op,
                    'prct_util_fabricacion_op': prct_util_fabricacion_op,
                    'precio_unitario_op': precio_unitario_op,
                    'regla_calculo_op': regla_calculo_op,
                    'piedras_solicitud': piedras_solicitud,
                    'piedras_lista': piedras_lista,
                    'adicionales_lista': adicionales_lista,
                    'adicional_solicitud': adicionales_solicitud,
                    'precio_total_piedras_taller': precio_total_piedras_taller,
                    'utilidad_piedras_op': utilidad_piedras_op,
                    'precio_total_piedras_op': precio_total_piedras_op,
                    'precio_total_adicionales_taller': precio_total_adicionales_taller,
                    'utilidad_adicionales_op': utilidad_adicionales_op,
                    'precio_total_adicionales_op': precio_total_adicionales_op,
                    'piedraLista': piedraLista,
                    'adicionalesLista': adicionalesLista,
                    'costo_total_rubros': costo_total_rubros,
                    'costo_color_unitario': costo_color_unitario,
                    'rechazos': rechazos
                    }

    if request.method == 'POST':
        solicitud = SolicitudTrabajo.objects.filter(pk=id_solicitud).first()

        if solicitud:
            if accion == 1:
                # json_data = json.loads(request.body)
                rubros_lista = request.POST.getlist('rubros_lista[]')
                longitud = len(rubros_lista)
                piedras_lista = request.POST.getlist('piedrasLista[]')
                adicionales_lista = request.POST.getlist('adicionales_lista[]')
                prct_impuestos = solicitud.tienda.sociedad.grupo_empresarial.prct_impuestos

                peso_min = request.POST.get('peso_min', None)
                peso_max = request.POST['peso_max']
                costo_fabricacion_unitario = request.POST['costo_unitario']
                precio_fabricacion_unitario = request.POST['precio_unitario']
                tiempo_ent_min = request.POST['tiempo_ent_min']
                tiempo_ent_max = request.POST['tiempo_ent_max']
                total_rubros = request.POST['total_rubros']
                prct_impuestos_ta = request.POST['prct_impuestos_ta']
                observacion_cotizado = request.POST.get('observacion_cotizado', None)
                id_item = request.POST.get('id_item', None)
                solicitud.peso_min = peso_min
                solicitud.peso_max = peso_max

                solicitud.costo_fabricacion_unitario = costo_fabricacion_unitario
                solicitud.precio_fabricacion_unitario = precio_fabricacion_unitario
                solicitud.total_rubros = total_rubros
                solicitud.tiempo_ent_min = tiempo_ent_min
                solicitud.tiempo_ent_max = tiempo_ent_max
                solicitud.prct_impuestos_ta = prct_impuestos_ta
                solicitud.observacion_cotizado = observacion_cotizado
                solicitud.estado_id = 8
                solicitud.usuario_modifica = request.user.id
                solicitud.fecha_cotizacion = datetime.now(timezone.utc)
                resta_minutos = \
                    round((((
                        solicitud.fecha_cotizacion - solicitud.fecha_creacion)
                        .seconds)/60), 1)
                solicitud.tiempo_cotizacion = resta_minutos
                solicitud.save()
                item.item_id = id_item
                item.usuario_modifica = request.user.id 
                item.save()
                if not solicitud.externa:
                    producto = item.item.descripcion
                    principal = True
                    postergada = False
                    id_transaccion = solicitud.id_solicitud
                    tipo_transaccion = 1
                    tipo_notificacion = 1
                    
                    notificaciones = Notificaciones.objects.filter(taller_id=solicitud.taller_id,
                                                                id_transaccion=solicitud.id_solicitud,
                                                                tipo_transaccion=tipo_transaccion)
                    for n in notificaciones:
                        n.estado_id = 8
                        n.vista = 1
                        n.save()

                    NotificacionSolicitudCotizada.delay(
                        request.user.id,
                        solicitud.tienda_id,
                        solicitud.taller_id,
                        producto,
                        principal,
                        postergada,
                        id_transaccion,
                        tipo_transaccion,
                        solicitud.estado_id,
                        tipo_notificacion
                    )

                if longitud > 0:
                    rubros = json.loads(rubros_lista[0])
                    if rubros:
                        for rubro in rubros:
                            id_rubro = rubro.get('id', None)
                            valor = rubro.get('valor', None)
                            infoRubro = SolicitudRubros(
                                rubro_id=id_rubro,
                                valor=valor,
                                solicitud_id=solicitud.id_solicitud,
                                usuario_crea=request.user.id
                            )
                            if infoRubro:
                                infoRubro.save()

                if len(piedras_lista) > 0:
                    piedras = json.loads(piedras_lista[0])
                    if piedras:
                        for piedra in piedras:
                            infoPiedra = SolicitudesPiedras(
                                solicitud=solicitud,
                                piedra_id=piedra.get('idPiedra'),
                                piedra_detalle_id=piedra.get('idDetalle'),
                                cantidad_piedras=piedra.get('cantidad'),
                                costo_piedra_taller=piedra.get('costoUnitarioPiedraTaller'),
                                precio_piedra_taller=piedra.get('precioUnitarioPiedraTaller'),
                                subtotal_piedras_taller=piedra.get('subtotalPiedraTaller')
                            )
                            if infoPiedra:
                                infoPiedra.save()
                    solicitud.costo_total_piedras_ta = request.\
                        POST['costoTotalPiedrasTaller']
                    solicitud.precio_total_piedras_ta = request.\
                        POST['precioTotalPiedrasTaller']
                    solicitud.save()
                if len(adicionales_lista) > 0:
                    adicionales = json.loads(adicionales_lista[0])
                    if adicionales:
                        for adicional in adicionales:
                            infoAdicional = SolicitudesAdicionales(
                                solicitud=solicitud,
                                adicional_id=adicional.get('id'),
                                cantidad_adicionales=adicional.get('cantidad'),
                                costo_adicional_taller=adicional.get('costo'),
                                precio_adicional_taller=adicional.get('precio_ta'),
                                subtotal_adicional_taller=adicional.get('subtotal_ta')
                            )
                            if infoAdicional:
                                infoAdicional.save()

            if accion == 2:
                json_data = json.loads(request.body)
                tiempo_dias = json_data['tiempo_dias']
                tiempo_horas = json_data['tiempo_horas']
                tiempo_minutos = json_data['tiempo_minutos']
                tiempo_respuesta = \
                    datetime.now(timezone.utc) + \
                    timedelta(days=int(tiempo_dias))
                tiempo_respuesta = \
                    tiempo_respuesta + \
                    timedelta(hours=int(float(tiempo_horas)))
                tiempo_respuesta = \
                    tiempo_respuesta + \
                    timedelta(minutes=int(tiempo_minutos))
                solicitud.estado_id = 4
                solicitud.tiempo_respuesta = tiempo_respuesta
                solicitud.usuario_modifica = request.user.id

                kwargs = {'id_transaccion': solicitud.id_solicitud, 'user': request.user.id}
                kwargs = json.dumps(kwargs)

                # zona_horaria = request.user.pais.zona_horaria
                nombre_tarea = 'evaluarsolicitud_' + str(request.user.id) + \
                    '_' + str(solicitud.id_solicitud)

                periodo, _ = CrontabSchedule.objects.get_or_create(
                    minute=tiempo_respuesta.minute,
                    hour=tiempo_respuesta.hour,
                    day_of_week='*',
                    day_of_month=tiempo_respuesta.day,
                    month_of_year=tiempo_respuesta.month
                    # timezone=zona_horaria
                )

                tarea = PeriodicTask.objects.filter(
                    name=nombre_tarea
                ).first()

                if tarea:
                    tarea.crontab = periodo
                    tarea.kwargs = kwargs
                    tarea.save()
                else:
                    PeriodicTask.objects.create(
                        crontab=periodo,
                        name=nombre_tarea,
                        task='ntf.tasks.NotificacionEvaluarSolicitud',
                        kwargs=kwargs
                    )
                solicitud.save()
                if not solicitud.externa:
                    producto = item.item.descripcion
                    principal = True
                    postergada = False
                    id_transaccion = solicitud.id_solicitud
                    tipo_transaccion = 1
                    tipo_notificacion = 1
                    notificaciones = Notificaciones.objects.filter(taller_id=solicitud.taller_id,
                                                                id_transaccion=solicitud.id_solicitud,
                                                                tipo_transaccion=tipo_transaccion)
                    for n in notificaciones:
                        n.estado_id = 4
                        n.vista = 1
                        n.save()

                    NotificacionSolicitudCotizada.delay(
                        request.user.id,
                        solicitud.tienda_id,
                        solicitud.taller_id,
                        producto,
                        principal,
                        postergada,
                        id_transaccion,
                        tipo_transaccion,
                        solicitud.estado_id,
                        tipo_notificacion
                    )
            if accion == 3:
                json_data = json.loads(request.body)
                observacion_id = json_data['id_observacion']
                observacion_adicional = json_data['observacion_adicional']
                obs_objeto = ConfiguracionRechazoSolicitudOrdenes.\
                    objects.filter(id_obs_rechazo=observacion_id).first()
                reenvio = False
                if request.user.tipo_usuario_id == 2:
                    solicitud.estado_id = 5
                    solicitud.observacion_rechazo_ta = observacion_adicional
                    solicitud.rechazo_id = observacion_id
                    reenvio = reenviarSolicitud(solicitud.id_solicitud, request.user.pais_id)
                if request.user.tipo_usuario_id == 3:
                    solicitud.estado_id = 9
                    solicitud.rechazo_id = observacion_id
                    solicitud.observacion_rechazo_op = observacion_adicional
                solicitud.usuario_modifica = request.user.id
                solicitud.save()
                if not solicitud.externa and not reenvio:
                    tipo_transaccion = 1
                    notificaciones = Notificaciones.objects.filter(taller_id=solicitud.taller_id,
                                                                id_transaccion=solicitud.id_solicitud,
                                                                tipo_transaccion=tipo_transaccion)
                    for n in notificaciones:
                        n.estado_id = 5
                        n.vista = 1
                        n.save()

                    producto = item.item.descripcion
                    principal = True
                    postergada = False
                    id_transaccion = solicitud.id_solicitud
                    tipo_notificacion = 2
                    NotificacionSolicitudCotizada.delay(
                        request.user.id,
                        solicitud.tienda_id,
                        solicitud.taller_id,
                        producto,
                        principal,
                        postergada,
                        id_transaccion,
                        tipo_transaccion,
                        solicitud.estado_id,
                        tipo_notificacion
                    )

    return render(request, template_name, contexto)



class GenerarOrdenSolicitudView(APIView):
    def post(self, request, pk=None):
        solicitud = SolicitudTrabajo.objects.filter(id_solicitud=pk).first()
        serializador = GenerarOrdenSerializer(solicitud, data=request.data)
        if serializador.is_valid():
            print('serializer')
            print(serializador)
            datos = request.data
            costo_color_unitario = float(datos['costo_color_unitario'])
            costo_color_total = float(datos['costo_color_total'])
            peso_solicitado = float(datos['peso_solicitado'])

            peso_materia_dividida = float(datos['peso_materia_dividida'])

            costo_gramo_base_taller = float(datos['costo_gramo_base_taller'])
            precio_gramo_base_taller = float(datos['precio_gramo_base_taller'])
            prct_utilidad_base_taller = float(datos['prct_utilidad_base_taller'])
            costo_base_total_ta = float(datos['costo_base_total_ta'])
            utilidad_base_taller = float(datos['utilidad_base_taller'])
            precio_base_total_ta = float(datos['precio_base_total_ta'])
            costo_unitario_taller = float(datos['costo_unitario_taller'])
            costo_total_fabricacion_ta = float(
                datos['costo_total_fabricacion_ta'])
            prct_util_fabricacion_taller = float(
                datos['prct_util_fabricacion_taller'])
            utilidad_fabricacion_taller = float(
                datos['utilidad_fabricacion_taller'])
            precio_unitario_taller = float(datos['precio_unitario_taller'])
            precio_fabricacion_total = float(
                datos['precio_fabricacion_total_ta'])
            # precio_fabricacion_total = float(
            #     datos['precio_fabricacion_total'])
            total_rubros = float(datos['total_rubros'])
            subtotal_taller = float(datos['subtotal_taller'])
            prct_impuestos_taller = float(datos['prct_impuestos_taller'])
            impuestos_taller = float(datos['impuestos_taller'])
            total_taller = float(datos['total_taller'])

            costo_gramo_base_op = float(datos['costo_gramo_base_op'])
            precio_gramo_base_op = float(datos['precio_gramo_base_op'])
            
            costo_base_total_op = float(datos['costo_base_total_op'])
            prct_utilidad_base_op = float(datos['prct_utilidad_base_op'])
            utilidad_base_op = float(datos['utilidad_base_op'])
            precio_base_total_op = float(datos['precio_base_total_op'])
            prct_util_fabricacion_op = float(datos['prct_util_fabricacion_op'])
            precio_unitario_op = float(datos['precio_unitario_op'])
            utilidad_fabricacion_op = float(datos['utilidad_fabricacion_op'])
            precio_fabricacion_total_op = float(
                datos['precio_fabricacion_total_op'])
            subtotal_op = float(datos['subtotal_op'])
            impuestos_op = float(datos['impuestos_op'])
            total_fabricacion_op = float(datos['total_fabricacion_op'])
            subtotal_solicitud = float(datos['subtotal_solicitud'])
            prct_impuestos_joyeria = float(datos['prct_impuestos_joyeria'])
            impuestos_solicitud = float(datos['impuestos_solicitud'])
            precio_sistema = float(datos['precio_sistema'])
            descuento = float(datos['descuento'])
            precio_final_solicitud = float(datos['precio_final_solicitud'])
            # util_sobre_piedras_op = float(datos['util_sobre_piedras_op'])
            # util_sobre_adicionales_op = float(datos['util_sobre_adicionales_op'])
            print('******')
            peso_cliente = datos['peso_cliente']
            print(peso_cliente)
            origen_materia = datos['origen_material_dividido']
            fabricacion_dividida = datos['fabricacion_dividida']
            # if peso_cliente:
            #     peso_materiaDividida = (float(peso_materia_dividida) - float(peso_cliente))


            origen_materia = OrigenMaterial.objects.filter(id_origen=origen_materia).first()


            solicitud.peso_solicitado = peso_solicitado
            solicitud.costo_gramo_base_taller = costo_gramo_base_taller
            solicitud.precio_gramo_base_taller = precio_gramo_base_taller
            solicitud.prct_utilidad_base_taller = prct_utilidad_base_taller
            solicitud.utilidad_base_taller = utilidad_base_taller
            solicitud.costo_base_total_ta = costo_base_total_ta
            solicitud.precio_base_total_ta = precio_base_total_ta
            solicitud.costo_fabricacion_unitario = costo_unitario_taller
            solicitud.precio_fabricacion_unitario = precio_unitario_taller
            solicitud.costo_total_fabricacion_ta = costo_total_fabricacion_ta
            solicitud.precio_fabricacion_total = precio_fabricacion_total
            solicitud.prct_util_sobre_fabrica_ta = prct_util_fabricacion_taller
            solicitud.util_sobre_fabrica_ta = utilidad_fabricacion_taller


            # solicitud.util_sobre_adicionales_op = util_sobre_adicionales_op
            # solicitud.util_sobre_piedras_op = util_sobre_piedras_op

            solicitud.total_rubros = total_rubros
            solicitud.subtotal_taller = subtotal_taller
            solicitud.prct_impuestos_ta = prct_impuestos_taller
            solicitud.impuestos_taller = impuestos_taller
            solicitud.total_taller = total_taller

            solicitud.costo_gramo_base_op = costo_gramo_base_op
            solicitud.precio_gramo_base_op = precio_gramo_base_op

            solicitud.prct_util_sobre_base_op = prct_utilidad_base_op
            solicitud.costo_base_total_op = costo_base_total_op
            solicitud.precio_base_total_op = precio_base_total_op
            solicitud.util_sobre_base_op = utilidad_base_op
            solicitud.prct_util_sobre_fabrica_op = prct_util_fabricacion_op
            solicitud.util_sobre_fabrica_op = utilidad_fabricacion_op
            solicitud.precio_unitario_op = precio_unitario_op
            solicitud.precio_fabricacion_total_op = precio_fabricacion_total_op
            solicitud.subtotal_solicitud = subtotal_solicitud
            solicitud.prct_impuestos_op = prct_impuestos_joyeria
            solicitud.impuestos_op = impuestos_solicitud
            solicitud.descuento_solicitud = descuento
            solicitud.precio_sistema = precio_sistema
            solicitud.precio_final_venta = precio_final_solicitud

            solicitud.peso_materia_dividida = peso_materia_dividida
            solicitud.fabricacion_dividida = fabricacion_dividida
            solicitud.origen_material_dividido = origen_materia
            solicitud.peso_cliente_dividido = peso_cliente

            solicitud.usuario_modifica = request.user.id
            solicitud.save()

            serializador.save()
            return Response(serializador.data, status=200)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=400)


class SolicitarAExternoView(APIView):
    parser_classes = [JSONParser]
    def post(self, request, pk=None):
        solicitud = SolicitudTrabajo.objects.filter(id_solicitud=pk).first()
        taller_neutro = Talleres.objects.filter(nombre='NEUTRO').first()
        serializador = SolicitarAExternoSerializer(solicitud,
                                                   data=request.data)
        proveedores = Proveedores.objects.filter(
            taller=1,
            pais_id=self.request.user.pais_id
        ).count()
        if proveedores > 0:
            if serializador.is_valid():
                solicitud.usuario_modifica = request.user.id
                solicitud.generado_con_ext = True
                solicitud.save()
                nueva_solicitud = SolicitudTrabajo(
                    longitud=solicitud.longitud,
                    externa=True,
                    acabado=solicitud.acabado,
                    parte_interna=solicitud.parte_interna,
                    cantidad_piedras=solicitud.cantidad_piedras,
                    sku_relacionado=solicitud.sku_relacionado,
                    detalle=solicitud.detalle,
                    color_id=solicitud.color_id,
                    estado_id=6,
                    pais_id=solicitud.pais_id,
                    proveedor_id=solicitud.proveedor_id,
                    talla_id=solicitud.talla_id,
                    taller_id=taller_neutro.id_taller,
                    # usuario_id=request.user.id,
                    usuario_crea=request.user.id,
                    origen_material=solicitud.origen_material,
                    solicitud_relacionada=solicitud.secuencia
                )
                if nueva_solicitud:
                    nueva_solicitud.save()
                    detalles_solicitud = DetalleSolicitud.objects.\
                        filter(solicitud_id=solicitud.id_solicitud)
                    if detalles_solicitud:
                        for detalle in detalles_solicitud:
                            if detalle.solicitud_id:
                                if detalle.item.tipo_catalogo.\
                                     descripcion == 'PRODUCTOS':
                                    item = Items.objects.\
                                        filter(sku='PRO-GEN-001').first()
                                else:
                                    item = Items.objects.\
                                        filter(sku='SER-GEN-001').first()
                                nuevo_detalle = DetalleSolicitud(
                                    solicitud_id=nueva_solicitud.id_solicitud,
                                    item=item,
                                    pais_id=nueva_solicitud.pais_id,
                                    usuario_crea=request.user.id
                                )
                            if nuevo_detalle:
                                nuevo_detalle.save()
                    imagenes = SolicitudesImagenes.objects.\
                        filter(solicitud=solicitud)
                    for imagen in imagenes:
                        infoImg = SolicitudesImagenes(
                            usuario_crea=request.user.id,
                            imagen=imagen.imagen,
                            solicitud=nueva_solicitud,
                            pais=request.user.pais
                        )
                        if infoImg:
                            infoImg.save()

                    solicitud_nueva = {
                        "id_solicitud": str(nueva_solicitud.id_solicitud)
                    }
                serializador.save()
                return Response(solicitud_nueva, status=200)

            else:
                return Response(serializador.errors, status=400)
        else:
            solicitud_nueva = {
                "id_solicitud": str(0)
            }
            return Response(solicitud_nueva, status=200)


def reenviarSolicitud(id_solicitud, pais_id):
    solicitud = SolicitudTrabajo.objects.\
        filter(id_solicitud=id_solicitud).first()
    prioridad = int(solicitud.taller.prioridad) + 1

    while solicitud:

        # try:
        taller = Talleres.objects.\
            filter(prioridad=prioridad, pais_id=pais_id).first()
        # except Taller.DoesNotExist:
        #     return False

        print(taller)
        print('taller inactivo?')
        if taller and taller.estado_id == 2 :
            print('si')
            print('siguiente taller...')
            prioridad += 1
        else:
            print('no')
            break

    if taller:
        registros = str(taller.secuencia_solicitudes+1)
        while len(registros) < 5:
            registros = '0' + registros
        secuencia = taller.nombre + '-' + registros
        nueva_solicitud = SolicitudTrabajo(
            secuencia=secuencia,
            longitud=solicitud.longitud,
            externa=solicitud.externa,
            acabado=solicitud.acabado,
            parte_interna=solicitud.parte_interna,
            cantidad_piedras=solicitud.cantidad_piedras,
            sku_relacionado=solicitud.sku_relacionado,
            detalle=solicitud.detalle,
            color_id=solicitud.color_id,
            estado=solicitud.estado,
            pais_id=solicitud.pais_id,
            proveedor_id=solicitud.proveedor_id,
            talla_id=solicitud.talla_id,
            taller_id=taller.id_taller,
            tienda_id=solicitud.tienda_id,
            usuario_crea=solicitud.usuario_crea,
            origen_material=solicitud.origen_material,
            solicitud_relacionada=solicitud.secuencia
        )
        if nueva_solicitud:
            nueva_solicitud.save()
            detalles_solicitud = DetalleSolicitud.objects.\
                filter(solicitud_id=solicitud.id_solicitud)
            if detalles_solicitud:
                for detalle in detalles_solicitud:
                    if detalle.solicitud_id:
                        if detalle.item.tipo_catalogo.\
                                descripcion == 'PRODUCTOS':
                            item = Items.objects.\
                                filter(sku='PRO-GEN-001').first()
                        else:
                            item = Items.objects.\
                                filter(sku='SER-GEN-001').first()
                        nuevo_detalle = DetalleSolicitud(
                            solicitud_id=nueva_solicitud.id_solicitud,
                            item=item,
                            pais_id=nueva_solicitud.pais_id,
                            usuario_crea=solicitud.usuario_crea
                        )
                    if nuevo_detalle:
                        nuevo_detalle.save()
            imagenes = SolicitudesImagenes.objects.\
                filter(solicitud=solicitud)
            if imagenes:
                for imagen in imagenes:
                    infoImg = SolicitudesImagenes(
                        usuario_crea=solicitud.usuario_crea,
                        imagen=imagen.imagen,
                        solicitud=nueva_solicitud,
                        pais=nueva_solicitud.pais
                    )
                    if infoImg:
                        infoImg.save()
            NotificacionSolicitudActualizar.delay(
                solicitud.taller_id,
                solicitud.id_solicitud,
                1,
                5
            )
            taller = nueva_solicitud.taller_id
            producto = nuevo_detalle.item.descripcion
            principal = True
            postergada = False
            id_transaccion = nueva_solicitud.id_solicitud
            tipo_transaccion = 1
            tipo_notificacion = 2
            NotificacionSolicitudCreada.delay(
                nueva_solicitud.usuario_crea,
                nueva_solicitud.tienda_id,
                taller,
                producto,
                principal,
                postergada,
                id_transaccion,
                tipo_transaccion,
                nueva_solicitud.estado_id,
                tipo_notificacion
            )
            # enviarSms.delay(nueva_solicitud.id_solicitud, 2)
            mensaje_telegram = "Se ha generado una Solicitud con la secuencia {}, y solicitada por la tienda '{}'.".format(nueva_solicitud.secuencia, nueva_solicitud.tienda)
            taller_id = Talleres.objects.filter(id_taller=nueva_solicitud.taller_id).values('id_taller')
            usuario_t = UsuariosTalleres.objects.filter(taller_id__in=taller_id)
            lista_usuario_telegram = []
            for usuario in usuario_t:
                lista_usuario_telegram.append(usuario.usuario.usuario_telegram)
            print(lista_usuario_telegram)
            # usuario_telegr = Usuarios.objects.filter(id=usuario_t.usuario_id).first()
            # usuario_telegr = usuario_telegr.usuario_telegram
            enviarTelegram.delay(lista_usuario_telegram, mensaje_telegram)
            return True
    else:

        return False


class OrdenesListaView(SinPermisos, generic.ListView):
    permission_required = "trn.view_ordentrabajo"
    model = OrdenTrabajo
    template_name = "trn/ordenes_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        usuario=self.request.user
        tiendas= UsuariosTiendas.objects.filter(usuario=usuario).values('tienda_id')

        if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
            return OrdenTrabajo.objects.\
                filter(tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial())
        if self.request.user.rol.zonal == True:
            return OrdenTrabajo.objects.filter(tienda__zona_id=self.request.user.zona)

        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES': 
            return OrdenTrabajo.objects.filter(tienda__in=tiendas)
        else:
            return OrdenTrabajo.objects.filter(taller=self.request.user.taller())

    def get_context_data(self, **kwargs):
        context = super(OrdenesListaView, self).get_context_data(**kwargs)
        context['peso_max_arc'] = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_ARCHIVO').first()
        context['ext_perm_arc'] = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()
        context['ext_perm_img'] = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['peso_max_img'] = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        context['cantidad_max_img'] = ConfiguracionSistema.objects.\
            filter(clave='CANTIDAD_MAX_IMAGENES').first()
        context['PESO_MAX_DATA'] = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        return context





def ObtenerOrdenesPagos(filtros, talleres, zonas, user):

    estado_pendiente = filtros.get('estadoPendiente')
    estado_aprobado = filtros.get('estadoAprobado')
    estado_facturado = filtros.get('estadoFacturado')
    estado_revisado = filtros.get('estadoRevisado')
    estado_pagado = filtros.get('estadoPagado')
    clave_busqueda = filtros.get('claveBusqueda')
    f_inicio = filtros.get('fechaInicio')
    f_fin = filtros.get('fechaFin')
    opcion = filtros.get('opcion')

    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    if opcion == 1:
        f_inicio = dia_uno_mes_actual
        f_fin = ahora
    if opcion == 2:
        f_inicio = dia_uno_mes_anterior
        f_fin = dia_uno_mes_actual
    if opcion == 3:
        f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
        f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
    if opcion == 4:
        f_inicio = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
        f_fin = ahora
    
    id_tiendas = UsuariosTiendas.objects.filter(usuario_id=user.id).values('tienda_id')
    if user.tipo_usuario.descripcion != 'USUARIO OPERACIONES':
        print('usuario taller')
        ordenes_aprobadas = OrdenTrabajo.objects.\
            filter(
                # tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                taller__in=talleres,
                pago_aprobado=True,
                pais=user.pais
            ).exclude(
                orden_facturada=True
            )

        if clave_busqueda != '':
            ordenes_aprobadas = ordenes_aprobadas.\
                filter(
                    tienda__nombre__icontains=clave_busqueda
                ) | ordenes_aprobadas.\
                filter(
                    secuencia__icontains=clave_busqueda
                )
        ordenes_facturadas = OrdenTrabajo.objects.\
            filter(
                # tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                taller__in=talleres,
                fecha_creacion__gte=f_inicio,
                fecha_creacion__lte=f_fin,
                orden_facturada=True,
                pais=user.pais
            ).exclude(
                orden_pagada=True
            )
        if clave_busqueda != '':
            ordenes_facturadas = ordenes_facturadas.\
                filter(
                    tienda__nombre__icontains=clave_busqueda
                ) | ordenes_facturadas.\
                filter(
                    secuencia__icontains=clave_busqueda
                ) | ordenes_facturadas.\
                filter(
                    numero_factura__icontains=clave_busqueda
                )

        ordenes_pagadas = OrdenTrabajo.objects.\
            filter(
                # tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                taller__in=talleres,
                fecha_creacion__gte=f_inicio,
                fecha_creacion__lte=f_fin,
                orden_pagada=True,
                pais=user.pais
            )
        if clave_busqueda != '':
            ordenes_pagadas = ordenes_pagadas.\
                filter(
                    tienda__nombre__icontains=clave_busqueda
                ) | ordenes_pagadas.\
                filter(
                    secuencia__icontains=clave_busqueda
                ) | ordenes_pagadas.\
                filter(
                    numero_factura__icontains=clave_busqueda
                )
        ordenes_pendientes = OrdenTrabajo.objects.\
            filter(
                # tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                taller__in=talleres,
                fecha_creacion__gte=f_inicio,
                fecha_creacion__lte=f_fin,
                estado__descripcion__in=['PRODUCTO RECIBIDO', 'FINALIZADO'],
                pais=user.pais
            ).exclude(
                pago_aprobado=True
            )
        if clave_busqueda != '':
            ordenes_pendientes = ordenes_pendientes.\
                filter(
                    tienda__nombre__icontains=clave_busqueda
                ) | ordenes_pendientes.\
                filter(
                    secuencia__icontains=clave_busqueda
                )

    else:
        print('usuario operaciones')
        id_tiendas = UsuariosTiendas.objects.filter(usuario_id=user.id).values('tienda_id')
        if user.rol.admin == True:
            ordenes_aprobadas = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                    taller__in=talleres,
                    pago_aprobado=True
                ).exclude(
                    orden_facturada=True
                )

            if clave_busqueda != '':
                ordenes_aprobadas = ordenes_aprobadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_aprobadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    )
            ordenes_facturadas = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    orden_facturada=True,
                    pais=user.pais
                ).exclude(
                    orden_pagada=True
                )
            if clave_busqueda != '':
                ordenes_facturadas = ordenes_facturadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_facturadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    ) | ordenes_facturadas.\
                    filter(
                        numero_factura__icontains=clave_busqueda
                    )

            ordenes_pagadas = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    orden_pagada=True,
                    pais=user.pais
                )
            if clave_busqueda != '':
                ordenes_pagadas = ordenes_pagadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_pagadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    ) | ordenes_pagadas.\
                    filter(
                        numero_factura__icontains=clave_busqueda
                    )
            ordenes_pendientes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=user.grupo_empresarial(),
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    estado__descripcion__in=['PRODUCTO RECIBIDO', 'FINALIZADO'],
                    pais=user.pais
                ).exclude(
                    pago_aprobado=True
                )
            if clave_busqueda != '':
                ordenes_pendientes = ordenes_pendientes.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_pendientes.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    )
        else:
            ordenes_aprobadas = OrdenTrabajo.objects.\
                filter(
                    tienda_id__in=id_tiendas,
                    taller__in=talleres,
                    pago_aprobado=True
                ).exclude(
                    orden_facturada=True
                )

            if clave_busqueda != '':
                ordenes_aprobadas = ordenes_aprobadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_aprobadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    )
            ordenes_facturadas = OrdenTrabajo.objects.\
                filter(
                    tienda_id__in=id_tiendas,
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    orden_facturada=True,
                    pais=user.pais
                ).exclude(
                    orden_pagada=True
                )
            if clave_busqueda != '':
                ordenes_facturadas = ordenes_facturadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_facturadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    ) | ordenes_facturadas.\
                    filter(
                        numero_factura__icontains=clave_busqueda
                    )

            ordenes_pagadas = OrdenTrabajo.objects.\
                filter(
                    tienda_id__in=id_tiendas,
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    orden_pagada=True,
                    pais=user.pais
                )
            if clave_busqueda != '':
                ordenes_pagadas = ordenes_pagadas.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_pagadas.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    ) | ordenes_pagadas.\
                    filter(
                        numero_factura__icontains=clave_busqueda
                    )
            ordenes_pendientes = OrdenTrabajo.objects.\
                filter(
                    tienda_id__in=id_tiendas,
                    taller__in=talleres,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin,
                    estado__descripcion__in=['PRODUCTO RECIBIDO', 'FINALIZADO'],
                    pais=user.pais
                ).exclude(
                    pago_aprobado=True
                )
            if clave_busqueda != '':
                ordenes_pendientes = ordenes_pendientes.\
                    filter(
                        tienda__nombre__icontains=clave_busqueda
                    ) | ordenes_pendientes.\
                    filter(
                        secuencia__icontains=clave_busqueda
                    )


    ordenes = OrdenTrabajo.objects.none()
    if (
         not estado_pendiente
         and not estado_aprobado
         and not estado_facturado
         and not estado_pagado):
        ordenes = ordenes.union(
            ordenes_pendientes,
            ordenes_aprobadas,
            ordenes_facturadas,
            ordenes_pagadas)
    else:
        if estado_pendiente:
            ordenes = ordenes | ordenes_pendientes
        if estado_aprobado:
            ordenes = ordenes | ordenes_aprobadas
        if estado_facturado:
            ordenes = ordenes | ordenes_facturadas
        if estado_revisado:
            ordenes = ordenes | ordenes_revisadas
        if estado_pagado:
            ordenes = ordenes | ordenes_pagadas
    return ordenes.order_by('-fecha_creacion')




class OrdenesListaAPIView(APIView):
    def get(self, request, limite):
        if self.request.user.tipo_usuario == 'USUARIO OPERACIONES':
            if limite == 10:
                ordenes = OrdenTrabajo.objects.\
                    filter(tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()).\
                    order_by('-fecha_modificacion')[:limite]
            else:
                ordenes = OrdenTrabajo.objects.\
                    filter(tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()).\
                    order_by('-fecha_modificacion')
        else:
            if limite == 10:
                ordenes = OrdenTrabajo.objects.\
                    filter(taller=self.request.user.taller()).\
                    order_by('-fecha_modificacion')[:limite]
            else:
                ordenes = OrdenTrabajo.objects.\
                    filter(taller=self.request.user.taller()).\
                    order_by('-fecha_modificacion')
        data = OrdenesSerializer(ordenes, many=True).data
        return Response(data)


class OrdenesListaFechaAPIView(APIView):
    def get(self, request, f_inicio, f_fin, opcion):
        tiendas= UsuariosTiendas.objects.filter(usuario=self.request.user).values('tienda_id')
        ahora = datetime.now(timezone.utc)
        dia_uno_mes_actual = ahora.replace(
            day=1,
            hour=0,
            minute=0,
            second=0
            )
        dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
        dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
            day=1,
            hour=0,
            minute=0,
            second=0
            )
        f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
        f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            if opcion == 1:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial(),
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                                fecha_creacion__gte=dia_uno_mes_actual,
                                fecha_creacion__lte=ahora
                            ).order_by('-fecha_modificacion')
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=dia_uno_mes_actual,
                                fecha_creacion__lte=ahora
                            ).order_by('-fecha_modificacion')
            if opcion == 2:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                                fecha_creacion__gte=dia_uno_mes_anterior,
                                fecha_creacion__lte=dia_uno_mes_actual
                            ).order_by('-fecha_modificacion')
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=dia_uno_mes_anterior,
                                fecha_creacion__lte=dia_uno_mes_actual
                            ).order_by('-fecha_modificacion')
            if opcion == 3:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=self.request.user.grupo_empresarial()
                        ).order_by('-fecha_modificacion')[:100]
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona
                            ).order_by('-fecha_modificacion')[:100]
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas
                            ).order_by('-fecha_modificacion')[:100]

                
            if opcion == 4:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        ).order_by('-fecha_modificacion')[:1000]
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona
                            ).order_by('-fecha_modificacion')[:1000]
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas
                            ).order_by('-fecha_modificacion')[:1000]
            if opcion == 5:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona,
                                fecha_creacion__gte=f_inicio,
                                fecha_creacion__lte=f_fin + timedelta(days=1)
                            ).order_by('-fecha_modificacion')
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                                fecha_creacion__gte=f_inicio,
                                fecha_creacion__lte=f_fin + timedelta(days=1)
                            ).order_by('-fecha_modificacion')
            if opcion == 6:
                if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        ).order_by('-fecha_modificacion')
                else:
                    if self.request.user.rol.zonal:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__zona_id=self.request.user.zona
                            ).order_by('-fecha_modificacion')
                    else:
                        ordenes = OrdenTrabajo.objects.\
                            filter(
                                tienda__in=tiendas,
                            ).order_by('-fecha_modificacion')
        else:
            # id_t = Talleres.objects.filter(pais_id=self.request.user.pais_id).first()

            if opcion == 1:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller(),
                        fecha_creacion__gte=dia_uno_mes_actual,
                        fecha_creacion__lte=ahora
                    ).order_by('-fecha_modificacion')
            if opcion == 2:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller(),
                        fecha_creacion__gte=dia_uno_mes_anterior,
                        fecha_creacion__lte=dia_uno_mes_actual
                    ).order_by('-fecha_modificacion')
            if opcion == 3:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')[:100]
            if opcion == 4:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')[:1000]
            if opcion == 5:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller(),
                        fecha_creacion__gte=f_inicio,
                        fecha_creacion__lte=f_fin + timedelta(days=1)
                    ).order_by('-fecha_modificacion')
            if opcion == 6:
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        taller=self.request.user.taller()
                    ).order_by('-fecha_modificacion')
        data = OrdenesSerializer(ordenes, many=True).data
        return Response(data)


class OrdenesPagosListaView(SinPermisos, generic.TemplateView):
    permission_required = "trn.view_ordentrabajo"
    template_name = "trn/ordenes_pagos_lista.html"
    login_url = "bases:login"


class OrdenesPagosListaAPIView(APIView):
    def post(self, request):
        # body = json.loads(self.request.body)
        body = self.request.body
        body = json.loads(body)
        talleres_internos = body.get('talleresInternos')
        talleres_externos = body.get('talleresExternos')
        print('talleres/*/*/*/*/')
        print(talleres_internos)
        print(talleres_externos)
        print('********ordenes pagos****************')
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            talleres_id = Talleres.objects.\
                filter(
                    nombre=self.request.user.taller(),
                    pais_id=self.request.user.pais_id
                ).\
                values('id_taller')
            zonas_id = Zonas.objects.\
                filter(
                    id_zona=self.request.user.zona,
                    estado__descripcion='ACTIVO'
                ).\
                values('id_zona')
            # print(talleres_id)
            # print(zonas_id)
        else:
            if (talleres_internos and talleres_externos) or\
                 (not talleres_internos and not talleres_externos):
                talleres_id = Talleres.objects.\
                    filter(
                        pais=self.request.user.pais,
                        estado__descripcion='ACTIVO'
                    ).\
                    values('id_taller') | Talleres.objects.\
                    filter(
                        nombre='NEUTRO'
                    ).values('id_taller')
                
            elif talleres_internos:
                talleres_id = Talleres.objects.\
                    filter(
                        pais=self.request.user.pais,
                        estado__descripcion='ACTIVO'
                    ).\
                    values('id_taller')
                
            else:
                talleres_id = Talleres.objects.\
                    filter(
                        nombre='NEUTRO'
                    ).values('id_taller')
                
            if self.request.user.rol.zonal:
                zonas_id = Zonas.objects.\
                    filter(
                        id_zona=self.request.user.zona
                    ).\
                    values('id_zona')
                
            else:
                zonas_id = Zonas.objects.\
                    filter(
                        id_zona=self.request.user.zona,
                        grupo_empresarial_id=self.request.user.grupo_empresarial().id_grupo_empresarial,
                        estado__descripcion='ACTIVO'
                    ).\
                    values('id_zona')
                
        # print(talleres_id)
        # print(zonas_id)
        ordenes = ObtenerOrdenesPagos(
            body,
            talleres_id,
            zonas_id,
            self.request.user)
        # print(ordenes)
        if ordenes:
            data = OrdenesSerializer(ordenes, many=True).data
        else:
            data = None
        return Response(data)



class TipoOrdenView(generic.TemplateView):
    template_name = "trn/tipo_orden_modal.html"
    login_url = "bases:login"


@login_required(login_url='/login/')
@permission_required('trn.add_ordentrabajo',
                     login_url='bases:sin_permisos')
def CrearOrdenSolicitudView(request, id_trn=None, identificacion=None):
    template_name = "trn/ordenes_solicitud_crear.html"
    form_rol = {}
    contexto = {}

    solicitud = SolicitudTrabajo.objects.filter(pk=id_trn).first()
    color_solicitud_id = solicitud.color 
    if color_solicitud_id == 0:
        costo_color_unitario = 0
    else:
        costo_color_unitario = color_solicitud_id.costo_adicional_ta

    cliente = Clientes.objects.filter(identificacion=identificacion).\
        first()
    imagenes = SolicitudesImagenes.objects.filter(solicitud=solicitud)
    # tienda_user = UsuariosTiendas.objects.filter(usuario_id=request.user.id).first()
    ext_perm_arc = ConfiguracionSistema.objects.filter(clave='EXT_PERMITIDAS_IMAGEN').first()
    if request.method == 'GET':
        contexto = {
                    'solicitud': solicitud,
                    'cliente': cliente,
                    'imagenes': imagenes,
                    'ext_perm_arc': ext_perm_arc,
                    'costo_color_unitario': costo_color_unitario
                    }

    if request.method == 'POST':
        # json_data = json.loads(request.body)
        # env_material = json_data['env_material']
        env_material = request.POST['env_material']
        if env_material == 'false':
            env_material = False
        else:
            env_material = True
        registros = OrdenTrabajo.objects.\
            filter(taller=solicitud.taller).count()
        detalle_solicitud = DetalleSolicitud.objects.\
            filter(solicitud=solicitud).first()
        if env_material:
            estado = 12
        else:
            estado = 20

        if solicitud:
            if solicitud.externa:
                registros = str(solicitud.proveedor.secuencia_ordenes+1)
            else:
                registros = str(solicitud.taller.secuencia_ordenes+1)
            while len(registros) < 5:
                registros = '0' + registros
            if solicitud.externa:
                secuencia = solicitud.proveedor.identificacion\
                    + '-' + registros
            else:
                secuencia = solicitud.taller.nombre + '-' + registros
            piedras_solicitud = SolicitudesPiedras.objects.\
                filter(solicitud=solicitud)
            
            # agregar adicionales al crear la orden desde una solicitud
            solicitudes_adicionales = SolicitudesAdicionales.objects.\
                filter(solicitud=solicitud)
              
            infoOrden = OrdenTrabajo(
                secuencia=secuencia,
                cliente=cliente,
                tienda_id=solicitud.tienda.id_tienda,
                taller=solicitud.taller,
                proveedor=solicitud.proveedor,
                pais=solicitud.pais,
                categoria=detalle_solicitud.item.categoria,
                color=solicitud.color,
                externa=solicitud.externa,
                origen_material=solicitud.origen_material,
                env_material=env_material,
                peso_solicitado=solicitud.peso_solicitado,
                unidades_solicitadas=1,
                costo_gramo_base_taller=solicitud.costo_gramo_base_taller,
                precio_gramo_base_taller=solicitud.precio_gramo_base_taller,
                prct_utilidad_base_taller=solicitud.prct_utilidad_base_taller,
                utilidad_base_taller=solicitud.utilidad_base_taller,
                costo_base_total_ta=solicitud.costo_base_total_ta,
                precio_base_total_ta=solicitud.precio_base_total_ta,
                costo_fabricacion_unitario=solicitud.costo_fabricacion_unitario,
                precio_fabricacion_unitario=solicitud.precio_fabricacion_unitario,
                costo_total_fabricacion_ta=solicitud.costo_total_fabricacion_ta,
                precio_fabricacion_total=solicitud.precio_fabricacion_total,
                prct_util_sobre_fabrica_ta=solicitud.prct_util_sobre_fabrica_ta,
                util_sobre_fabrica_ta=solicitud.util_sobre_fabrica_ta,
                subtotal_taller=solicitud.subtotal_taller,
                prct_impuestos_ta=solicitud.prct_impuestos_ta,
                impuestos_taller=solicitud.impuestos_taller,
                total_taller=solicitud.total_taller,
                costo_color_unitario= float(costo_color_unitario),
                costo_color_total = float(costo_color_unitario * solicitud.peso_solicitado),
                costo_gramo_base_op=solicitud.costo_gramo_base_op,
                precio_gramo_base_op=solicitud.precio_gramo_base_op,
                prct_util_sobre_base_op=solicitud.prct_util_sobre_base_op,
                costo_base_total_op=solicitud.costo_base_total_op,
                precio_base_total_op=solicitud.precio_base_total_op,
                util_sobre_base_op=solicitud.util_sobre_base_op,
                prct_util_sobre_fabrica_op=solicitud.prct_util_sobre_fabrica_op,
                util_sobre_fabrica_op=solicitud.util_sobre_fabrica_op,
                precio_unitario_op=solicitud.precio_unitario_op,
                precio_fabricacion_total_op=solicitud.precio_fabricacion_total_op,
                subtotal_orden=solicitud.subtotal_solicitud,
                prct_impuestos_op=solicitud.prct_impuestos_op,
                impuestos_op=solicitud.impuestos_op,
                descuento_orden=solicitud.descuento_solicitud,
                precio_sistema=solicitud.precio_sistema,
                precio_final_venta=solicitud.precio_final_venta,
                estado_id=estado,
                usuario_crea=request.user.id,
                costo_total_rubros=solicitud.total_rubros,
                peso_cliente_dividido=solicitud.peso_cliente_dividido,
                origen_material_dividido=solicitud.origen_material_dividido,
                peso_materia_dividida=solicitud.peso_materia_dividida,
                fabricacion_dividida= solicitud.fabricacion_dividida,
                fabricacion_interna=solicitud.fabricacion_interna

            )
            if infoOrden:
                infoOrden.save()
                if infoOrden.externa:
                    infoOrden.proveedor.secuencia_ordenes += 1
                    infoOrden.proveedor.save()
                else:
                    infoOrden.taller.secuencia_ordenes += 1
                    infoOrden.taller.save()
                form = OrdenAnticipoForm(
                    instance=infoOrden,
                    data=request.POST,
                    files=request.FILES
                )
                if form.is_valid():
                    form.save()
                if infoOrden.externa:
                    solicitud.estado_id = 7
                else:
                    solicitud.estado_id = 10
                solicitud.save()
            infoDetalle = DetalleOrden(
                id_solicitud=solicitud.id_solicitud,
                orden=infoOrden,
                pais=infoOrden.pais,
                usuario_crea=request.user.id,
                id_item=detalle_solicitud.item_id
            )

            if piedras_solicitud:
                for piedra in piedras_solicitud:
                    infoPiedra = OrdenesPiedras(
                        orden=infoOrden,
                        piedra=piedra.piedra,
                        piedra_detalle=piedra.piedra_detalle,
                        cantidad_piedras=piedra.cantidad_piedras,
                        costo_piedra_taller=piedra.costo_piedra_taller,
                        precio_piedra_taller=piedra.precio_piedra_taller,
                        prct_utilidad_piedra_op=piedra.prct_utilidad_piedra_op,
                        precio_piedra_op=piedra.precio_piedra_op,
                        subtotal_piedras_taller=piedra.subtotal_piedras_taller,
                        subtotal_piedras_op=piedra.subtotal_piedras_op
                    )
                    if infoPiedra:
                        infoPiedra.save()
            
            if solicitudes_adicionales:
                for adicional in solicitudes_adicionales:
                    infoAdicional = OrdenesAdicionales(
                        orden=infoOrden,
                        adicional=adicional.adicional,
                        cantidad_adicionales=adicional.cantidad_adicionales,
                        costo_adicional_taller=adicional.costo_adicional_taller,
                        precio_adicional_taller=adicional.precio_adicional_taller,
                        prct_utilidad_adicional_op=adicional.prct_utilidad_adicional_op,
                        precio_adicional_op=adicional.precio_adicional_op,
                        subtotal_adicional_taller=adicional.subtotal_adicional_taller,
                        subtotal_adicional_op=adicional.subtotal_adicional_op
                    )
                    if infoAdicional:
                        infoAdicional.save()

            if infoDetalle:
                infoDetalle.save()
                if not solicitud.externa:
                    producto = detalle_solicitud.item.descripcion
                    principal = True
                    postergada = False
                    id_transaccion = infoOrden.id_orden
                    tipo_transaccion = 2
                    tipo_notificacion = 2
                    NotificacionOrdenes.delay(
                        request.user.id,
                        infoOrden.tienda_id,
                        solicitud.taller_id,
                        producto,
                        principal,
                        postergada,
                        id_transaccion,
                        tipo_transaccion,
                        infoOrden.estado_id,
                        tipo_notificacion
                    )    
            if request.user.pais.nombre != 'COLOMBIA':
                enviarCorreoCliente.delay(infoOrden.id_orden)
                # enviarSms.delay(infoOrden.id_orden, 1)
            mensaje_telegram = "Se ha generado una Orden de trabajo con la secuencia {}, y solicitada por la tienda '{}'.".format(infoOrden.secuencia, infoOrden.tienda)
            
            taller_id = Talleres.objects.filter(id_taller=infoOrden.taller_id).values('id_taller')
            usuario_t = UsuariosTalleres.objects.filter(taller_id__in=taller_id)
            lista_usuario_telegram = []
            for usuario in usuario_t:
                lista_usuario_telegram.append(usuario.usuario.usuario_telegram)
            enviarTelegram.delay(lista_usuario_telegram, mensaje_telegram)
            return HttpResponse(infoOrden.id_orden)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('trn.add_ordentrabajo',
                     login_url='bases:sin_permisos')
def CrearOrdenItemView(request, id_item=None, identificacion=None):
    template_name = "trn/ordenes_item_crear.html"
    form_rol = {}
    contexto = {}
    sociedad = 0
    tiendas = None
    item = Items.objects.filter(pk=id_item).first()
    detalles = DetalleItems.objects.filter(id_item=item).\
        filter(estado__descripcion='ACTIVO')
    colores = ItemsColores.objects.filter(item=item)
    sin_talla = Tallas.objects.filter(talla=0)
    cliente = Clientes.objects.all()
    tiendas_id = UsuariosTiendas.objects.filter(usuario_id=request.user.id).values('tienda_id')
    if request.user.rol.descripcion == 'ADMIN OPERACIONES':
        tiendas = Tiendas.objects.filter(sociedad__grupo_empresarial=request.user.grupo_empresarial())
    if tiendas_id:
        tiendas = Tiendas.objects.filter(id_tienda__in=tiendas_id)
        sociedad_tienda = tiendas.values('sociedad_id')
        sociedad = Sociedades.objects.filter(id_sociedad__in=sociedad_tienda).first()
    configuracion_op = sociedad
    configuracion_ta = item.taller
    origen_pre = OrigenMaterial.objects.\
        filter(id_origen=request.user.grupo_empresarial().origen_material).first()
    costo_fabricacion_unitario = item.costo_taller
    proveedor = item.proveedor()
    if proveedor:
        costo_fabricacion_unitario = proveedor.costo_gramo
        prct_impuestos_proveedor = proveedor.prct_impuestos
        proveedor_item = proveedor.id
    else:
        costo_fabricacion_unitario = item.costo_taller
        prct_impuestos_proveedor = 0
        proveedor_item = 0
    

    precio_definido_taller = item.categoria.precio_taller_obj()

    precio_definido_op = item.categoria.precio_empresa_obj()
    if precio_definido_op:
        prct_util_fabricacion_op = precio_definido_op.prct_utilidad
        precio_unitario_op = precio_definido_op.precio
        regla_calculo_op = precio_definido_op.tipo.regla_calculo.descripcion
    else:
        prct_util_fabricacion_op = configuracion_op.grupo_empresarial.utilidad_sobre_taller
        precio_unitario_op = configuracion_op.grupo_empresarial.precio_gramo_final
        tipo_precio = TiposPrecios.objects.\
            filter(id_tipo=configuracion_op.grupo_empresarial.tipo_precio_predefinido).first()
        regla_calculo_op = tipo_precio.regla_calculo.descripcion



    tooltips = ConfiguracionTooltipOperaciones.objects.\
        filter(
            estado=1,
            pais=request.user.pais_id,
            grupo=configuracion_op.grupo_empresarial_id
        )



    tool_orig_mat = ''
    tool_ant_fabr = ''
    tool_color = ''

    for tool in tooltips:
        if tool.campo_orden == 'origen_material':
            tool_orig_mat = tool.texto
        if tool.campo_orden == 'anticipo_fabricacion':
            tool_ant_fabr = tool.texto
        if tool.campo_orden == 'color':
            tool_color = tool.texto

    ext_perm_arc = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()


    if request.method == 'GET':

        contexto = {
                    'item': item,
                    'detalles': detalles,
                    'colores': colores,
                    'configuracion': configuracion_op,
                    'configuracion_op': request.user.grupo_empresarial(),
                    'configuracion_ta': configuracion_ta,
                    'origen_material': OrigenMaterial.objects.all().exclude(descripcion='NINGUNO'),
                    'origen_pre': origen_pre,
                    'precio_definido_taller': precio_definido_taller,
                    'precio_definido_op': precio_definido_op,
                    'costo_fabricacion_unitario': costo_fabricacion_unitario,
                    'prct_util_fabricacion_op': prct_util_fabricacion_op,
                    'precio_unitario_op': precio_unitario_op,
                    'regla_calculo_op': regla_calculo_op,
                    'tiendas': tiendas,
                    'sociedad': sociedad,
                    'tool_orig_mat': tool_orig_mat,
                    'tool_ant_fabr': tool_ant_fabr,
                    'ext_perm_arc': ext_perm_arc,
                    'tool_color': tool_color
                    }

    if request.method == 'POST':
        cliente = Clientes.objects.filter(identificacion=identificacion).\
            first()
        adicionales_lista = request.POST.getlist('adicionales_lista[]')

        longitud = len(adicionales_lista)
        tipo_transaccion = request.POST['tipo_transaccion']
        # fabricacion_interna = request.POST['fabricacion_interna']

        color = request.POST['id_color']

        if tipo_transaccion == '1':
            id_detalle_item = request.POST['id_detalle_item']

            if id_detalle_item == 'undefined':
                talla = Tallas.objects.filter(talla=0).first()
                id_detalle_item = talla.id_talla
            # sin_color = Colores.objects.filter(descripcion='SIN COLOR').first()
            # color = sin_color.id_color
            
        if tipo_transaccion == '2':
            detalle_item = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            id_detalle_item = detalle_item.id_detalle_item
            color_item = ItemsColores.objects.\
                filter(item_id=item.id_item).first()
            color = color_item.color_id


        env_material = request.POST['env_material']
        if env_material == 'false':
            env_material = False
        else:
            env_material = True
        # id_detalle_item = request.POST['id_detalle_item']
        # color = request.POST['id_color']
        peso_solicitado = request.POST['peso_solicitado']
        origen = request.POST['origen_material']
        datos_extra = request.POST['datos_extra']
        # adicionales
        costo_adicionales = request.POST['costo_adicionales']
        precio_adicionales = request.POST['precio_adicionales']
        precio_adicionales_op = request.POST['precio_adicionales_op']
        util_sobre_adicionales = request.POST['util_sobre_adicionales']
        util_sobre_adicionales_op = request.POST['util_sobre_adicionales_op']
        
        costo_piedras = request.POST['costo_piedras']
        precio_piedras = request.POST['precio_piedras']
        precio_piedras_op = request.POST['precio_piedras_op']
        util_sobre_piedras = request.POST['util_sobre_piedras']
        util_sobre_piedras_op = request.POST['util_sobre_piedras_op']

        costo_gramo_base_taller = request.POST['costo_gramo_base_taller']
        precio_gramo_base_taller = request.POST['precio_gramo_base_taller']
        prct_utilidad_base_taller = request.POST['prct_utilidad_base_taller']
        costo_base_total_ta = request.POST['costo_base_total_ta']
        utilidad_base_taller = request.POST['utilidad_base_taller']
        precio_base_total_ta = request.POST['precio_base_total_ta']
        costo_fabricacion_unitario = request.POST['costo_fabricacion_unitario']
        costo_total_fabricacion_ta = request.POST['costo_total_fabricacion_ta']
        prct_util_fabricacion_taller = request.\
            POST['prct_util_fabricacion_taller']
        utilidad_fabricacion_taller = request.\
            POST['utilidad_fabricacion_taller']
        precio_fabricacion_unitario = request.\
            POST['precio_fabricacion_unitario']
        precio_fabricacion_total_ta = request.\
            POST['precio_fabricacion_total_ta']
        costo_piedras_basicas = request.POST['costo_piedras_basicas']
        costo_color_unitario = request.POST['costo_color_unitario']
        costo_color_total = request.POST['costo_color_total']
        

        subtotal_taller = request.POST['subtotal_taller']
        prct_impuestos_taller = request.POST['prct_impuestos_taller']
        impuestos_taller = request.POST['impuestos_taller']
        total_taller = request.POST['total_taller']
        costo_gramo_base_op = request.POST['costo_gramo_base_op']
        precio_gramo_base_op = request.POST['precio_gramo_base_op']
        
        costo_base_total_op = request.POST['costo_base_total_op']
        # prct_utilidad_base_op = request.POST['prct_utilidad_base_op']
        utilidad_base_op = request.POST['utilidad_base_op']
        precio_base_total_op = request.POST['precio_base_total_op']
        prct_util_fabricacion_op = request.POST['prct_util_fabricacion_op']
        
        precio_unitario_op = request.POST['precio_unitario_op']
        utilidad_fabricacion_op = request.POST['utilidad_fabricacion_op']
        precio_fabricacion_total_op = request.\
            POST['precio_fabricacion_total_op']
        subtotal_op = request.POST['subtotal_op']
        impuestos_op = request.POST['impuestos_op']
        total_fabricacion_op = request.POST['total_fabricacion_op']
        subtotal_orden = request.POST['subtotal_orden']
        prct_impuestos_joyeria = request.POST['prct_impuestos_joyeria']
        impuestos_orden = request.POST['impuestos_orden']
        precio_sistema = request.POST['precio_sistema']
        descuento = request.POST['descuento']
        precio_final_orden = request.POST['precio_final_orden']
        origen_material = OrigenMaterial.objects.\
            filter(descripcion=origen).first()
    
        tienda_seleccionada = request.POST['tienda']

        peso_cliente = None
        establecimiento = None
        datos_fabricacion = {}
        establecimiento_id = None
        peso_materia_dividida = None
        fabricacion_dividida = 0
        datos_fabricacion = request.POST['extra']
        datos_fabricacion = json.loads(datos_fabricacion)
        for dato in datos_fabricacion:
            peso_cliente = datos_fabricacion.get('pesoCliente')
            establecimiento = datos_fabricacion.get('origenSeleccionado')
            peso_materia_dividida = datos_fabricacion.get('pesoCalcular')
            fabricacion_dividida =  datos_fabricacion.get('fabricacionDividida')
        if len(datos_fabricacion) != 0:
            establecimiento_id = OrigenMaterial.objects.filter(descripcion=str(establecimiento)).first()


        if env_material:
            estado = 12
        else:
            estado = 20

        if item:
            registros = str(item.taller.secuencia_ordenes+1)
            while len(registros) < 5:
                registros = '0' + registros
            secuencia = item.taller.nombre + '-' + registros
            tienda = Tiendas.objects.filter(id_tienda=tienda_seleccionada).first()
            
            infoOrden = OrdenTrabajo(
                secuencia=secuencia,
                cliente=cliente,
                tienda=tienda,
                taller=item.taller,
                proveedor_id=1,
                pais=request.user.pais,
                categoria=item.categoria,
                color_id=color,
                datos_extra=datos_extra,
                externa=0,
                origen_material=origen_material,
                env_material=env_material,
                peso_solicitado=peso_solicitado,
                unidades_solicitadas=1,
                costo_gramo_base_taller=costo_gramo_base_taller,
                precio_gramo_base_taller=precio_gramo_base_taller,
                prct_utilidad_base_taller=prct_utilidad_base_taller,
                utilidad_base_taller=utilidad_base_taller,
                costo_base_total_ta=costo_base_total_ta,
                precio_base_total_ta=precio_base_total_ta,
                costo_fabricacion_unitario=costo_fabricacion_unitario,
                precio_fabricacion_unitario=precio_fabricacion_unitario,
                costo_total_fabricacion_ta=costo_total_fabricacion_ta,
                precio_fabricacion_total=precio_fabricacion_total_ta,
                prct_util_sobre_fabrica_ta=prct_util_fabricacion_taller,
                util_sobre_fabrica_ta=utilidad_fabricacion_taller,
                costo_color_unitario=costo_color_unitario,
                costo_color_total=costo_color_total,
                subtotal_taller=subtotal_taller,
                prct_impuestos_ta=prct_impuestos_taller,
                impuestos_taller=impuestos_taller,
                costo_piedras_basicas=costo_piedras_basicas,
                total_taller=total_taller,
                # costo_piedras=costo_piedras,
                # precio_piedras=precio_piedras,
                # precio_piedras_op=precio_piedras_op,
                # util_sobre_piedras=util_sobre_piedras,
                # util_sobre_piedras_op=util_sobre_piedras_op,
                # prct_util_sobre_base_op=prct_utilidad_base_op,
                costo_adicionales_taller=costo_adicionales,
                util_sobre_adicionales_taller=util_sobre_adicionales,
                util_sobre_adicionales_op=util_sobre_adicionales_op,
                precio_adicionales_taller=precio_adicionales,
                precio_adicionales_op=precio_adicionales_op,

                costo_gramo_base_op=costo_gramo_base_op,
                precio_gramo_base_op=precio_gramo_base_op,
                costo_base_total_op=costo_base_total_op,
                precio_base_total_op=precio_base_total_op,
                util_sobre_base_op=utilidad_base_op,
                prct_util_sobre_fabrica_op=prct_util_fabricacion_op,
                util_sobre_fabrica_op=utilidad_fabricacion_op,
                precio_unitario_op=precio_unitario_op,
                precio_fabricacion_total_op=precio_fabricacion_total_op,
                subtotal_orden=subtotal_orden,
                prct_impuestos_op=prct_impuestos_joyeria,
                impuestos_op=impuestos_op,
                descuento_orden=descuento,
                precio_sistema=precio_sistema,
                precio_final_venta=precio_final_orden,
                estado_id=estado,
                usuario_crea=request.user.id,
                # fabricacion_interna= fabricacion_interna,
                origen_material_dividido = establecimiento_id,
                peso_cliente_dividido= peso_cliente,
                peso_materia_dividida = peso_materia_dividida,
                fabricacion_dividida= fabricacion_dividida
            )

            if infoOrden:
                infoOrden.save()
                infoOrden.taller.secuencia_ordenes += 1
                infoOrden.taller.save()
                form = OrdenAnticipoForm(
                    instance=infoOrden,
                    data=request.POST,
                    files=request.FILES
                )
                if form.is_valid():
                    form.save()

            infoDetalle = DetalleOrden(
                id_item=item.id_item,
                id_detalle_item=id_detalle_item,
                orden=infoOrden,
                pais=infoOrden.pais,
                usuario_crea=request.user.id
            )
            if infoDetalle:
                infoDetalle.save()
                producto = item.descripcion
                principal = True
                postergada = False
                id_transaccion = infoOrden.id_orden
                tipo_transaccion = 2
                tipo_notificacion = 2
                NotificacionOrdenes.delay(
                    request.user.id,
                    infoOrden.tienda.id_tienda,
                    infoOrden.taller_id,
                    producto,
                    principal,
                    postergada,
                    id_transaccion,
                    tipo_transaccion,
                    infoOrden.estado_id,
                    tipo_notificacion
                )
                if longitud > 0:
                    adicionales = json.loads(adicionales_lista[0])
                if adicionales:
                    for adicional in adicionales:

                        adicional_id = adicional.get('adicional_id', None)
                        adicional_precio_taller_subt = float(adicional.get('adicionalPrecioTallerSubtotal', None))
                        adicional_utilidad_tienda = float(adicional.get('adicionalUtilidadTiendaSubtotal', None))
                        adicional_precio_unitario = float(adicional.get('adicionalPrecioTallerUnitario', None))
                        adicional_tienda_utilidad_prct = float(adicional.get('adicionalUtilidadTiendaPrct', None))
                        ordenAdicional = OrdenesAdicionales(
                            orden_id=infoOrden.id_orden,
                            adicional_id=adicional_id,
                            subtotal_adicional_op= adicional_precio_taller_subt + adicional_utilidad_tienda,
                            subtotal_adicional_taller=adicional.get('adicionalPrecioTallerSubtotal', None),
                            precio_adicional_op= adicional_precio_unitario * (1+ (adicional_tienda_utilidad_prct)/100),
                            prct_utilidad_adicional_op=adicional.get('adicionalUtilidadTiendaPrct', None),
                            precio_adicional_taller=adicional.get('adicionalPrecioTallerUnitario', None),
                            costo_adicional_taller=adicional.get('adicionalCostoTallerUnitario', None),
                            cantidad_adicionales=adicional.get('cantidad', None)
                        )

                        if ordenAdicional:
                            ordenAdicional.save()
            enviarCorreoCliente.delay(infoOrden.id_orden)
            enviarSms.delay(infoOrden.id_orden, 4)
            mensaje_telegram = "Se ha generado una Orden de trabajo con la secuencia {}, y solicitada por la tienda '{}'.".format(infoOrden.secuencia, infoOrden.tienda)
            
            taller_id = Talleres.objects.filter(id_taller=infoOrden.taller_id).values('id_taller')
            usuario_t = UsuariosTalleres.objects.filter(taller_id__in=taller_id)
            lista_usuario_telegram = []
            for usuario in usuario_t:
                lista_usuario_telegram.append(usuario.usuario.usuario_telegram)
            enviarTelegram.delay(lista_usuario_telegram, mensaje_telegram)

            return HttpResponse(infoOrden.id_orden)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('trn.change_ordentrabajo',
                     login_url='bases:sin_permisos')
def OrdenDetalleView(request, template_name='trn/detalle_orden.html', id_orden=None):
    form_rol = {}
    contexto = {}
    categoria_alianzas = None
    talla_mujer = None
    talla_hombre = None
    inscrip_hombre = None
    inscrip_mujer = None
    piedras_list = []
    piedras_relacionadas = []
    adicionales_relacionados = []
    rechazos = {}

    if request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
        rechazos = ConfiguracionRechazoSolicitudOrdenes.objects.\
            filter(
                taller=request.user.taller(),
                pais=request.user.pais,
                estado=1
            )
    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
        rechazos = ConfiguracionRechazoSolicitudOrdenes.objects.\
            filter(
                grupo_empresarial=request.user.grupo_empresarial(),
                pais=request.user.pais,
                estado=1
            )
    

    if request.method == 'GET':

        orden = OrdenTrabajo.objects.filter(id_orden=id_orden).first()
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_solicitud=None).first()
        sintalla = Tallas.objects.filter(talla=0).first()
        peso_max_arc = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_ARCHIVO').first()
        ext_perm_arc = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        cantidad_max_img = ConfiguracionSistema.objects.\
            filter(clave='CANTIDAD_MAX_IMAGENES').first()

        
        adicionales_lista = []
        piedras_lista = []
        piedras_relacionadas = []
        # agregar rubros de solicitud a la orden generada de una solicitud.
        rubros_lista = []
        adicionalesLista = []
        piedraLista = []

        adicionales = OrdenesAdicionales.objects.filter(orden_id=id_orden)
        piedras=OrdenesPiedras.objects.filter(orden_id=id_orden)
        




        costo_adicionales = 0.00
        for adicional in adicionales:
            if adicional:
                descripcion_adicional = Adicionales.objects.filter(id_adicional=adicional.adicional_id).first()
                adicional_detalle = [
                    str(descripcion_adicional),
                    str(adicional.cantidad_adicionales),
                    str(adicional.precio_adicional_taller),
                    str(adicional.precio_adicional_op),
                    str(adicional.subtotal_adicional_op),
                    str(adicional.subtotal_adicional_taller)

                ]
                detalle_adicional = {
                    'adicional': adicional.adicional.descripcion,
                    'cantidad': adicional.cantidad_adicionales,
                    'costo_adicional_taller': str(adicional.costo_adicional_taller),
                    'precio_adicional_taller': str(adicional.precio_adicional_taller),
                    'precio_adicional_operaciones': str(adicional.precio_adicional_op),
                    'subtotal_adicional_taller': str(adicional.subtotal_adicional_taller),
                    'subtotal_adicional_operaciones': str(round(adicional.subtotal_adicional_op, 2)),
                    'prct_utilidad_operaciones': str(round(adicional.prct_utilidad_adicional_op, 2)),
                    'utilidad': str(round((float(adicional.subtotal_adicional_op) - float(adicional.subtotal_adicional_taller)), 2)) 

                }
                adicional_detalle={
                    'cantidad': adicional.cantidad_adicionales,
                    'costo': str(adicional.costo_adicional_taller),
                    'precio_ta': str(adicional.precio_adicional_taller),
                    'utilidadTiendaPrct': str(adicional.prct_utilidad_adicional_op),
                    'id_adicional': str(adicional.adicional_id)
                }
                adicionalesLista.append(adicional_detalle)
                adicionales_relacionados.append(detalle_adicional)
                adicionales_lista.append(adicional_detalle)
        adicionales_lista = json.dumps(adicionales_lista)
        print(adicionales_lista)
        # piedras relacionadas a la orden 
        for piedra in piedras:
            if piedra:
                descripcion = Piedras.objects.filter(id_piedra=piedra.piedra_id).first()
                piedra_detalle = [
                    str(descripcion),
                    str(piedra.cantidad_piedras),
                    str(piedra.precio_piedra_taller),
                    str(piedra.subtotal_piedras_taller),
                    str(piedra.subtotal_piedras_op)
                ]
                detalle_piedra = {
                    'piedra': piedra.piedra.descripcion,
                    'cantidad': piedra.cantidad_piedras,
                    'costo_piedra_taller': str(piedra.costo_piedra_taller),
                    'precio_piedra_taller': str(piedra.precio_piedra_taller),
                    'precio_piedra_operaciones': str(piedra.precio_piedra_op),
                    'subtotal_piedra_taller': str(piedra.subtotal_piedras_taller),
                    'subtotal_piedra_operaciones': str(round(piedra.subtotal_piedras_op, 2)),
                    'prct_utilidad_operaciones': str(round(piedra.prct_utilidad_piedra_op, 2)),
                    'utilidad': str(round((float(piedra.subtotal_piedras_op) - float(piedra.subtotal_piedras_taller)), 2)) 

                }
                piedra_detalle={
                    'cantidad': piedra.cantidad_piedras,
                    'costo': str(piedra.costo_piedra_taller),
                    'precio_ta': str(piedra.precio_piedra_taller),
                    'utilidadTiendaPrct': str(piedra.prct_utilidad_piedra_op),
                    'id_piedra': piedra.piedra_id
                }
                piedraLista.append(piedra_detalle)
                piedras_relacionadas.append(detalle_piedra)
                piedras_lista.append(piedra_detalle)
        piedras_lista = json.dumps(piedras_lista)
        print(piedras_lista)
        rubros_asociados = None
        piedras_preciosas = None
        rubros = None
        item_solicitud = None
        costo_total_rubros = 0

        if detalleitem:
            print('solicitud')
            print(detalleitem)
            item = SolicitudTrabajo.objects.\
                filter(pk=detalleitem.id_solicitud).first()
            detalleSolicitud = DetalleSolicitud.objects.\
                filter(solicitud_id=item.id_solicitud).first()
            detalle = None
            imagenes = SolicitudesImagenes.objects.\
                filter(solicitud=item)
            rubros = SolicitudRubros.objects.filter(solicitud_id=detalleitem.id_solicitud)
            for rubro in rubros:
                if rubro:
                    descripcion = RubrosAsociados.objects.filter(id_rubro=rubro.rubro_id).first()
                    rubro_detalle = [
                        str(descripcion),
                        str(rubro.valor),
                    ]
                    rubros_lista.append(rubro_detalle)
            rubros_lista = json.dumps(rubros_lista)

            item_solicitud = Items.objects.filter(id_item=detalleSolicitud.item_id, taller_id=item.taller_id).first()

            if rubros:
                for rubro in rubros:
                    costo_total_rubros += rubro.valor
            print(costo_total_rubros)
            
            
        else:
            print('catalogo')
            if orden.categoria.categoria_alianzas:
                detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).first()
                detalle = PiezasDetalles.objects.filter(pieza__item_id=detalleitem.id_item).first()
                if detalle != None:
                    item = Items.objects.filter(pk=detalle.pieza.item_id).first()
                else:
                    item =None
                talla_hombre = float(detalleitem.talla_hombre)
                talla_mujer = float(detalleitem.talla_mujer)
                inscrip_hombre = detalleitem.inscripcion_hombre
                inscrip_mujer = detalleitem.inscripcion_mujer

                # edicion de vista
                piezas_detalles = PiezasDetalles.objects.filter(id_pieza_detalle=detalleitem.id_pieza_detalle)
                if piezas_detalles:
                    for pieza in piezas_detalles:
                        print(pieza)
                        # piedras_piezas = PiezasPiedras.objects.filter(detalle_pieza_id=pieza.id_pieza_detalle)
                        piedras = PiezasPiedras.objects.filter(detalle_pieza_id=pieza.id_pieza_detalle)
                        print(piedras)
                        piedras = PiezasPiedrasItemSerializer(piedras, many=True).data
                        print(piedras)
                        for piedra in piedras:
                            detalle_piedra = {
                                'sku': piedra.get('sku'),
                                'descripcion': piedra.get('descripcion'),
                                'puntos': piedra.get('puntos'),
                                'cantidad': piedra.get('cantidad'),

                            }
                            piedras_list.append(detalle_piedra)
                
            else:
                detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                    exclude(id_item=None).first()

                detalle = DetalleItems.objects.\
                    filter(id_detalle_item=detalleitem.id_detalle_item).first()
                item = Items.objects.filter(id_item=detalleitem.id_item).first()
            detalleSolicitud = None
            imagenes = ItemsImagenes.objects.\
                filter(item=item)
            rubros_asociados = None
            piedras_preciosas = None

            # detalle para las alianzas
            categoria_alianzas = orden.categoria.categoria_alianzas
            # if categoria_alianzas:
                # talla_hombre = float(detalleitem.talla_hombre)
                # talla_mujer = float(detalleitem.talla_mujer)
                # inscrip_hombre = detalleitem.inscripcion_hombre
                # inscrip_mujer = detalleitem.inscripcion_mujer

                # piezas_detalles = PiezasDetalles.objects.filter(id_pieza_detalle=detalleitem.id_pieza_detalle)

                # if piezas_detalles:
                #     for pieza in piezas_detalles:
                #         # piedras_piezas = PiezasPiedras.objects.filter(detalle_pieza_id=pieza.id_pieza_detalle)
                #         piedras = PiezasPiedras.objects.filter(detalle_pieza_id=pieza.id_pieza_detalle)

                #         piedras = PiezasPiedrasItemSerializer(piedras, many=True).data
                #         for piedra in piedras:
                #             detalle_piedra = {
                #                 'sku': piedra.get('sku'),
                #                 'descripcion': piedra.get('descripcion'),
                #                 'puntos': piedra.get('puntos'),
                #                 'cantidad': piedra.get('cantidad'),

                #             }
                #             piedras_list.append(detalle_piedra)
        imagenes_orden_terminada = OrdenesImagenes.objects.\
            filter(orden=orden)

        # piedras relacionadas a la orden
        piedras=OrdenesPiedras.objects.filter(orden_id=id_orden)
        for piedra in piedras:
            if piedra:
                descripcion = Piedras.objects.filter(id_piedra=piedra.piedra_id).first()
                piedra_detalle = [
                    str(descripcion),
                    str(piedra.cantidad_piedras),
                    str(piedra.precio_piedra_taller),
                    str(piedra.subtotal_piedras_taller),
                    str(piedra.prct_utilidad_piedra_op)
                ]
                piedras_relacionadas.append(piedra_detalle)
        piedras_relacionadas = json.dumps(piedras_relacionadas)


        tooltips = ConfiguracionTooltipOperaciones.objects.\
            filter(
                estado=1,
                pais=request.user.pais_id,
                grupo=orden.tienda.sociedad.grupo_empresarial_id
            )




        lista_tool = []

        tool_comp_env= ''
        tool_orig_mat = ''
        tool_antic_fabr = ''
        tool_cta_por_pag = ''
        tool_ordn_compr = ''
        tool_fct_taller = ''

        for tool in tooltips:
            
            if tool.campo_orden == 'comprobante_env':
                tool_comp_env = tool.texto
            if tool.campo_orden == 'origen_material':
                tool_orig_mat = tool.texto
            if tool.campo_orden == 'anticipo_fabricacion':
                tool_antic_fabr = tool.texto
            if tool.campo_orden == 'cta_por_pagar':
                tool_cta_por_pag = tool.texto
            if tool.campo_orden == 'orden_compra':
                tool_ordn_compr = tool.texto
            if tool.campo_orden == 'factura_taller':
                tool_fct_taller = tool.texto

            detalle_tool = {
                'campo' : tool.campo_orden,
                'texto' : tool.texto
            }
            lista_tool.append(detalle_tool)
        lista_tool = json.dumps(lista_tool)

        
        if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            config = request.user.grupo_empresarial()
        else:
            config = request.user.taller()
        contexto = {
            'orden': orden,
            'item': item,
            'detalle': detalle,
            'detalleSolicitud': detalleSolicitud,
            'sintalla': sintalla,
            # 'costo_adicionales': costo_adicionales,
            'adicionales_lista': adicionales,
            'adicionales_listado': adicionales_lista,
            'piedras_lista': piedras,
            'piedras_listado':piedras_lista,
            'rubros_listado': rubros,
            'peso_max_arc': peso_max_arc,
            'ext_perm_arc': ext_perm_arc,
            'imagenes': imagenes,
            'ext_perm_img': ext_perm_img,
            'peso_max_img': peso_max_img,
            'cantidad_max_img': cantidad_max_img,
            'imagenes_orden_terminada': imagenes_orden_terminada,
            'PESO_MAX_DATA': settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            'rubros_asociados': rubros_asociados,
            'piedras_preciosas': piedras_preciosas,
            # detalle alianzas ################
            'categoria_alianzas': categoria_alianzas,
            'talla_mujer': talla_mujer,
            'talla_hombre': talla_hombre,
            'inscripcion_hombre': inscrip_hombre,
            'inscripcion_mujer': inscrip_mujer,
            'piedras_alianza': piedras_list,
            'piedras_relacionadas': piedras_relacionadas,
            'adicionales_relacionados': adicionales_relacionados,
            'piedras_lista': piedras,
            'tooltips': lista_tool,
            'tool_comp_env': tool_comp_env,
            'tool_orig_mat': tool_orig_mat,
            'tool_antic_fabr': tool_antic_fabr,
            'tool_cta_por_pag': tool_cta_por_pag,
            'tool_ordn_compr': tool_ordn_compr,
            'tool_fct_taller': tool_fct_taller,
            'piedraLista': piedraLista,
            'adicionalesLista': adicionalesLista,
            'item_solicitud': item_solicitud,
            'costo_total_rubros': costo_total_rubros,
            'rechazos': rechazos,
            'config': config
        }


    if request.method == 'POST':
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        json_data = json.loads(request.body)
        estado = json_data['estado']
        estado = int(estado)
        if estado == 17:
            orden.fecha_recibe_prod = datetime.now(timezone.utc)
            orden.estado_id = 17

            limite_venta = orden.usuario.tmp_lim_vta
            tiempo_limite_vta = \
                datetime.now(timezone.utc) + \
                timedelta(days=int(limite_venta))
            kwargs = {'id_transaccion': orden.id_orden}
            kwargs = json.dumps(kwargs)

            zona_horaria = request.user.pais.zona_horaria
            nombre_tarea = 'limiteventa_' + str(request.user.id) + \
                '_' + str(orden.id_orden)

            periodo, _ = CrontabSchedule.objects.get_or_create(
                minute=tiempo_limite_vta.minute,
                hour=tiempo_limite_vta.hour,
                day_of_week='*',
                day_of_month=tiempo_limite_vta.day,
                month_of_year=tiempo_limite_vta.month,
                timezone=zona_horaria
            )

            tarea = PeriodicTask.objects.filter(
                name=nombre_tarea
            ).first()

            if tarea:
                tarea.crontab = periodo
                tarea.kwargs = kwargs
                tarea.save()
            else:
                PeriodicTask.objects.create(
                    crontab=periodo,
                    name=nombre_tarea,
                    task='ntf.tasks.NotificacionLimiteVenta',
                    kwargs=kwargs
                )
        if estado == 14:
            orden.fecha_recibe_mat = datetime.now(timezone.utc)
            orden.estado_id = 14
        orden.save()

    return render(request, template_name, contexto)

class DetalleOrdenApi(APIView):

    def get(self, request, id_orden=None):
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_solicitud=None).first()
        sintalla = Tallas.objects.filter(talla=0).first()

        if detalleitem:
            item = SolicitudTrabajo.objects.\
                filter(pk=detalleitem.id_solicitud).first()
            detalleSolicitud = DetalleSolicitud.objects.\
                filter(solicitud_id=item.id_solicitud).first()
            detalle = detalleitem.objects.\
                filter(
                    pk=detalleitem.id_detalle_item
                ).first()

            imagenes = SolicitudesImagenes.objects.\
                filter(solicitud=item)
            rubros_asociados = SolicitudRubros.objects.\
                filter(solicitud_id=item.id_solicitud)
            sku = detalleSolicitud.item.sku
            if orden.externa:
                fabricante = item.proveedor.nombres + ' ' +\
                    item.proveedor.apellidos
            else:
                fabricante = item.taller.nombre
            item_descripcion = detalleSolicitud.item.descripcion
            item_detalles = item.detalle
            if detalleSolicitud.item.unidad_medida.descripcion == 'TALLA':
                item_medida = str(item.talla.talla) + ' ' + \
                    item.talla.estandar.descripcion
            else:
                item_medida = str(item.longitud) + ' ' + detalleSolicitud.\
                    item.unidad_medida.simbolo
            cantidad_piedras = item.cantidad_piedras
            tiempo_entrega_min = item.tiempo_ent_min
            tiempo_entrega_max = item.tiempo_ent_max
            item = SolicitudesSerializer(item).data
            detalleSolicitud = DetallesSolicitudSerializer(detalleSolicitud).\
                data
            imagenes = SolicitudImagenesSerializer(imagenes, many=True).\
                data
        else:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            detalle = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            detalleSolicitud = None
            sku = item.sku
            if orden.externa:
                fabricante = orden.proveedor.nombres + ' ' +\
                    item.proveedor.apellidos
            else:
                fabricante = orden.taller.nombre
            item_descripcion = item.descripcion
            item_detalles = orden.datos_extra
            if detalle.estandar:
                item_medida = str(detalle.medida) + ' ' + detalle.estandar
            else:
                item_medida = str(detalle.medida) + ' ' + detalle.unidad_medida
            cantidad_piedras = detalle.cantidad_piedras
            tiempo_entrega_min = item.tiempo_entrega_min
            tiempo_entrega_max = item.tiempo_entrega_max
            imagenes = ItemsImagenes.objects.\
                filter(item=item)
            item = ItemDetalleOrdenSerializer(item).data
            imagenes = ItemImagenesSerializer(
                imagenes,
                many=True
            ).data
            rubros_asociados = None

        imagenes_orden_terminada = OrdenesImagenes.objects.\
            filter(orden=orden)
        imagenes_orden_terminada = OrdenImagenesSerializer(
            imagenes_orden_terminada, many=True
        ).data
        rubros_asociados = SolicitudRubrosSerializer(
            rubros_asociados,
            many=True
        ).data
        orden = OrdenDetallesSerializer(orden).data

        return Response(
            {
                'orden': orden,
                'item': item,
                'sku': sku,
                'fabricante': fabricante,
                'item_descripcion': item_descripcion,
                'item_detalles': item_detalles,
                'item_medida': item_medida,
                'cantidad_piedras': cantidad_piedras,
                'tiempo_entrega_min': tiempo_entrega_min,
                'tiempo_entrega_max': tiempo_entrega_max,
                'imagenes': imagenes,
                # 'detalle': detalle,
                'detalleSolicitud': detalleSolicitud,
                # 'sintalla': sintalla,
                'imagenes_orden_terminada': imagenes_orden_terminada,
                'rubros_asociados': rubros_asociados
            },
            status=200)



def CorreoTemplateView(request, id_orden=None):
    template_name = "trn/correo_cliente.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
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
                    str(item_adicional.sku),
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
                    str(item_adicional.piedra.sku),
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
            detalle = None
        else:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            detalle = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            detalleSolicitud = None
        precio_final = float(orden.precio_con_desceunto) \
            + float(orden.costo_envio)

        contexto = {
                    'orden': orden,
                    'item': item,
                    'detalle': detalle,
                    'detalleSolicitud': detalleSolicitud,
                    'sintalla': sintalla,
                    'costo_adicionales': costo_adicionales,
                    'adicionales_lista': adicionales_lista,
                    'sUrl': settings.BASE_DIR,
                    'precio_final': precio_final,
                    'usuario': request.user
                    }
        enviarCorreoCliente.delay(id_orden)

    return render(request, template_name, contexto)


def CorreoZonalTemplateView(request, id_orden=None):
    template_name = "trn/correo_producto_recibido.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_solicitud=None).first()
        sintalla = Tallas.objects.filter(talla=0).first()
        usuario = Usuarios.objects.filter(
            zona_id=request.user.zona_id,
            rol__zonal=True
            )

        adicionales_lista = []
        adicionales = DetalleOrden.objects.filter(orden_id=id_orden)
        costo_adicionales = 0.00
        for adicional in adicionales:
            if adicional.id_adicional:
                item_adicional = Adicionales.objects.\
                    filter(id_adicional=adicional.id_adicional).first()
                adicional_detalle = [
                    str(item_adicional.sku),
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
                    str(item_adicional.piedra.sku),
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
            detalle = None
        else:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            detalle = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            detalleSolicitud = None
        print(settings.BASE_DIR)
        precio_final = float(orden.precio_con_desceunto) \
            + float(orden.costo_envio)

        contexto = {
                    'orden': orden,
                    'item': item,
                    'detalle': detalle,
                    'detalleSolicitud': detalleSolicitud,
                    'sintalla': sintalla,
                    'costo_adicionales': costo_adicionales,
                    'adicionales_lista': adicionales_lista,
                    'sUrl': settings.BASE_DIR,
                    'precio_final': precio_final,
                    'usuario': usuario
                    }
        enviarCorreoZonal.delay(id_orden)

    return render(request, template_name, contexto)


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path





class DetalleOrdenApi(APIView):

    def get(self, request, id_orden=None):
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_solicitud=None).first()
        sintalla = Tallas.objects.filter(talla=0).first()

        if detalleitem:
            item = SolicitudTrabajo.objects.\
                filter(pk=detalleitem.id_solicitud).first()
            detalleSolicitud = DetalleSolicitud.objects.\
                filter(solicitud_id=item.id_solicitud).first()
            detalle = None
            imagenes = SolicitudesImagenes.objects.\
                filter(solicitud=item)
            rubros_asociados = SolicitudRubros.objects.\
                filter(solicitud_id=item.id_solicitud)
            sku = detalleSolicitud.item.sku
            if orden.externa:
                fabricante = item.proveedor.nombres + ' ' +\
                    item.proveedor.apellidos
            else:
                fabricante = item.taller.nombre
            item_descripcion = detalleSolicitud.item.descripcion
            item_detalles = item.detalle
            if detalleSolicitud.item.unidad_medida.descripcion == 'TALLA':
                item_medida = str(item.talla.talla) + ' ' + \
                    item.talla.estandar.descripcion
            else:
                item_medida = str(item.longitud) + ' ' + detalleSolicitud.\
                    item.unidad_medida.simbolo
            cantidad_piedras = item.cantidad_piedras
            tiempo_entrega_min = item.tiempo_ent_min
            tiempo_entrega_max = item.tiempo_ent_max
            item = SolicitudesSerializer(item).data
            detalleSolicitud = DetallesSolicitudSerializer(detalleSolicitud).\
                data
            imagenes = SolicitudImagenesSerializer(imagenes, many=True).\
                data
        else:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            detalle = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            detalleSolicitud = None
            sku = item.sku
            if orden.externa:
                fabricante = orden.proveedor.nombres + ' ' +\
                    item.proveedor.apellidos
            else:
                fabricante = orden.taller.nombre
            item_descripcion = item.descripcion
            item_detalles = orden.datos_extra
            if detalle.estandar:
                item_medida = str(detalle.medida) + ' ' + detalle.estandar
            else:
                item_medida = str(detalle.medida) + ' ' + detalle.unidad_medida
            cantidad_piedras = detalle.cantidad_piedras
            tiempo_entrega_min = item.tiempo_entrega_min
            tiempo_entrega_max = item.tiempo_entrega_max
            imagenes = ItemsImagenes.objects.\
                filter(item=item)
            item = ItemDetalleOrdenSerializer(item).data
            imagenes = ItemImagenesSerializer(
                imagenes,
                many=True
            ).data
            rubros_asociados = None

        imagenes_orden_terminada = OrdenesImagenes.objects.\
            filter(orden=orden)
        imagenes_orden_terminada = OrdenImagenesSerializer(
            imagenes_orden_terminada, many=True
        ).data
        rubros_asociados = SolicitudRubrosSerializer(
            rubros_asociados,
            many=True
        ).data
        orden = OrdenDetallesSerializer(orden).data
        # print(imagenes_orden_terminada)
        return Response(
            {
                'orden': orden,
                'item': item,
                'sku': sku,
                'fabricante': fabricante,
                'item_descripcion': item_descripcion,
                'item_detalles': item_detalles,
                'item_medida': item_medida,
                'cantidad_piedras': cantidad_piedras,
                'tiempo_entrega_min': tiempo_entrega_min,
                'tiempo_entrega_max': tiempo_entrega_max,
                'imagenes': imagenes,
                # 'detalle': detalle,
                'detalleSolicitud': detalleSolicitud,
                # 'sintalla': sintalla,
                'imagenes_orden_terminada': imagenes_orden_terminada,
                'rubros_asociados': rubros_asociados
            },
            status=200)



@login_required(login_url='/login/')
def ComprobanteTemplateView(request, id_orden=None):
    if request.user.pais.nombre == 'COLOMBIA':
        template_name = "trn/comprobante_formato_nuevo.html"
    else:
        template_name = "trn/comprobante_orden.html"
    if request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
        if request.user.pais.nombre == 'BRASIL':
            template_name = "trn/comprobante_taller_br.html"
        else:
            template_name = "trn/comprobante_orden.html"

            # template_name = "trn/comprobante_orden_taller.html"
    contexto = {}



    orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
    detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
        exclude(id_solicitud=None).first()


    # texto_politicas 

    politicas_comerciales = PoliticasComerciales.objects.filter(empresa_id=orden.tienda.sociedad.grupo_empresarial_id).first()
    if politicas_comerciales:
        texto_politicas = politicas_comerciales.descripcion
    else:
        texto_politicas = ""

    # if detalleitem:
    #     template_name = "trn/comprobante_formato_nuevo.html"

    # print(detalleitem)
    sintalla = Tallas.objects.filter(talla=0).first()

    adicionales_lista = []
    adicionales = DetalleOrden.objects.filter(orden_id=id_orden)
    costo_adicionales = 0.00
    imagenes_orden = None
    talla_mujer = None
    talla_hombre =  None
    inscripcion_m = None
    inscripcion_h = None
    fecha_estimada_entrega = None
    contador_imagenes = 0
    piezas_acabados = None
    piedras_lista = []
    rubros_lista = []
    item = None
    rubros = None 
    piedras = None



    adicionales = OrdenesAdicionales.objects.filter(orden_id=id_orden)



    for adicional in adicionales:
        if adicional.adicional_id:
            item_adicional = Adicionales.objects.\
                filter(id_adicional=adicional.adicional_id).first()
            adicional_detalle = [
                str(item_adicional.sku),
                str(item_adicional.descripcion),
                str(item_adicional.precio_taller),
                str(adicional.cantidad_adicionales)
            ]
            adicionales_lista.append(adicional_detalle)
            costo_adicionales += \
                (float(item_adicional.precio_taller)*float(adicional.cantidad_adicionales))
        # if adicional.id_piedra:
        #     item_adicional = DetallePiedras.objects.\
        #         filter(id_detalle_piedra=adicional.id_detalle_piedra).\
        #         first()
        #     adicional_detalle = [
        #         str(item_adicional.piedra.sku),
        #         str(item_adicional.piedra.descripcion),
        #         str(item_adicional.precio),
        #         str(adicional.cantidad)
        #     ]
        #     adicionales_lista.append(adicional_detalle)
        #     costo_adicionales += \
        #         (float(item_adicional.precio)*float(adicional.cantidad))
    costo_adicionales = round(costo_adicionales, 2)
    piedras=OrdenesPiedras.objects.filter(orden_id=id_orden)


    if detalleitem:
        item = SolicitudTrabajo.objects.\
            filter(pk=detalleitem.id_solicitud).first()
        detalleSolicitud = DetalleSolicitud.objects.\
            filter(solicitud_id=item.id_solicitud).first()
        detalle = None
        imagenes = SolicitudesImagenes.objects.\
            filter(solicitud=item)


        rubros = SolicitudRubros.objects.filter(solicitud_id=detalleitem.id_solicitud)
        for rubro in rubros:
            if rubro:
                descripcion = RubrosAsociados.objects.filter(id_rubro=rubro.rubro_id).first()
                rubro_detalle = [
                    str(descripcion),
                    str(rubro.valor),
                ]
                rubros_lista.append(rubro_detalle)
        # rubros_lista = json.dumps(rubros_lista)

        detalle_orden = DetalleOrden.objects.filter(id_solicitud=item.id_solicitud).values('orden_id')
        orden_id = OrdenTrabajo.objects.filter(id_orden__in=detalle_orden).first()
        if orden.fecha_fin_trabajo != None:
            fecha_estimada_entrega = orden.fecha_fin_trabajo
        else:
            fecha_orden = orden.fecha_creacion
            fecha_estimada_entrega = fecha_orden + timedelta(days=item.tiempo_ent_max)
            

    else:
        if orden.categoria.categoria_alianzas:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).exclude(id_item=None).first()
            detalle = PiezasDetalles.objects.filter(pieza__item_id=detalleitem.id_item).first()
            piezas_acabados = PiezasAcabados.objects.filter(pieza__item_id=detalleitem.id_item).first()
            # piezas_piedras = PiezasPiedras.objects.filter(detalle_pieza=detalle)
            # for i in piezas_piedras:
            #     piedra_detalle = DetallePiedras.objects.filter(id_detalle_piedra=i.detalle_piedra_id)
            #     for j in piedra_detalle:
            #         piedras = {
            #             'cantidad': i.cantidad,
            #             'piedra': j.piedra.descripcion
            #         }

            #         piedras_lista.append(piedras)
            # print(piedras_lista)
            # piedras_lista = json.dumps(piedras_lista)

            if detalle != None:
                item = Items.objects.filter(pk=detalle.pieza.item_id).first()
            else:
                item =None

            talla_mujer = str(detalleitem.talla_mujer)
            talla_hombre = str(detalleitem.talla_hombre)
            inscripcion_m = str(detalleitem.inscripcion_mujer)
            inscripcion_h = str(detalleitem.inscripcion_hombre)


            if orden.fecha_fin_trabajo != None:
                fecha_estimada_entrega = orden.fecha_fin_trabajo
            else:
                fecha_orden = orden.fecha_creacion
                fecha_estimada_entrega = fecha_orden + timedelta(days=item.tiempo_entrega_max)
            imagenes = ItemsImagenes.objects.\
                filter(item=item)

        else:

            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            detalle = DetalleItems.objects.\
                filter(pk=detalleitem.id_detalle_item).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            imagenes = ItemsImagenes.objects.\
                filter(item=item)


            if orden.fecha_fin_trabajo != None:
                fecha_estimada_entrega = orden.fecha_fin_trabajo
            else:
                fecha_orden = orden.fecha_creacion
                print(fecha_orden)
                fecha_estimada_entrega = fecha_orden + timedelta(days=item.tiempo_entrega_max)
            
            print('fecha estimada', fecha_estimada_entrega)
        

        detalleSolicitud = None
       


        imagenes = ItemsImagenes.objects.\
            filter(item=item)
        
        rubros_asociados = None
        piedras_preciosas = None


        '''antigua condicion else'''
        # detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
        #     exclude(id_item=None).first()
        # print(detalleitem)

        
        # item = Items.objects.filter(pk=detalleitem.id_item).first()
        # print(item)
        # detalle = DetalleItems.objects.\
        #     filter(id_item_id=item.id_item).first()
        # print(detalle)
        # detalleSolicitud = None
    contador_imagenes = len(imagenes)
    contador_imagenes = int(contador_imagenes)

    # print(request.user.taller().logotipo.url)
    contexto = {
                'orden': orden,
                'item': item,
                'detalle': detalle,
                'detalleSolicitud': detalleSolicitud,
                'acabado': piezas_acabados,
                'detalleSolicitud': detalleSolicitud,
                'sintalla': sintalla,
                'costo_adicionales': costo_adicionales,
                # 'adicionales_lista': adicionales_lista,
                'imagenes': imagenes,
                'sUrl': settings.SITIO,
                'usuario': request.user,
                'imagenes_orden': imagenes_orden,
                'talla_mujer': talla_mujer,
                'talla_hombre': talla_hombre,
                'grabado_mujer': inscripcion_m,
                'grabado_hombre': inscripcion_h,
                'fecha_estimada_entrega': fecha_estimada_entrega,
                'contador_imagenes': contador_imagenes,
                'piedras_lista': piedras_lista,
                'rubros_lista': rubros,
                'adicionales_lista': adicionales,
                'piedras_relacionadas': piedras,
                'texto_politicas': texto_politicas
                }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    template = get_template(template_name)
    html = template.render(contexto)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def ReporteOrdenesListaView(request, f_inicio, f_fin, opcion):
    template_name = "trn/reporte_lista_ordenes.html"
    contexto = {}
    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
    f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
    # taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
    # operaciones
    if request.user.tipo_usuario == 'OPERACIONES':
        taller = None
        usuario = request.user
        if opcion == 1:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_actual,
                        fecha_creacion__lte=ahora
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 2:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_anterior,
                        fecha_creacion__lte=dia_uno_mes_actual
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 3:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')[:100]
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 4:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')[:1000]
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 5:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=f_inicio,
                        fecha_creacion__lte=f_fin + timedelta(days=1)
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = f_inicio
            fecha_fin = f_fin
        if opcion == 6:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__sociedad__zona_id=request.user.zona
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            usuario_crea=request.user.id
                        ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if request.user.rol.descripcion == 'ADMIN OPERACIONES':
            solicitudes = SolicitudTrabajo.objects.filter(
                tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                estado__descripcion='ESPERA COTIZACION TALLER'
            ) | SolicitudTrabajo.objects.filter(
                tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                estado__descripcion='ESPERA DE EVALUACION'
            )
        else:
            if request.user.rol.zonal:
                solicitudes = SolicitudTrabajo.objects.filter(
                    tienda__sociedad__zona_id=request.user.zona,
                    estado__descripcion='ESPERA COTIZACION TALLER'
                ) | SolicitudTrabajo.objects.filter(
                    # usuario__user_usuariostiendas__tienda_id__zona_id=request.user.zona,
                    tienda__sociedad__zona_id = request.user.zona,
                    estado__descripcion='ESPERA DE EVALUACION'
                )
            else:
                solicitudes = SolicitudTrabajo.objects.filter(
                    usuario_crea=request.user.id,
                    estado__descripcion='ESPERA COTIZACION TALLER'
                ) | SolicitudTrabajo.objects.filter(
                    usuario_crea=request.user.id,
                    estado__descripcion='ESPERA DE EVALUACION'
                )
        if solicitudes:
            solicitudes = solicitudes.\
                order_by('estado__orden', '-fecha_modificacion')
    # taller
    else:
    
        taller = request.user.taller()
        usuario = None

        if opcion == 1:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller,
                    fecha_creacion__gte=dia_uno_mes_actual,
                    fecha_creacion__lte=ahora
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 2:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller,
                    fecha_creacion__gte=dia_uno_mes_anterior,
                    fecha_creacion__lte=dia_uno_mes_actual
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 3:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller
                ).order_by('estado__orden', '-fecha_modificacion')[:100]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 4:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller
                ).order_by('estado__orden', '-fecha_modificacion')[:1000]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 5:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller,
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin + timedelta(days=1)
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = f_inicio
            fecha_fin = f_fin
        if opcion == 6:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller_id=taller.id_taller
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        solicitudes = SolicitudTrabajo.objects.filter(
            taller=taller,
            estado__descripcion='ESPERA COTIZACION TALLER'
        ) | SolicitudTrabajo.objects.filter(
            taller=taller,
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
                'solicitudes': solicitudes,
                # 'tienda': tienda
                }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    template = get_template(template_name)
    html = template.render(contexto)

    if ordenes:
        # generar pdf
        pisaStatus = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
    else:
        return HttpResponse(
            'No existen órdenes en el rango de fechas seleccionado'
            )
    # error
    if pisaStatus.err:
        return HttpResponse('error: ' + html + '.')
    return response


def ReporteOrdenesAdminOpView(request, f_inicio, f_fin, opcion):
    template_name = "trn/reporte_lista_ordenes.html"
    contexto = {}
    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
    f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
    taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
    
    # operaciones
    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
        taller = None
        usuario = request.user        
        if opcion == 1:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    fecha_creacion__gte=dia_uno_mes_actual,
                    fecha_creacion__lte=ahora
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 2:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    fecha_creacion__gte=dia_uno_mes_anterior,
                    fecha_creacion__lte=dia_uno_mes_actual
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        if opcion == 3:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial()
                ).order_by('estado__orden', '-fecha_modificacion')[:100]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 4:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                ).order_by('estado__orden', '-fecha_modificacion')[:1000]
            fecha_inicio = None
            fecha_fin = None
        if opcion == 5:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin + timedelta(days=1)
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = f_inicio
            fecha_fin = f_fin
        if opcion == 6:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial()
                ).order_by('estado__orden', '-fecha_modificacion')
            fecha_inicio = None
            fecha_fin = None
        solicitudes = SolicitudTrabajo.objects.filter(
            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
            estado__descripcion='ESPERA COTIZACION TALLER'
        ) | SolicitudTrabajo.objects.filter(
            tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
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

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    template = get_template(template_name)
    html = template.render(contexto)

    if ordenes:
        # generar pdf
        pisaStatus = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
    else:
        return HttpResponse(
            'No existen órdenes en el rango de fechas seleccionado'
            )
    # error
    if pisaStatus.err:
        return HttpResponse('error: ' + html + '.')
    return response


@login_required(login_url='/login/')
@permission_required('trn.change_ordentrabajo',
                     login_url='bases:sin_permisos')
def AgregarPiedraView(request, id_orden=None, id_piedra=None):
    template_name = "trn/agregar_piedra_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        piedra = Piedras.objects.filter(id_piedra=id_piedra).first()
        detalles_piedra = DetallePiedras.objects.\
            filter(piedra_id=piedra.id_piedra, estado_id=1)
        config = Talleres.objects.filter(
            id_taller=piedra.taller_id,
            pais_id=request.user.pais_id
        ).first()
        if config != None:
            utilidad_fab_op = config.utilidad_sobre_piedras
            print(utilidad_fab_op)
        # else:
        #     utilidad_fab_op = request.user.grupo_empresarial().utilidad_sobre_taller
        
        contexto = {
            'piedra': piedra,
            'detalles_piedra': detalles_piedra,
            'id_orden': id_orden,
            'utilidad_fab_op': utilidad_fab_op
            }

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('trn.change_ordentrabajo',
                     login_url='bases:sin_permisos')
def AgregarAdicionalView(request, id_orden=None, id_adicional=None):
    template_name = "trn/agregar_adicional_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        adicional = Adicionales.objects.\
            filter(id_adicional=id_adicional).first()
        # config = ConfigUtilidadTaller.objects.filter(
        #     id_taller=adicional.taller_id,
        #     id_usuario_op=request.user.id
        # ).first()
        # if config:
        #     utilidad_fab_op = config.utilidad_sobre_adicionales
        # else:
        #     utilidad_fab_op = request.user.grupo_empresarial().utilidad_sobre_taller
        config = request.user.taller()
        if config:
            utilidad_fab_op = config.utilidad_sobre_base
        else:
            utilidad_fab_op = request.user.grupo_empresarial().utilidad_sobre_taller
        
        contexto = {
            'adicional': adicional,
            'id_orden': id_orden,
            'utilidad_fab_op': utilidad_fab_op
            }

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('trn.change_ordentrabajo',
                     login_url='bases:sin_permisos')
def AprobacionPagoModalView(request, id_orden=None):
    template_name = "trn/aprobacion_pago_modal.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
            exclude(id_solicitud=None).first()
        sintalla = Tallas.objects.filter(talla=0).first()
        usuario_aprueba = Usuarios.objects.\
            filter(id=orden.usuario_aprueba_pago).first()

        costos_lista = []
        total_costos_asociados = 0.00

        if detalleitem:
            item = SolicitudTrabajo.objects.\
                filter(pk=detalleitem.id_solicitud).first()
            detalleSolicitud = DetalleSolicitud.objects.\
                filter(solicitud_id=item.id_solicitud).first()
            detalle = None
            costos_asociados = SolicitudRubros.objects.\
                filter(solicitud_id=item.id_solicitud)
            for costo in costos_asociados:
                costo_detalle = [
                    'rubro',
                    str(costo.rubro.descripcion),
                    str(costo.valor),
                    '1'
                ]
                costos_lista.append(costo_detalle)
                total_costos_asociados += float(costo.valor)
            total_costos_asociados = round(total_costos_asociados, 2)
            costos_lista = json.dumps(costos_lista)
        else:
            detalleitem = DetalleOrden.objects.filter(orden_id=id_orden).\
                exclude(id_item=None).first()
            item = Items.objects.filter(pk=detalleitem.id_item).first()
            detalle = DetalleItems.objects.\
                filter(id_item_id=item.id_item).first()
            detalleSolicitud = None
            adicionales = DetalleOrden.objects.filter(orden_id=id_orden)
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
                    costos_lista.append(adicional_detalle)
                    total_costos_asociados += \
                        (
                            float(item_adicional.precio) *
                            float(adicional.cantidad)
                        )
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
                    costos_lista.append(adicional_detalle)
                    total_costos_asociados += \
                        (
                            float(
                                item_adicional.precio
                            )*float(
                                adicional.cantidad
                            )
                        )
            total_costos_asociados = round(total_costos_asociados, 2)
            costos_lista = json.dumps(costos_lista)

        contexto = {
                    'orden': orden,
                    'item': item,
                    'detalle': detalle,
                    'detalleSolicitud': detalleSolicitud,
                    'sintalla': sintalla,
                    'total_costos_asociados': total_costos_asociados,
                    'costos_lista': costos_lista,
                    'usuario_aprueba': usuario_aprueba
                    }

    if request.method == 'POST':
        orden = OrdenTrabajo.objects.filter(pk=id_orden).first()
        orden.pago_aprobado = True
        orden.usuario_aprueba_pago = request.user.id
        orden.fecha_aprueba_pago = datetime.now(timezone.utc)
        orden.save()

    return render(request, template_name, contexto)


class EnvioMaterialView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        file_serializer = EnvioMaterialSerializer(orden, data=request.data)
        if file_serializer.is_valid():
            orden.fecha_envio_mat = datetime.now(timezone.utc)
            if orden.externa:
                orden.estado_id = 16
            else:
                orden.estado_id = 13
            orden.usuario_modifica = request.user.id
            orden.save()
            file_serializer.save()
            return Response(file_serializer.data, status=200)
        else:
            return Response(file_serializer.errors, status=400)


class RecibirMaterialView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        file_serializer = RecibirMaterialSerializer(orden, data=request.data)
        if file_serializer.is_valid():
            orden.fecha_recibe_mat = datetime.now(timezone.utc)
            orden.estado_id = 14
            orden.usuario_modifica = request.user.id
            orden.save()
            file_serializer.save()
            return Response(file_serializer.data, status=200)
        else:
            return Response(file_serializer.errors, status=400)


class AnularOrdenView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = AnularOrdenSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.fecha_anulacion = datetime.now(timezone.utc)
            orden.estado_id = 18
            orden.usuario_modifica = request.user.id
            orden.save()
            id_transaccion = orden.id_orden
            tipo_transaccion = 2
            NotificacionOrdenesActualizar.delay(
                orden.tienda_id,
                orden.taller_id,
                id_transaccion,
                tipo_transaccion,
                orden.estado_id
            )

            serializador.save()
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)

class FinalizarTrabajoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = FinalizarTrabajoSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.fecha_fin_trabajo = datetime.now(timezone.utc)
            orden.estado_id = 15
            orden.usuario_modifica = request.user.id
            peso_final = float(request.POST['peso_final'])
            imagenes = request.FILES.getlist('imagen')
            if imagenes:
                for imagen in imagenes:
                    infoImg = OrdenesImagenes(
                        usuario_crea=request.user.id,
                        imagen=imagen,
                        orden=orden,
                        pais=request.user.pais
                    )
                    if infoImg:
                        infoImg.save()
            orden.peso_final = peso_final
            # orden.total_taller_recalculado = orden.total_taller
            if orden.taller.recalcular_precio:

                orden.costo_gramo_base_taller = request.\
                    POST['costo_gramo_base_taller']
                orden.precio_gramo_base_taller = request.\
                    POST['precio_gramo_base_taller']
                    # POST.get('precio_gramo_base_taller', 0.00)
                orden.prct_utilidad_base_taller = request.\
                    POST['prct_utilidad_base_taller']
                orden.costo_base_total_ta = request.POST['costo_base_total_ta']

                orden.utilidad_base_taller = request.POST['utilidad_base_taller']
                orden.precio_base_total_ta = request.POST['precio_base_total_ta']

                orden.costo_fabricacion_unitario = request.\
                    POST['costo_fabricacion_unitario']
                orden.costo_total_fabricacion_ta = request.\
                    POST['costo_total_fabricacion_ta']
                # print(orden.prct_util_sobre_fabrica_ta)
                # orden.prct_util_sobre_fabrica_ta = float(request.POST['prct_util_fabricacion_taller'])
                # print(orden.prct_util_sobre_fabrica_ta, 'prct utili sobre fabrica ta')
                orden.util_sobre_fabrica_ta = request.\
                    POST['utilidad_fabricacion_taller']
                orden.precio_fabricacion_unitario = request.\
                    POST['precio_fabricacion_unitario']

                orden.precio_fabricacion_total = request.\
                    POST['precio_fabricacion_total_ta']
                orden.costo_piedras_basicas = request.POST['costo_piedras_basicas']
                orden.costo_color_unitario = request.POST['costo_color_unitario']
                orden.costo_color_total = request.POST['costo_color_total']
                orden.subtotal_taller = request.POST['subtotal_taller']
                orden.prct_impuestos_ta = request.POST['prct_impuestos_taller']
                orden.impuestos_taller = request.POST['impuestos_taller']
                orden.total_taller_recalculado = request.POST['total_taller']
                orden.costo_gramo_base_op = request.POST['costo_gramo_base_op']
                orden.precio_gramo_base_op = request.POST['precio_gramo_base_op']
                orden.costo_base_total_op = request.POST['costo_base_total_op']
                orden.prct_util_sobre_base_op = request.\
                    POST['prct_utilidad_base_op']
                orden.util_sobre_base_op = request.POST['utilidad_base_op']
                orden.precio_base_total_op = request.POST['precio_base_total_op']
                orden.prct_util_sobre_fabrica_op = request.\
                    POST['prct_util_fabricacion_op']
                orden.precio_unitario_op = request.POST['precio_unitario_op']
                orden.util_sobre_fabrica_op = request.\
                    POST['utilidad_fabricacion_op']
                orden.precio_fabricacion_total_op = request.\
                    POST['precio_fabricacion_total_op']
                orden.subtotal_op = request.POST['subtotal_op']
                orden.impuestos_op = request.POST['impuestos_op']
                orden.total_fabricacion_op = request.POST['total_fabricacion_op']
                orden.subtotal_orden = request.POST['subtotal_orden']
                orden.prct_impuestos_op = request.POST['prct_impuestos_joyeria']
                orden.impuestos_orden = request.POST['impuestos_orden']
                orden.precio_sistema = request.POST['precio_sistema']
                orden.descuento_orden = request.POST['descuento']
                orden.precio_recalculado = request.POST['precio_final_orden']
                # orden.precio_final_venta = request.POST['precio_sistema']
            orden.save()
            serializador.save()
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)



class EnviarProductoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
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

        serializador = EnviarProductoSerializer(orden, data=request.data)

        if serializador.is_valid():
            serializador.save()
            orden.fecha_envio_prod = datetime.now(timezone.utc)
            orden.estado_id = 16
            orden.usuario_modifica = request.user.id
            # print(orden.subtotal_taller)
            # orden.subtotal_taller = orden.subtotal_taller + orden.costo_envio
            # orden.impuestos_taller = (float(orden.subtotal_taller) * (1 + 0.12)) - float(orden.subtotal_taller)
            # orden.impuestos_taller = (round(orden.impuestos_taller, 2))
            # orden.subtotal_orden = float(orden.subtotal_orden) + float(orden.costo_envio)
            # print(orden.subtotal_orden)
            # print(orden.prct)
            # orden.impuestos_op = float(orden.subtotal_orden) * float(orden.prct_impuestos_op/100)
            # print(orden.impuestos_op)
            # orden.precio_sistema = orden.subtotal_orden + orden.impuestos_op
            # orden.precio_recalculado = orden.subtotal_orden + orden.impuestos_op
            # if orden.total_taller_recalculado != None and orden.costo_envio != 0:
                # orden.total_taller_recalculado = float(orden.subtotal_taller) + float(orden.impuestos_taller)
            # else:
                # orden.total_taller = float(orden.subtotal_taller) + float(orden.impuestos_taller)

            orden.save()

            if not orden.externa:
                # tienda_id =  Tiendas.objects.filter(zona_id=self.request.user.zona).first()
                principal = True
                postergada = False
                id_transaccion = orden.id_orden
                tipo_transaccion = 2
                tipo_notificacion = 1
                NotificacionOrdenes.delay(
                    request.user.id,
                    orden.tienda_id,
                    orden.taller_id,
                    producto,
                    principal,
                    postergada,
                    id_transaccion,
                    tipo_transaccion,
                    orden.estado_id,
                    tipo_notificacion
                )
            pass
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)




class CrearFactura(APIView):
    def post(self, request):
        body = json.loads(self.request.body)
        numero_factura = body.get('numeroFactura')
        factura = Facturas.objects.filter(numero_factura=numero_factura)
        infoFactura = Facturas(
            numero_factura=numero_factura,
            taller=self.request.user.taller(),
            estado_id=21,
            usuario_crea=self.request.user.id
        )
        if infoFactura:
            infoFactura.save()
            response = JsonResponse(
                {'mensaje': 'ok'},
                status=200
                )
        else:
            response = JsonResponse(
                {'mensaje': 'error'},
                status=500
                )
        return response



class AprobarRevisionOrden(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id_orden=None):
        orden = OrdenTrabajo.objects.\
            filter(id_orden=id_orden).first()
        orden.orden_revisada = True
        orden.usuario_registra_revision = self.request.user.id
        orden.fecha_revision = datetime.now(timezone.utc)
        orden.save()
        return Response({'mensaje': 'correcto'}, status=200)



class AprobarPagoOrden(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id_orden=None):
        orden = OrdenTrabajo.objects.\
            filter(id_orden=id_orden).first()
        orden.pago_aprobado = True
        orden.usuario_aprueba_pago = self.request.user.id
        orden.fecha_aprueba_pago = datetime.now(timezone.utc)
        orden.save()
        return Response({'mensaje': 'correcto'}, status=200)




class RecibirProductoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        detalle_orden = DetalleOrden.objects.filter(orden_id = orden.id_orden).first()

        
        serializador = RecibirProductoSerializer(orden, data=request.data)
        if serializador.is_valid():
            
            orden.fecha_recibe_prod = datetime.now(timezone.utc)
            orden.estado_id = 17
            #notificacion para el taller, confirmando haber recibido producto
            tipo_notificacion = 2
            if detalle_orden.id_solicitud:
                detalle = DetalleSolicitud.objects.filter(solicitud_id=detalle_orden.id_solicitud).first()
                producto_id = int(detalle.item_id)
                producto_obj = Items.objects.filter(id_item=producto_id).first()
                producto = producto_obj.descripcion
            else:
                producto_id = int(detalle_orden.id_item)
                producto_obj = Items.objects.filter(id_item=producto_id).first()
                producto = producto_obj.descripcion
            print(producto_id)
            print(producto_obj)
            print(producto)
            print('**********************/******')

            postergada = 0
            principal = 1
            id_transaccion = orden.id_orden
            tipo_transaccion = 2
            id_estado = orden.estado_id
            NotificacionOrdenes.delay(
                        request.user.id,
                        orden.tienda_id,
                        orden.taller_id,
                        producto,
                        principal,
                        postergada,
                        id_transaccion,
                        tipo_transaccion,
                        id_estado,
                        tipo_notificacion
                    )
            orden.usuario_modifica = request.user.id
            if detalle_orden.id_solicitud:
                detalle = DetalleSolicitud.objects.filter(solicitud_id=detalle_orden.id_solicitud).first()
                item = int(detalle.item_id)
            else:
                item = int(detalle_orden.id_item)



            item = Items.objects.filter(id_item=item).first()
            print(item, 'item')
            solicitud_orden = SolicitudTrabajo.objects.filter(id_solicitud=detalle_orden.id_solicitud).first()
            if solicitud_orden:
                limite_venta = solicitud_orden.tiempo_ent_max
            else:
                limite_venta = item.tiempo_entrega_max
            tiempo_limite_vta = \
                datetime.now(timezone.utc) + \
                timedelta(days=int(limite_venta))
            kwargs = {'id_transaccion': orden.id_orden}
            kwargs = json.dumps(kwargs)
            
            nombre_tarea = 'limiteventa_' + str(request.user.id) + \
                '_' + str(orden.id_orden)

            periodo, _ = CrontabSchedule.objects.get_or_create(
                minute=tiempo_limite_vta.minute,
                hour=tiempo_limite_vta.hour,
                day_of_week='*',
                day_of_month=tiempo_limite_vta.day,
                month_of_year=tiempo_limite_vta.month
                # timezone=zona_horaria
            )

            tarea = PeriodicTask.objects.filter(
                name=nombre_tarea
            ).first()

            if tarea:
                tarea.crontab = periodo
                tarea.kwargs = kwargs
                tarea.save()
            else:
                PeriodicTask.objects.create(
                    crontab=periodo,
                    name=nombre_tarea,
                    task='ntf.tasks.NotificacionLimiteVenta',
                    kwargs=kwargs
                )
            orden.save()
            serializador.save()
            enviarCorreoCliente.delay(orden.id_orden)
            # enviarCorreoZonal.delay(orden.id_orden)
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)


class CargarDocumentosTaller(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):

        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        factura = Facturas.objects.filter(id_factura=request.data['numeroFactura']).first()
        
        serializador = CargarDocTallerSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.usuario_modifica = self.request.user.id
            orden.numero_factura = factura.numero_factura
            orden.orden_facturada = 1
            orden.usuario_registra_factura = self.request.user.id
            orden.fecha_facturacion = datetime.now(timezone.utc)
            

            detalle = DetallesFacturas.objects.filter(orden_id=orden.id_orden).exists()
            if detalle == False:
                detalle_factura = DetallesFacturas(factura_id = factura.id_factura,\
                                                    orden_id = orden.id_orden)
                orden.save()
                detalle_factura.save()
                serializador.save()
            else:
                estado = 2
                return JsonResponse({'estado': estado})
            
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)



class PagarOrden(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id_orden=None):
        orden = OrdenTrabajo.objects.\
            filter(id_orden=id_orden).first()
        orden.orden_pagada = True
        orden.usuario_registra_pago = self.request.user.id
        orden.fecha_pago = datetime.now(timezone.utc)
        orden.save()
        return Response({'mensaje': 'correcto'}, status=200)





class CargarDocumentosOperaciones(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = CargarDocOpSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.usuario_modifica = request.user.id
            serializador.save()
            orden.save()
            # orden.estado_id = 19
            # orden.save()
            return Response(serializador.data, status=200)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=400)


class DevolverProductoView(APIView):

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = EnviarProductoSerializer(orden, data=request.data)

        
        if serializador.is_valid():
            body = json.loads(self.request.body)
            observacion_id = body.get('id_observacion')
            observacion_adicional = body.get('observacion_adicional')

            orden.fecha_envio_prod = datetime.now(timezone.utc)
            orden.estado_id = 11
            orden.usuario_modifica = request.user.id
            orden.rechazo_id = observacion_id
            orden.obs_recepcion_prod = observacion_adicional
            orden.save()
            registros = str(orden.taller.secuencia_ordenes+1)
            while len(registros) < 5:
                registros = '0' + registros
            secuencia = orden.taller.nombre + '-' + registros
            nueva_orden = OrdenTrabajo(
                secuencia= secuencia,
                origen_material_id= orden.origen_material_id,
                externa=orden.externa,
                env_material=orden.env_material,
                color_id=orden.color_id,
                estado_id=12,
                pais_id=orden.pais_id,
                proveedor_id=orden.proveedor_id,
                taller_id=orden.taller_id,
                tienda_id=orden.tienda_id,
                usuario_crea=request.user.id,
                cliente_id=orden.cliente_id,
                peso_solicitado=orden.peso_solicitado,
                categoria_id=orden.categoria_id,

                # campos que aparecen nulos al generear la nueva orden
                costo_gramo_base_taller=orden.costo_gramo_base_taller,
                precio_gramo_base_taller=orden.precio_gramo_base_taller,
                costo_fabricacion_unitario=orden.costo_fabricacion_unitario,
                precio_fabricacion_unitario=orden.precio_fabricacion_unitario,
                costo_total_fabricacion_ta=orden.costo_total_fabricacion_ta,
                precio_fabricacion_total=orden.precio_fabricacion_total,
                prct_util_sobre_fabrica_ta=orden.prct_util_sobre_fabrica_ta,
                util_sobre_fabrica_ta=orden.util_sobre_fabrica_ta,
                subtotal_taller=orden.subtotal_taller,
                prct_impuestos_ta=orden.prct_impuestos_ta,
                impuestos_taller=orden.impuestos_taller,
                total_taller=orden.total_taller,
                costo_piedras_taller=orden.costo_piedras_taller,
                util_sobre_piedras_taller=orden.util_sobre_piedras_taller,
                precio_piedras_taller=orden.precio_piedras_taller,
                costo_adicionales_taller=orden.costo_adicionales_taller,
                costo_gramo_base_op=orden.costo_gramo_base_op,
                precio_gramo_base_op=orden.precio_gramo_base_op,
                costo_base_total_op=orden.costo_base_total_op,
                precio_base_total_op=orden.precio_base_total_op,
                util_sobre_base_op=orden.util_sobre_base_op,
                prct_util_sobre_fabrica_op=orden.prct_util_sobre_fabrica_op,
                util_sobre_fabrica_op=orden.util_sobre_fabrica_op,
                precio_unitario_op=orden.precio_unitario_op,
                precio_fabricacion_total_op=orden.precio_fabricacion_total_op,
                subtotal_orden=orden.subtotal_orden,
                prct_impuestos_op=orden.prct_impuestos_op,
                impuestos_op=orden.impuestos_op,
                descuento_orden=orden.descuento_orden,
                precio_sistema=orden.precio_sistema,
                precio_final_venta=orden.precio_final_venta,
                prct_utilidad_base_taller=orden.prct_utilidad_base_taller,
                utilidad_base_taller=orden.utilidad_base_taller,
                costo_base_total_ta=orden.costo_base_total_ta,
                precio_base_total_ta=orden.precio_base_total_ta,
                costo_total_rubros=orden.costo_total_rubros
            )
            if nueva_orden:
                nueva_orden.save()
                nueva_orden.taller.secuencia_ordenes += 1
                nueva_orden.taller.save()

                # adicionales, rubros o piedras que esten relacionados con la orden anterior.
                adicional_orden = OrdenesAdicionales.objects.filter(orden_id=orden.id_orden)
                if adicional_orden:
                    for adicional in adicional_orden:
                        nuevo_adicional_orden = OrdenesAdicionales(
                            cantidad_adicionales=adicional.cantidad_adicionales,
                            costo_adicional_taller=adicional.costo_adicional_taller,
                            precio_adicional_taller=adicional.precio_adicional_taller,
                            prct_utilidad_adicional_op=adicional.prct_utilidad_adicional_op,
                            precio_adicional_op=adicional.precio_adicional_op,
                            subtotal_adicional_taller=adicional.subtotal_adicional_taller,
                            subtotal_adicional_op=adicional.subtotal_adicional_op,
                            adicional_id=adicional.adicional_id,
                            orden_id=nueva_orden.id_orden
                        )
                        if nuevo_adicional_orden:
                            nuevo_adicional_orden.save()

                # agregar piedrs a la nueva orden que se genera
                piedras_orden = OrdenesPiedras.objects.filter(orden_id=orden.id_orden)
                if piedras_orden:
                    for piedra in piedras_orden:
                        nueva_piedra_orden = OrdenesPiedras(
                            cantidad_piedras=piedra.cantidad_piedras,
                            costo_piedra_taller=piedra.costo_piedra_taller,
                            precio_piedra_taller=piedra.precio_piedra_taller,
                            prct_utilidad_piedra_op=piedra.prct_utilidad_piedra_op,
                            precio_piedra_op=piedra.precio_piedra_op,
                            subtotal_piedras_taller=piedra.subtotal_piedras_taller,
                            subtotal_piedras_op=piedra.subtotal_piedras_op,
                            piedra_id=piedra.piedra_id,
                            piedra_detalle_id=piedra.piedra_detalle_id,
                            orden_id=nueva_orden.id_orden
                        )
                        if nueva_piedra_orden:
                            nueva_piedra_orden.save()

                # adicionales, rubros o piedras agregadas a la nueva orden
                # (falta hacer prueba con rubros y piedras)

                detalles_orden = DetalleOrden.objects.\
                    filter(orden_id=orden.id_orden)
                if detalles_orden:
                    for detalle in detalles_orden:
                        if detalle.id_solicitud:
                            detalle_solicitud_item = DetalleSolicitud.objects.\
                                filter(
                                    solicitud_id=detalle.id_solicitud
                                ).first()
                            nuevo_detalle = DetalleOrden(
                                id_solicitud=detalle.id_solicitud,
                                orden_id=nueva_orden.id_orden,
                                pais_id=nueva_orden.pais_id,
                                usuario_crea=request.user.id,
                                id_item=detalle_solicitud_item.item_id
                            )
                        else:
                            nuevo_detalle = DetalleOrden(
                                id_item=detalle.id_item,
                                id_detalle_item=detalle.id_detalle_item,
                                orden_id=nueva_orden.id_orden,
                                pais_id=nueva_orden.pais_id,
                                usuario_crea=request.user.id
                            )
                        if nuevo_detalle:
                            nuevo_detalle.save()
            serializador.save()
            # notificacion de la orden nueva que
            # se genero cuando, se devolvio la anterior
            producto_id = int(nuevo_detalle.id_item)
            producto_obj = Items.objects.filter(id_item=producto_id).first()
            producto = producto_obj.descripcion

            id_transaccion=nueva_orden.id_orden
            tipo_transaccion=2
            tipo_notificacion = 2
            principal=1
            postergada=0
            NotificacionOrdenes.delay(
                self.request.user.id,
                nueva_orden.tienda_id,
                nueva_orden.taller_id,
                producto,
                principal,
                postergada,
                id_transaccion,
                tipo_transaccion,
                nueva_orden.estado_id,
                tipo_notificacion
            )
            
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)


class FinalizarOrdenView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = FinalizarOrdenSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.fecha_venta = datetime.now(timezone.utc)
            orden.estado_id = 19
            orden.usuario_modifica = request.user.id
            orden.orden_vendida = True
            orden.save()
            id_transaccion = orden.id_orden
            tipo_transaccion = 2
            NotificacionOrdenesActualizar.delay(
                orden.tienda_id,
                orden.taller_id,
                id_transaccion,
                tipo_transaccion,
                orden.estado_id
            )
            
            serializador.save()
            resta_minutos = \
                round((((orden.fecha_venta - orden.fecha_creacion)
                      .seconds)/60), 1)
            orden.tiempo_duracion_orden = resta_minutos
            orden.save()
            return Response(serializador.data, status=200)
        else:
            return Response(serializador.errors, status=400)


class FinalizarSinVentaView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=None):
        orden = OrdenTrabajo.objects.filter(id_orden=pk).first()
        serializador = FinalizarSinVentaSerializer(orden, data=request.data)
        if serializador.is_valid():
            orden.fecha_venta = datetime.now(timezone.utc)
            orden.estado_id = 19
            orden.usuario_modifica = request.user.id
            orden.orden_vendida = False
            orden.save()
            serializador.save()
            resta_minutos = \
                round((((orden.fecha_venta - orden.fecha_creacion)
                      .seconds)/60), 1)
            orden.tiempo_duracion_orden = resta_minutos
            orden.save()
            id_transaccion = orden.id_orden
            tipo_transaccion = 2
            NotificacionOrdenesActualizar.delay(
                orden.tienda_id,
                orden.taller_id,
                id_transaccion,
                tipo_transaccion,
                orden.estado_id
            )
            return Response(serializador.data, status=200)
        else:
            print(serializador.errors)
            return Response(serializador.errors, status=400)


class EnviarCorreoView(APIView):
    def get(self, request):
        resultado = enviarCorreo.delay()
        print(resultado.backend)
        enviarCorreo.delay()
        return Response("Correo enviado", status=status.HTTP_200_OK)

    def post(self, request):
        enviarCorreo.delay()
        return Response("Tarea recibida", status=status.HTTP_201_CREATED)


class ReporteOrdenesPagos(APIView):
    def post(self, request):
        body = json.loads(self.request.body)
        
        talleres_internos = body.get('talleresInternos')
        talleres_externos = body.get('talleresExternos')

        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            talleres_id = Talleres.objects.\
                filter(
                    nombre=self.request.user.taller().nombre
                ).\
                values('id_taller')
            zonas_id = Zonas.objects.\
                filter(
                    id_zona=self.request.user.zona,
                    estado__descripcion='ACTIVO'
                ).\
                values('id_zona')
        else:
            if (talleres_internos and talleres_externos) or\
                 (not talleres_internos and not talleres_externos):
                talleres_id = Talleres.objects.\
                    filter(
                        pais=self.request.user.pais
                    ).\
                    values('id_taller') | Talleres.objects.\
                    filter(
                        nombre='NEUTRO'
                    ).values('id_taller')
            elif talleres_internos:
                talleres_id = Talleres.objects.\
                    filter(
                        pais=self.request.user.pais
                    ).\
                    values('id_taller')
            else:
                talleres_id = Talleres.esobjects.\
                    filter(
                        nombre='NEUTRO'
                    ).values('id_taller')
            if self.request.user.rol.zonal:
                zonas_id = Zonas.objects.\
                    filter(
                        id_zona=self.request.user.zona
                    ).\
                    values('id_zona')
            else:
                zonas_id = Zonas.objects.\
                    filter(
                        estado__descripcion='ACTIVO'
                    ).\
                    values('id_zona')
        # print('***reporte***')
        # print(talleres_id)
        # print(zonas_id)
        ordenes = ObtenerOrdenesPagos(
            body,
            talleres_id,
            zonas_id,
            self.request.user)
        if ordenes:
            ahora = datetime.now(timezone.utc)

            ordenes_resource = OrdenesResource()
            dataset = ordenes_resource.export(ordenes)
            nombre_archivo = 'Reporte_ordenes_pago' + ahora.strftime('%d-%m-%Y') + '.xls'
            response = HttpResponse(
                dataset.xls,
                content_type='application/vnd.ms-excel'
                )
            response['Content-Disposition'] = 'attachment; filename=' \
                + nombre_archivo
        else:
            response = HttpResponse('No existen ordenes')
        return response

# reporte usuarios

class ReporteUsuarios(APIView):
    def post(self, request):
        body = json.loads(self.request.body)
        # talleres_internos = body.get('talleresInternos')
        # talleres_externos = body.get('talleresExternos')

        # if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
        #     talleres_id = Talleres.objects.\
        #         filter(
        #             nombre=self.request.user.taller().nombre
        #         ).\
        #         values('id_taller')
        #     zonas_id = Zonas.objects.\
        #         filter(
        #             id_zona=self.request.user.zona,
        #             estado__descripcion='ACTIVO'
        #         ).\
        #         values('id_zona')
        # else:
        #     if (talleres_internos and talleres_externos) or\
        #          (not talleres_internos and not talleres_externos):
        #         talleres_id = Talleres.objects.\
        #             filter(
        #                 pais=self.request.user.pais
        #             ).\
        #             values('id_taller') | Talleres.objects.\
        #             filter(
        #                 nombre='NEUTRO'
        #             ).values('id_taller')
        #     elif talleres_internos:
        #         talleres_id = Talleres.objects.\
        #             filter(
        #                 pais=self.request.user.pais
        #             ).\
        #             values('id_taller')
        #     else:
        #         talleres_id = Talleres.esobjects.\
        #             filter(
        #                 nombre='NEUTRO'
        #             ).values('id_taller')
        #     if self.request.user.rol.zonal:
        #         zonas_id = Zonas.objects.\
        #             filter(
        #                 id_zona=self.request.user.zona
        #             ).\
        #             values('id_zona')
        #     else:
        #         zonas_id = Zonas.objects.\
        #             filter(
        #                 estado__descripcion='ACTIVO'
        #             ).\
        #             values('id_zona')
        # ordenes = ObtenerOrdenesPagos(
        #     body,
        #     talleres_id,
        #     zonas_id,
        #     self.request.user)
        # if ordenes:
        #     ahora = datetime.now(timezone.utc)

        #     ordenes_resource = OrdenesResource()
        #     dataset = ordenes_resource.export(ordenes)
        #     nombre_archivo = 'Reporte_' + ahora.strftime('%d-%m-%Y') + '.xls'
        #     response = HttpResponse(
        #         dataset.xls,
        #         content_type='application/vnd.ms-excel'
        #         )
        #     response['Content-Disposition'] = 'attachment; filename=' \
        #         + nombre_archivo
        # else:
        response = HttpResponse('No existen ordenes')
        return response



def ReporteOrdenesListaExcel(request, f_inicio, f_fin, opcion):
    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
    f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()

    # operaciones
    tiendas_id = UsuariosTiendas.objects.filter(usuario_id=request.user.id).values('tienda_id')
    if request.user.tipo_usuario.descripcion == "USUARIO OPERACIONES":
        if opcion == 1:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_actual,
                        fecha_creacion__lte=ahora
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 2:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__zona__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_anterior,
                        fecha_creacion__lte=dia_uno_mes_actual
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 3:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial()
                    ).order_by('estado__orden', '-fecha_modificacion')[:100]
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
        if opcion == 4:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')[:1000]
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
        if opcion == 5:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=f_inicio,
                        fecha_creacion__lte=f_fin + timedelta(days=1)
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 6:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = OrdenTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = OrdenTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by('estado__orden', '-fecha_modificacion')
        if request.user.rol.descripcion == 'ADMIN OPERACIONES':
            solicitudes = SolicitudTrabajo.objects.filter(
                tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                estado__descripcion='ESPERA COTIZACION TALLER'
            ) | SolicitudTrabajo.objects.filter(
                tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                estado__descripcion='ESPERA DE EVALUACION'
            )
        else:
            if request.user.rol.zonal:
                solicitudes = SolicitudTrabajo.objects.filter(
                    tienda__zona_id=request.user.zona,
                    estado__descripcion='ESPERA COTIZACION TALLER'
                ) | SolicitudTrabajo.objects.filter(
                    tienda__zona_id=request.user.zona,
                    estado__descripcion='ESPERA DE EVALUACION'
                )
            else:
                solicitudes = SolicitudTrabajo.objects.filter(
                    tienda_id__in=tiendas_id,
                    estado__descripcion='ESPERA COTIZACION TALLER'
                ) | SolicitudTrabajo.objects.filter(
                    tienda_id__in=tiendas_id,
                    estado__descripcion='ESPERA DE EVALUACION'
                )
        if solicitudes:
            solicitudes = solicitudes.\
                order_by('estado__orden', '-fecha_modificacion')
    # taller
    else:
        if opcion == 1:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=dia_uno_mes_actual,
                    fecha_creacion__lte=ahora
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 2:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=dia_uno_mes_anterior,
                    fecha_creacion__lte=dia_uno_mes_actual
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 3:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')[:100]
        if opcion == 4:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')[:1000]
        if opcion == 5:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin + timedelta(days=1)
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 6:
            ordenes = OrdenTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')
    if ordenes:
        ordenes_resource = OrdenesListaResource()
        dataset = ordenes_resource.export(ordenes)
        nombre_archivo = 'Reporte_lista_ordenes_' + ahora.strftime('%d-%m-%Y') + '.xls'
        response = HttpResponse(
            dataset.xls,
            content_type='application/vnd.ms-excel'
            )
        response['Content-Disposition'] = 'attachment; filename=' \
            + nombre_archivo
    else:
        response = HttpResponse('No existen ordenes')
    return response


class FacturasDetalles(APIView):
    def get(self, request, id_factura):
        factura = Facturas.objects.\
            filter(pk=id_factura).first()
        detalles_factura = DetallesFacturas.objects.\
            filter(factura=factura)
        factura = FacturasSerializer(factura).data
        detalles_factura = DetallesFacturasSerializer(
            detalles_factura,
            many=True
        ).data
        response = JsonResponse(
            {
                'factura': factura,
                'detalles_factura': detalles_factura
            },
            status=200
        )
        return response
        


class ObtenerFacturasCreadas(APIView):
    def get(self, request, id_taller):
        facturas = Facturas.objects.filter(
            taller_id=id_taller,
            estado__descripcion='CREADA'
        )
        facturas = FacturasSerializer(facturas, many=True).data
        return JsonResponse(
            {'facturas': facturas},
            status=200
        )


class FacturasListaView(SinPermisos, generic.TemplateView):
    permission_required = "trn.view_facturas"
    template_name = "trn/facturas_lista.html"
    login_url = "bases:login"

    # def get_context_data(self, **kwargs):
    #     context = super(TipoSolicitudView, self).get_context_data(**kwargs)
    #     id_item = self.kwargs['id_item']
    #     context['item'] = Items.objects.filter(id_item=id_item).first()
    #     context['proveedores'] = Proveedores.objects.filter(
    #         taller=1,
    #         pais_id=self.request.user.pais_id
    #     ).count()
    #     return context




@login_required(login_url='/login/')
def validarFactura(request):
    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        numero = request.GET.get("numero", None)
        orden = request.GET.get("orden", None)
        if numero:
            try:
                factura_obj = Facturas.objects.filter(numero_factura=numero).exists()
                if factura_obj:
                    estado = 2
                else:
                    infoFactura = Facturas(
                        numero_factura=numero,
                        taller=request.user.taller(),
                        estado_id=21,
                        usuario_crea=request.user.id
                    )
                    if infoFactura:
                        infoFactura.save()
                        # infoDetalle = DetallesFacturas(factura_id=infoFactura.id_factura, orden_id=orden)
                        # if infoDetalle:
                        #     infoDetalle.save()
                        estado = 1
            except Facturas.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)



class ObtenerFacturas(APIView):
    def post(self, request, id_taller):
        facturas = Facturas.objects.filter(
            taller_id=id_taller
        )
        filtros = self.request
        tipo_usuario = self.request.user.tipo_usuario.descripcion
        if tipo_usuario == 'USUARIO TALLER':
            talleres = Talleres.objects.filter(
                nombre=self.request.user.taller()
            ).values('id_taller')
        else:
            talleres = Talleres.objects.filter(
                pais=self.request.user.pais
            ).values('id_taller')
        facturas = BusquedaFacturas(
            filtros,
            tipo_usuario,
            talleres
        )
        registros = facturas.count()
        facturas = FacturasSerializer(facturas, many=True).data
        return JsonResponse(
            {
                'facturas': facturas,
                'registros': registros
            },
            status=200
        )


def BusquedaFacturas(filtros, tipo_usuario, talleres):
    estados = filtros.POST['estadosBusqueda[]']
    estados = json.loads(estados)
    clave_busqueda = filtros.POST['claveBusqueda']
    f_inicio = filtros.POST['fechaInicio']
    f_fin = filtros.POST['fechaFin']
    opcion = int(filtros.POST['opcion'])
    if len(estados) == 0:
        if tipo_usuario == 'USUARIO TALLER':
            estados = Estados.objects.filter(
                descripcion__in=[
                    'CREADA',
                    'CONFIRMADA',
                    'PAGADA'
                ]
            ).values('id_estado')
        else:
            estados = Estados.objects.filter(
                descripcion__in=[
                    'CONFIRMADA',
                    'PAGADA'
                ]
            ).values('id_estado')

    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    if opcion == 1:
        f_inicio = dia_uno_mes_actual
        f_fin = ahora
    if opcion == 2:
        f_inicio = dia_uno_mes_anterior
        f_fin = dia_uno_mes_actual
    if opcion == 3:
        f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
        f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()
    if opcion == 4:
        f_inicio = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
        f_fin = ahora
    facturas = Facturas.objects.filter(
        estado_id__in=estados,
        fecha_creacion__gte=f_inicio,
        fecha_creacion__lte=f_fin,
        taller_id__in=talleres
    )
    if clave_busqueda != '':
        facturas = facturas.\
            filter(
                numero_factura__icontains=clave_busqueda
            )
    return facturas.order_by('-fecha_creacion')




class FacturasActualizar(APIView):
    def post(self, request, id_factura):
        body = json.loads(self.request.body)
        estado = body.get('estado')
        factura = Facturas.objects.\
            filter(id_factura=id_factura).first()
        factura.estado = Estados.objects.filter(
            descripcion=estado
        ).first()
        factura.usuario_modifica = self.request.user.id
        factura.save()
        if estado == 'PAGADA':
            detalles_factura = DetallesFacturas.objects.\
                filter(factura=factura)
            for detalle in detalles_factura:
                detalle.orden.orden_pagada = True
                detalle.orden.usuario_registra_pago = self.request.user.id
                detalle.orden.fecha_pago = datetime.now(timezone.utc)
                detalle.orden.save()
        response = JsonResponse(
            {
                'mensaje': 'ok'
            },
            status=200
        )
        return response


class BorrarDetalleFactura(APIView):
    def post(self, request):
        body = json.loads(self.request.body)
        id_factura = body.get('id_factura')
        id_orden = body.get('id_orden')
        factura = Facturas.objects.\
            filter(id_factura=id_factura).first()
        orden = OrdenTrabajo.objects.\
            filter(id_orden=id_orden).first()

        if orden:
            orden.orden_facturada = False
            orden.usuario_registra_factura = None
            orden.fecha_facturacion = None
            orden.numero_factura = None
            orden.orden_pagada = False
            orden.save()
            detalle = DetallesFacturas.objects.\
                filter(
                    factura=factura,
                    orden=orden
                ).first()
            if detalle:
                detalle.delete()
        response = JsonResponse(
            {
                'mensaje': 'ok'
            },
            status=200
        )
        return response


class EliminarFactura(APIView):
    def post(self, request):
        body = json.loads(self.request.body)
        id_factura = body.get('id_factura')
        factura = Facturas.objects.\
            filter(id_factura=id_factura).first()
        detalles = DetallesFacturas.objects.\
            filter(factura=factura)
        if detalles:
            for detalle in detalles:
                detalle.orden.orden_facturada = False
                detalle.orden.usuario_registra_factura = None
                detalle.orden.fecha_facturacion = None
                detalle.orden.numero_factura = None
                detalle.orden.save()
                detalle.delete()
        factura.delete()
        response = JsonResponse(
            {
                'mensaje': 'ok'
            },
            status=200
        )
        return response


@login_required(login_url='/login/')
@permission_required('trn.add_ordentrabajo',
                     login_url='bases:sin_permisos')
def CrearOrdenAlianzaView(request, id_item=None, identificacion=None):
    template_name = "trn/ordenes_alianza_crear.html"
    form_rol = {}
    contexto = {}
    sociedad = 0
    item = Items.objects.filter(pk=id_item).first()
    # detalles = DetalleItems.objects.filter(id_item=item).\
    #     filter(estado__descripcion='ACTIVO')
    colores = ItemsColores.objects.filter(item=item)
    configuracion_op = request.user.grupo_empresarial()
    configuracion_ta = item.taller
    origen_material = OrigenMaterial.objects.all().\
        exclude(descripcion='NINGUNO')
    pieza = Piezas.objects.filter(
        item=item
    ).first()
    detalles = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza)

    acabados = PiezasAcabados.objects.filter(
        pieza=pieza
    )

    anchuras = Anchuras.objects.filter(
        taller=item.taller
    )
    talla_min_a = Tallas.objects.filter(
        id_talla=pieza.talla_minima_a
    ).first()
    talla_max_a = Tallas.objects.filter(
        id_talla=pieza.talla_maxima_a
    ).first()
    tallas_pieza_a = Tallas.objects.filter(
        talla__gte=talla_min_a.talla,
        talla__lte=talla_max_a.talla,
        taller=item.taller
    )
    talla_min_b = Tallas.objects.filter(
        id_talla=pieza.talla_minima_b
    ).first()
    talla_max_b = Tallas.objects.filter(
        id_talla=pieza.talla_maxima_b
    ).first()
    tallas_pieza_b = Tallas.objects.filter(
        talla__gte=talla_min_b.talla,
        talla__lte=talla_max_b.talla,
        taller=item.taller
    )
    partes_internas_id = PiezasDetalles.objects.filter(
        pieza=pieza
    ).values('parte_interna').distinct()
    partes_internas = PartesInternas.objects.filter(
        id_parte_interna__in=partes_internas_id
    )
    imagenes = ItemsImagenes.objects.filter(
        item=item
    )
    origen_pre = OrigenMaterial.objects.\
        filter(
            id_origen=request.user.grupo_empresarial().origen_material
        ).first()
    proveedor = item.proveedor()
    if proveedor:
        costo_fabricacion_unitario = proveedor.costo_gramo
    else:
        costo_fabricacion_unitario = item.costo_taller
    precio_definido_taller = item.categoria.precio_taller_obj()
    precio_definido_op = item.categoria.precio_empresa_obj()
    if precio_definido_op:
        prct_util_fabricacion_op = precio_definido_op.prct_utilidad
        precio_unitario_op = precio_definido_op.precio
        regla_calculo_op = precio_definido_op.tipo.regla_calculo.descripcion
    else:
        prct_util_fabricacion_op = configuracion_op.utilidad_sobre_taller
        precio_unitario_op = configuracion_op.precio_gramo_final
        tipo_precio = TiposPrecios.objects.\
            filter(id_tipo=configuracion_op.tipo_precio_predefinido).first()
        regla_calculo_op = tipo_precio.regla_calculo.descripcion
    # obtener tiendas para la orden
    tiendas_id = UsuariosTiendas.objects.filter(usuario_id=request.user.id).values('tienda_id')
    if request.user.rol.descripcion == 'ADMIN OPERACIONES':
        tiendas = Tiendas.objects.filter(sociedad__grupo_empresarial=request.user.grupo_empresarial())
    if tiendas_id:
        tiendas = Tiendas.objects.filter(id_tienda__in=tiendas_id)
        sociedad_tienda = tiendas.values('sociedad_id')
        sociedad = Sociedades.objects.filter(id_sociedad__in=sociedad_tienda).first()
    utilidad_fab_op = request.user.grupo_empresarial().utilidad_sobre_taller

    tooltips = ConfiguracionTooltipOperaciones.objects.\
        filter(
            estado=1,
            pais=request.user.pais_id,
            grupo=request.user.grupo_empresarial().id_grupo_empresarial
        )



    tool_orig_mat = ''
    tool_ant_fabr = ''

    for tool in tooltips:
        if tool.campo_orden == 'origen_material':
            tool_orig_mat = tool.texto
        if tool.campo_orden == 'anticipo_fabricacion':
            tool_ant_fabr = tool.texto

    if request.method == 'GET':

        contexto = {
                    'item': item,
                    'pieza': pieza,
                    'detalles': detalles,
                    'colores': colores,
                    'configuracion_op': configuracion_op,
                    'configuracion_ta': configuracion_ta,
                    'origen_material': origen_material,
                    'acabados': acabados,
                    'anchuras': anchuras,
                    'partes_internas': partes_internas,
                    'tallas_pieza_a': tallas_pieza_a,
                    'tallas_pieza_b': tallas_pieza_b,
                    'colores': colores,
                    'imagenes': imagenes,
                    'origen_pre': origen_pre,
                    'precio_definido_taller': precio_definido_taller,
                    'precio_definido_op': precio_definido_op,
                    'costo_fabricacion_unitario': costo_fabricacion_unitario,
                    'prct_util_fabricacion_op': prct_util_fabricacion_op,
                    'precio_unitario_op': precio_unitario_op,
                    'regla_calculo_op': regla_calculo_op,
                    'tiendas': tiendas,
                    'sociedad': sociedad,
                    'utilidad_fab_op': utilidad_fab_op,
                    'tool_orig_mat': tool_orig_mat,
                    'tool_ant_fabr': tool_ant_fabr
                    }

    if request.method == 'POST':
        cliente = Clientes.objects.filter(identificacion=identificacion).\
            first()
        
        # adicionales_lista = request.POST.getlist('adicionales_lista[]')
        piedras_lista = request.POST.getlist('piedrasLista[]')
        
        longitud_piedras = len(piedras_lista)

        tipo_transaccion = request.POST['tipo_transaccion']
        if tipo_transaccion == '1':
            id_pieza_detalle = request.POST['id_pieza_detalle']
            color = request.POST['id_color']
        if tipo_transaccion == '2':
            detalle_pieza = PiezasDetalles.objects.\
                filter(pieza_id=pieza.id_pieza, pieza__item=item).first()
            id_pieza_detalle = detalle_pieza.id_pieza_detalle
            color_item = ItemsColores.objects.\
                filter(item_id=item.id_item).first()
            color = color_item.color_id

        print(id_pieza_detalle)
        env_material = request.POST['env_material']
        if env_material == 'undefined' :
            env_material = False
        else:
            env_material = True
        peso_solicitado = request.POST['peso_solicitado']
        origen = request.POST['origen_material']
        datos_extra = request.POST['datos_extra']
        costo_adicionales = request.POST['costo_adicionales']
        precio_adicionales = request.POST['precio_adicionales']
        precio_adicionales_op = request.POST['precio_adicionales_op']
        costo_piedras = request.POST['costo_piedras']
        precio_piedras = request.POST['precio_piedras']
        precio_piedras_op = request.POST['precio_piedras_op']
        util_sobre_piedras = request.POST['util_sobre_piedras']
        util_sobre_piedras_op = request.POST['util_sobre_piedras_op']
        util_sobre_adicionales = request.POST['util_sobre_adicionales']
        util_sobre_adicionales_op = request.POST['util_sobre_adicionales_op']
        costo_gramo_base_taller = request.POST['costo_gramo_base_taller']
        precio_gramo_base_taller = request.POST['precio_gramo_base_taller']
        prct_utilidad_base_taller = request.POST['prct_utilidad_base_taller']
        costo_base_total_ta = request.POST['costo_base_total_ta']
        utilidad_base_taller = request.POST['utilidad_base_taller']
        precio_base_total_ta = request.POST['precio_base_total_ta']
        costo_fabricacion_unitario = request.POST['costo_fabricacion_unitario']
        costo_total_fabricacion_ta = request.POST['costo_total_fabricacion_ta']
        prct_util_fabricacion_taller = request.\
            POST['prct_util_fabricacion_taller']
        utilidad_fabricacion_taller = request.\
            POST['utilidad_fabricacion_taller']
        precio_fabricacion_unitario = request.\
            POST['precio_fabricacion_unitario']
        precio_fabricacion_total_ta = request.\
            POST['precio_fabricacion_total_ta']
        costo_piedras_basicas = request.POST['costo_piedras_basicas']
        costo_color_unitario = request.POST['costo_color_unitario']
        costo_color_total = request.POST['costo_color_total']
        subtotal_taller = request.POST['subtotal_taller']
        prct_impuestos_taller = request.POST['prct_impuestos_taller']
        impuestos_taller = request.POST['impuestos_taller']
        total_taller = request.POST['total_taller']
        costo_gramo_base_op = request.POST['costo_gramo_base_op']
        precio_base_total_op = request.POST['precio_base_total_op']

        precio_gramo_base_op = request.POST['precio_gramo_base_op']
        costo_base_total_op = request.POST['costo_base_total_op']
        prct_utilidad_base_op = request.POST['prct_utilidad_base_op']
        costo_base_total_op = request.POST['costo_base_total_op']
        utilidad_base_op = request.POST['utilidad_base_op']
        prct_util_fabricacion_op = request.POST['prct_util_fabricacion_op']
        precio_unitario_op = request.POST['precio_unitario_op']
        utilidad_fabricacion_op = request.POST['utilidad_fabricacion_op']
        precio_fabricacion_total_op = request.\
            POST['precio_fabricacion_total_op']
        subtotal_op = request.POST['subtotal_op']
        impuestos_op = request.POST['impuestos_op']
        total_fabricacion_op = request.POST['total_fabricacion_op']
        subtotal_orden = request.POST['subtotal_orden']
        prct_impuestos_joyeria = request.POST['prct_impuestos_joyeria']
        impuestos_orden = request.POST['impuestos_orden']
        precio_sistema = request.POST['precio_sistema']
        descuento = request.POST['descuento']
        precio_final_orden = request.POST['precio_final_orden']

        tienda_id = request.POST['tienda']
        if tienda_id:
            tienda= Tiendas.objects.filter(id_tienda=tienda_id).first()

        talla_mujer = request.POST['talla_a']
        talla_a = Tallas.objects.filter(id_talla=talla_mujer).first()
        talla_hombre = request.POST['talla_b']
        talla_b = Tallas.objects.filter(id_talla=talla_hombre).first()

        inscripcion_mujer = request.POST['inscripcion_mujer']
        inscripcion_hombre = request.POST['inscripcion_hombre']

        origen_material = OrigenMaterial.objects.\
            filter(descripcion=origen).first()

        if env_material:
            estado = 12
        else:
            estado = 20



        if item:
                                        
            registros = str(item.taller.secuencia_ordenes+1)
            while len(registros) < 5:
                registros = '0' + registros
            secuencia = item.taller.nombre + '-' + registros
            infoOrden = OrdenTrabajo(
                secuencia=secuencia,
                cliente=cliente,
                tienda=tienda,
                taller=item.taller,
                proveedor=proveedor,
                pais=request.user.pais,
                categoria=item.categoria,
                color_id=color,
                datos_extra=datos_extra,
                externa=0,
                origen_material=origen_material,
                env_material=env_material,
                peso_solicitado=peso_solicitado,
                unidades_solicitadas=1,
                # valores
                costo_gramo_base_taller=costo_gramo_base_taller,
                precio_gramo_base_taller=precio_gramo_base_taller,
                prct_utilidad_base_taller=prct_utilidad_base_taller,
                utilidad_base_taller=utilidad_base_taller,
                costo_base_total_ta=costo_base_total_ta,
                precio_base_total_ta=precio_base_total_ta,
                costo_fabricacion_unitario=costo_fabricacion_unitario,
                precio_fabricacion_unitario=precio_fabricacion_unitario,
                costo_total_fabricacion_ta=costo_total_fabricacion_ta,
                precio_fabricacion_total=precio_fabricacion_total_ta,
                prct_util_sobre_fabrica_ta=prct_util_fabricacion_taller,
                util_sobre_fabrica_ta=utilidad_fabricacion_taller,
                costo_color_unitario=costo_color_unitario,
                costo_color_total=costo_color_total,
                subtotal_taller=subtotal_taller,
                prct_impuestos_ta=prct_impuestos_taller,
                impuestos_taller=impuestos_taller,
                costo_piedras_basicas=costo_piedras_basicas,
                total_taller=total_taller,
                
                # costo_adicionales=costo_adicionales,

                costo_gramo_base_op=costo_gramo_base_op,
                precio_gramo_base_op=precio_gramo_base_op,
                prct_util_sobre_base_op=prct_utilidad_base_op,
                costo_base_total_op=costo_base_total_op,
                precio_base_total_op=precio_base_total_op,
                util_sobre_base_op=utilidad_base_op,
                prct_util_sobre_fabrica_op=prct_util_fabricacion_op,
                util_sobre_fabrica_op=utilidad_fabricacion_op,
                precio_unitario_op=precio_unitario_op,
                precio_fabricacion_total_op=precio_fabricacion_total_op,
                subtotal_orden=subtotal_orden,
                prct_impuestos_op=prct_impuestos_joyeria,
                impuestos_op=impuestos_op,
                descuento_orden=descuento,
                precio_sistema=precio_sistema,
                precio_final_venta=precio_final_orden,
                estado_id=estado,
                usuario_crea=request.user.id,
            )
            if infoOrden:
                infoOrden.save()
                infoOrden.taller.secuencia_ordenes += 1
                infoOrden.taller.save()
                form = OrdenAnticipoForm(
                    instance=infoOrden,
                    data=request.POST,
                    files=request.FILES
                )
                if form.is_valid():
                    form.save()

            infoDetalle = DetalleOrden(
                id_item=item.id_item,
                orden=infoOrden,
                pais=infoOrden.pais,
                usuario_crea=request.user.id,
                talla_mujer=talla_a.talla,
                talla_hombre=talla_b.talla,
                inscripcion_hombre=inscripcion_hombre,
                inscripcion_mujer=inscripcion_mujer,
                id_pieza_detalle=id_pieza_detalle,
                # id_detalle_item=detalle_item.id_detalle_item
            )
            if infoDetalle:
                infoDetalle.save()
                producto = item.descripcion
                principal = True
                postergada = False
                id_transaccion = infoOrden.id_orden
                tipo_transaccion = 2
                tipo_notificacion = 2
                NotificacionOrdenes.delay(
                    request.user.id,
                    infoOrden.tienda.id_tienda,
                    infoOrden.taller_id,
                    producto,
                    principal,
                    postergada,
                    id_transaccion,
                    tipo_transaccion,
                    infoOrden.estado_id,
                    tipo_notificacion,
                )

                if longitud_piedras > 0:
                    piedras = json.loads(piedras_lista[0])
                    

                    if piedras:
                        for piedra in piedras:
                            prct_utilidad_ope = Piedras.objects.filter(id_piedra=piedra['id_piedra']).values('prct_utilidad_op').first()
                            utilidad_operaciones = int(prct_utilidad_ope.get('prct_utilidad_op'))
                            cantidad_piedra = piedra['cantidad']
                            costo_taller = piedra['costo']
                            precio_taller = piedra['precio_ta']
                            prct_utilidad_operaciones = utilidad_operaciones
                            precio_operaciones = (float(precio_taller) * (1+(utilidad_operaciones/100)))
                            precio_operaciones = round(precio_operaciones, 2)
                            subtotal_taller = round((cantidad_piedra * float(precio_taller)), 2)
                            subtotal_operaciones = round((cantidad_piedra * float(precio_operaciones)), 2)

                            infoPiedraOrden = OrdenesPiedras(
                                cantidad_piedras = cantidad_piedra,
                                costo_piedra_taller=costo_taller,
                                precio_piedra_taller=precio_taller,
                                prct_utilidad_piedra_op=prct_utilidad_operaciones,
                                precio_piedra_op = precio_operaciones,
                                subtotal_piedras_taller = subtotal_taller,
                                subtotal_piedras_op= subtotal_operaciones,
                                orden_id=int(infoOrden.id_orden),
                                piedra_id=int(piedra['id_piedra']),
                                piedra_detalle_id=int(piedra['id_detalle']),
                                diseño=piedra['design']
                            )
                            if infoPiedraOrden:
                                infoPiedraOrden.save()

            enviarCorreoCliente.delay(infoOrden.id_orden)
            enviarSms.delay(infoOrden.id_orden, 1)

            mensaje_telegram = "Se ha generado una Orden de trabajo con la secuencia {}, y solicitada por la tienda '{}'.".format(infoOrden.secuencia, infoOrden.tienda)
            taller_id = Talleres.objects.filter(id_taller=infoOrden.taller_id).values('id_taller')
            usuario_t = UsuariosTalleres.objects.filter(taller_id__in=taller_id)
            lista_usuario_telegram = []
            for usuario in usuario_t:
                lista_usuario_telegram.append(usuario.usuario.usuario_telegram)
            enviarTelegram.delay(lista_usuario_telegram, mensaje_telegram)

            return HttpResponse(infoOrden.id_orden)

    return render(request, template_name, contexto)


# reporte de solicitudes de trabajo


def ReporteSolicitudListaExcel(request, f_inicio, f_fin, opcion):
    ahora = datetime.now(timezone.utc)
    dia_uno_mes_actual = ahora.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    dia_uno_mes_anterior = dia_uno_mes_actual - timedelta(days=1)
    dia_uno_mes_anterior = dia_uno_mes_anterior.replace(
        day=1,
        hour=0,
        minute=0,
        second=0
        )
    f_inicio = datetime.strptime(f_inicio, '%Y-%m-%d').date()
    f_fin = datetime.strptime(f_fin, '%Y-%m-%d').date()

    # operaciones
    tiendas_id = UsuariosTiendas.objects.filter(usuario_id=request.user.id).values('tienda_id')
    if request.user.tipo_usuario.descripcion == "USUARIO OPERACIONES":
        if opcion == 1:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_actual,
                        fecha_creacion__lte=ahora
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=dia_uno_mes_actual,
                            fecha_creacion__lte=ahora
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 2:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                        tienda__zona__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=dia_uno_mes_anterior,
                        fecha_creacion__lte=dia_uno_mes_actual
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=dia_uno_mes_anterior,
                            fecha_creacion__lte=dia_uno_mes_actual
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 3:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial()
                    ).order_by('estado__orden', '-fecha_modificacion')[:100]
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:100]
        if opcion == 4:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                    tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')[:1000]
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by(
                            'estado__orden',
                            '-fecha_modificacion')[:1000]
        if opcion == 5:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                        fecha_creacion__gte=f_inicio,
                        fecha_creacion__lte=f_fin + timedelta(days=1)
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                            fecha_creacion__gte=f_inicio,
                            fecha_creacion__lte=f_fin + timedelta(days=1)
                        ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 6:
            if request.user.rol.descripcion == 'ADMIN OPERACIONES':
                ordenes = SolicitudTrabajo.objects.\
                    filter(
                        tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
                    ).order_by('estado__orden', '-fecha_modificacion')
            else:
                if request.user.rol.zonal:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda__zona_id=request.user.zona
                        ).order_by('estado__orden', '-fecha_modificacion')
                else:
                    ordenes = SolicitudTrabajo.objects.\
                        filter(
                            tienda_id__in=tiendas_id,
                        ).order_by('estado__orden', '-fecha_modificacion')
        # if request.user.rol.descripcion == 'ADMIN OPERACIONES':
        #     solicitudes = SolicitudTrabajo.objects.filter(
        #         tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
        #         estado__descripcion='ESPERA COTIZACION TALLER'
        #     ) | SolicitudTrabajo.objects.filter(
        #         tienda__sociedad__grupo_empresarial=request.user.grupo_empresarial(),
        #         estado__descripcion='ESPERA DE EVALUACION'
        #     )
        # else:
        #     if request.user.rol.zonal:
        #         solicitudes = SolicitudTrabajo.objects.filter(
        #             tienda__zona_id=request.user.zona,
        #             estado__descripcion='ESPERA COTIZACION TALLER'
        #         ) | SolicitudTrabajo.objects.filter(
        #             tienda__zona_id=request.user.zona,
        #             estado__descripcion='ESPERA DE EVALUACION'
        #         )
        #     else:
        #         solicitudes = SolicitudTrabajo.objects.filter(
        #             tienda_id__in=tiendas_id,
        #             estado__descripcion='ESPERA COTIZACION TALLER'
        #         ) | SolicitudTrabajo.objects.filter(
        #             tienda_id__in=tiendas_id,
        #             estado__descripcion='ESPERA DE EVALUACION'
        #         )
        # if solicitudes:
        #     solicitudes = solicitudes.\
        #         order_by('estado__orden', '-fecha_modificacion')


    # taller
    else:
        if opcion == 1:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=dia_uno_mes_actual,
                    fecha_creacion__lte=ahora
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 2:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=dia_uno_mes_anterior,
                    fecha_creacion__lte=dia_uno_mes_actual
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 3:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')[:100]
        if opcion == 4:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')[:1000]
        if opcion == 5:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller(),
                    fecha_creacion__gte=f_inicio,
                    fecha_creacion__lte=f_fin + timedelta(days=1)
                ).order_by('estado__orden', '-fecha_modificacion')
        if opcion == 6:
            ordenes = SolicitudTrabajo.objects.\
                filter(
                    taller=request.user.taller()
                ).order_by('estado__orden', '-fecha_modificacion')
    if ordenes:
        ordenes_resource = SolicitudListaResource()

        dataset = ordenes_resource.export(ordenes)
        nombre_archivo = 'Reporte_solicitud_' + ahora.strftime('%d-%m-%Y') + '.xls'
        response = HttpResponse(
            dataset.xls,
            content_type='application/vnd.ms-excel'
            )
        response['Content-Disposition'] = 'attachment; filename=' \
            + nombre_archivo
    else:
        response = HttpResponse('No existen ordenes')
    return response