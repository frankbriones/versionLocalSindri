from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404

from django.views import generic
from django.urls import reverse_lazy
import json
import pytz
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ConfigGeneral, ConfigUtilidadProveedor,\
    ConfigUtilidadTaller, OperacionesTallerVista, ZonasTallerVista,\
    SectoresTallerVista, OperacionesProveedorVista, ZonasProveedorVista,\
    ConfiguracionApiSMS, ConfiguracionSistema, ConfiguracionReporteUsuarios,\
    PoliticasComerciales

from .forms import CfgOpeForm, CfgTalForm, CfgPaisForm, RubrosForm
from usr.models import Usuarios, UsuariosGruposEmpresariales, UsuariosTalleres, Roles
from ubc.models import Paises
from ctg.models import EstandarTallas, Items, Piedras, Adicionales, \
    TiposPrecios
from trn.models import RubrosAsociados, OrigenMaterial, OrdenTrabajo, \
    SolicitudTrabajo, ConfiguracionRechazoSolicitudOrdenes
from bases.models import Estados
from est.models import Zonas, Sectores, Talleres, GruposEmpresariales, Sociedades
from trn.tasks import enviarCorreo
from .tasks import CrearTareaEnvioReporte
from trn.models import SolicitudRubros

from trn.forms import ObservacionForm

from bases.views import SinPermisos




@login_required(login_url='/login/')
@permission_required('cfg.view_politicascomerciales',
                     login_url='bases:sin_permisos')
def EditarPoliticasComerciales(request, id_empresa=None):
    template_name = "cfg/configuracion_politicas.html"
    contexto = {}

    politicas = PoliticasComerciales.objects.filter(
        empresa_id=id_empresa
    ).first()

    if request.method == 'GET':
        contexto = {
            'politicas': politicas
            }

    if request.method == 'POST':
        body = json.loads(request.body)
        texto_politicas = body['texto_politicas']
        if not politicas:
            info_politica = PoliticasComerciales(
                usuario_crea=request.user.id,
                descripcion=texto_politicas,
                empresa=request.user.grupo_empresarial(),
                ordenamiento=1
            )
            if info_politica:
                info_politica.save()
        else:
            politicas.descripcion = texto_politicas
            politicas.save()

    return render(request, template_name, contexto)



'''editar configuracion general país'''


class CfgPaisEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ubc.change_paises"
    model = Paises
    template_name = "cfg/cfg_pais_form.html"
    context_object_name = "obj"
    form_class = CfgPaisForm
    success_url = reverse_lazy("bases:home")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        aut_externo = form.instance.aut_externo
        if not aut_externo:
            usuarios = Usuarios.\
                objects.filter(pais_id=self.request.user.pais_id)
            for usuario in usuarios:
                usuario.aut_externo = False
                usuario.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CfgPaisEditarView, self).get_context_data(**kwargs)
        context['zonas_horarias'] = pytz.common_timezones
        return context


'''editar configuracion general operaciones'''


class CfgEmpresaEditarView(SinPermisos, generic.UpdateView):
    permission_required = "cfg.change_configgeneral"
    model = GruposEmpresariales
    template_name = "cfg/cfg_op_form.html"
    form_class = CfgOpeForm
    success_url = reverse_lazy("bases:home")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        form.instance.configurado = True
        costo = form.instance.costo_gramo_base
        precio = form.instance.precio_gramo_base
        # las sociedades que pertencen a este grupo empresarial
        sociedades_obj = Sociedades.objects.\
            filter(
                grupo_empresarial=self.request.user.grupo_empresarial()
            )
        '''actualizar el costo y precio de las sociedades,
         de acuerdo a la cfg general del grupo empresarial'''

        for sociedad in sociedades_obj:
            sociedad.costo_gramo_base = costo
            sociedad.precio_gramo_base = precio
            sociedad.save()
        self.object = form.save()

        # crear los campos en el modelo para las notas de ayuda
        # grupo_campos =  GruposEmpresariales.objects.filter(id_grupo_empresarial=self.request.user.grupo_empresarial().id_grupo_empresarial).values('anticipo_fabricacion', 'comprobante_env', 'factura_taller', 'cta_por_pagar', 'orden_compra', 'origen_material')
        # print(grupo_campos)
        # lista_tool = []
        # for key, value in grupo_campos[0].items():

        #     if key == 'origen_material':
        #         if value > 0 :
        #             value = True
        #     print(value)
        #     tooltip_config = {
        #         'texto':key,
        #         'estado': value,
        #         'title' : ''
        #     }
        #     # lista_tool.append(tooltip_config)
        #     tooltip = 
        
        


        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return form.errors

    def get_context_data(self, **kwargs):
        context = super(CfgEmpresaEditarView, self).get_context_data(**kwargs)
        context['obj'] = self.object
        context['origenes'] = OrigenMaterial.objects.all()
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        peso_max_arc = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_ARCHIVO').first()
        ext_perm_arc = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        context['peso_max_arc'] = peso_max_arc
        context['ext_perm_arc'] = ext_perm_arc
        context['tiposprecios'] = TiposPrecios.objects.all()
        return context


@login_required(login_url='/login/')
@permission_required('cfg.change_configgeneral',
                     login_url='bases:sin_permisos')
def CalculadoraPorcentajesView(request, pk=None):
    template_name = "cfg/cal_porcentajes_modal.html"
    form_registro = {}
    contexto = {}
    configuracion = ConfigGeneral.objects.filter(id=pk).first()

    if request.method == 'GET':

        contexto = {
            'configuracion': configuracion,
            }

    if request.method == 'POST':
        json_data = json.loads(request.body)
        precio_gramo_base = json_data['precio_gramo_base']
        # utilidad_sobre_base = json_data['utilidad_sobre_base']
        utilidad_sobre_taller = json_data['utilidad_sobre_taller']
        prct_impuestos = json_data['prct_impuestos']
        precio_gramo_final = json_data['precio_gramo_final']

        configuracion.precio_gramo_base = precio_gramo_base
        # configuracion.utilidad_sobre_base = utilidad_sobre_base
        configuracion.utilidad_sobre_taller = utilidad_sobre_taller
        configuracion.prct_impuestos = prct_impuestos
        configuracion.precio_gramo_final = precio_gramo_final
        configuracion.save()

    return render(request, template_name, contexto)


'''editar configuracion general taller '''


class CfgTalEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_talleres"
    model = Talleres
    template_name = "cfg/cfg_ta_form.html"
    context_object_name = "obj"
    form_class = CfgTalForm
    success_url = reverse_lazy("bases:home")
    login_url = "bases:login"

    def form_valid(self, form):
        # items = Items.objects.\
        #     filter(taller=self.request.user.taller,
        #            tipo_catalogo_id=2)
        # for item in items:
        #     item.escala_peso = form.instance.escala_peso
        #     item.valor_fraccion = form.instance.valor_fraccion
        #     item.save()
        # piedras = Piedras.objects.\
        #     filter(taller=self.request.user.taller)
        # for piedra in piedras:
        #     piedra.utilidad_sobre_piedras = \
        #         form.instance.utilidad_sobre_piedras
        #     piedra.save()
        # adicionales = Adicionales.objects.\
        #     filter(taller=self.request.user.taller)
        # for adicional in adicionales:
        #     adicional.utilidad_sobre_adicionales = \
        #         form.instance.utilidad_sobre_adicionales
        #     adicional.save()
        form.instance.usuario_modifica = 1
        form.instance.configurado = True
        secuencia_ordenes = form.instance.secuencia_ordenes
        secuencia_solicitudes = form.instance.secuencia_solicitudes
        ultima_orden = OrdenTrabajo.objects.\
            filter(taller_id=self.request.user.taller()).\
            order_by('-fecha_creacion').first()
        if ultima_orden:
            sec_orden_actual = int(ultima_orden.secuencia[-5:])
        else:
            sec_orden_actual = 0
        ultima_solicitud = SolicitudTrabajo.objects.\
            filter(taller_id=self.request.user.taller()).\
            order_by('-fecha_creacion').first()
        if ultima_solicitud:
            sec_solicitud_actual = int(ultima_solicitud.secuencia[-5:])
        else:
            sec_solicitud_actual = 0
        if secuencia_ordenes < sec_orden_actual:
            return render(self.request,
                          "cfg/cfg_ta_form.html",
                          {
                              'mensaje': 'secuencia-ordenes',
                              'estandar_tallas': EstandarTallas.objects.all(),
                              'form': form}
                          )
        if secuencia_solicitudes < sec_solicitud_actual:
            return render(self.request,
                          "cfg/cfg_ta_form.html",
                          {
                              'mensaje': 'secuencia-solicitudes',
                              'estandar_tallas': EstandarTallas.objects.all(),
                              'form': form}
                          )
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(CfgTalEditarView, self).get_context_data(**kwargs)
        context['estandar_tallas'] = EstandarTallas.objects.all()
        context['tiposprecios'] = TiposPrecios.objects.all()
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        peso_max_arc = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_ARCHIVO').first()
        ext_perm_arc = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_ARCHIVO').first()
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        context['peso_max_arc'] = peso_max_arc
        context['ext_perm_arc'] = ext_perm_arc
        return context


'''utilidad joyeria-taller '''
@login_required(login_url='/login/')
@permission_required('cfg.change_configutilidadtaller',
                     login_url='bases:sin_permisos')
def CfgOperacionesTaller(request, usuario_id=None):
    template_name = "cfg/cfg_ope_tal_form.html"
    form_registro = {}
    contexto = {}

    if request.method == 'GET':
        ope_talleres = OperacionesTallerVista.objects.\
            filter(pais_id=request.user.pais_id)
        zonas_talleres = ZonasTallerVista.objects.\
            filter(pais_id=request.user.pais_id)
        sectores_talleres = SectoresTallerVista.objects.\
            filter(pais_id=request.user.pais_id)
        cfg_utilidad = ConfigUtilidadTaller.objects.\
            filter(pais_id=request.user.pais_id)

        contexto = {
            'rel_usuarios': ope_talleres,
            'rel_zonas': zonas_talleres,
            'rel_sectores': sectores_talleres,
            'configuraciones': cfg_utilidad
            }

    if request.method == 'POST':

        pais_id = request.user.pais_id

        json_data = json.loads(request.body)
        id_item = json_data['id_item']
        nombre = json_data['nombre']
        id_taller = json_data['id_taller']
        taller = json_data['taller']
        tipo = json_data['tipo']
        utilidad = json_data['utilidad']

        if tipo == 1:
            configuracion = ConfigUtilidadTaller.objects.\
                filter(id_usuario_op=id_item, id_taller=id_taller).first()
            if configuracion:
                configuracion.utilidad = utilidad
                configuracion.usuario_modifica = request.user.id
                configuracion.save()
            else:
                infoCfg = ConfigUtilidadTaller(
                    id_usuario_op=id_item,
                    usuario_op=nombre,
                    id_taller=id_taller,
                    taller=taller,
                    utilidad=utilidad,
                    pais_id=pais_id,
                    usuario_crea=request.user.id
                )
                if infoCfg:
                    infoCfg.save()

        if tipo == 2:
            usuarios = Usuarios.objects.filter(zona_id=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    configuracion = ConfigUtilidadTaller.objects.\
                        filter(id_usuario_op=usuario.id, id_taller=id_taller).\
                        first()
                    if configuracion:
                        configuracion.utilidad = utilidad
                        configuracion.usuario_modifica = request.user.id
                        configuracion.save()
                    else:
                        infoCfg = ConfigUtilidadTaller(
                            id_usuario_op=usuario.id,
                            usuario_op=usuario.username,
                            id_taller=id_taller,
                            taller=taller,
                            utilidad=utilidad,
                            pais_id=pais_id,
                            usuario_crea=request.user.id
                        )
                        if infoCfg:
                            infoCfg.save()

        if tipo == 3:
            usuarios = Usuarios.objects.filter(sector_id=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    configuracion = ConfigUtilidadTaller.objects.\
                        filter(id_usuario_op=usuario.id, id_taller=id_taller).\
                        first()
                    if configuracion:
                        configuracion.utilidad = utilidad
                        configuracion.usuario_modifica = request.user.id
                        configuracion.save()
                    else:
                        infoCfg = ConfigUtilidadTaller(
                            id_usuario_op=usuario.id,
                            usuario_op=usuario.username,
                            id_taller=id_taller,
                            taller=taller,
                            utilidad=utilidad,
                            pais_id=pais_id,
                            usuario_crea=request.user.id
                        )
                        if infoCfg:
                            infoCfg.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('cfg.change_configutilidadproveedor',
                     login_url='bases:sin_permisos')
def CfgOperacionesProveedor(request, usuario_id=None):
    template_name = "cfg/cfg_ope_pro_form.html"
    form_registro = {}
    contexto = {}

    if request.method == 'GET':
        ope_proveedores = OperacionesProveedorVista.objects.\
            filter(pais_id=request.user.pais_id)
        zonas_proveedores = ZonasProveedorVista.objects.\
            filter(pais_id=request.user.pais_id)
        cfg_utilidad = ConfigUtilidadProveedor.objects.\
            filter(pais_id=request.user.pais_id)

        contexto = {
            'rel_usuarios': ope_proveedores,
            'rel_zonas': zonas_proveedores,
            'configuraciones': cfg_utilidad
            }

    if request.method == 'POST':

        pais_id = request.user.pais_id

        json_data = json.loads(request.body)
        id_item = json_data['id_item']
        nombre = json_data['nombre']
        id_proveedor = json_data['id_proveedor']
        prv_nombres = json_data['prv_nombres']
        prv_apellidos = json_data['prv_apellidos']
        tipo = json_data['tipo']
        utilidad = json_data['utilidad']

        if tipo == 1:
            configuracion = ConfigUtilidadProveedor.objects.\
                filter(id_usuario_op=id_item, proveedor_id=id_proveedor)\
                .first()
            if configuracion:
                configuracion.utilidad = utilidad
                configuracion.usuario_modifica = request.user.id
                configuracion.save()
            else:
                infoCfg = ConfigUtilidadProveedor(
                    id_usuario_op=id_item,
                    usuario_op=nombre,
                    proveedor_id=id_proveedor,
                    nombres=prv_nombres,
                    apellidos=prv_apellidos,
                    utilidad=utilidad,
                    pais_id=pais_id,
                    usuario_crea=request.user.id
                )
                if infoCfg:
                    infoCfg.save()

        if tipo == 2:
            usuarios = Usuarios.objects.filter(zona_id=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    configuracion = ConfigUtilidadProveedor.objects.\
                        filter(id_usuario_op=usuario.id,
                               proveedor_id=id_proveedor).first()
                    if configuracion:
                        configuracion.utilidad = utilidad
                        configuracion.usuario_modifica = request.user.id
                        configuracion.save()
                    else:
                        infoCfg = ConfigUtilidadProveedor(
                            id_usuario_op=usuario.id,
                            usuario_op=usuario.username,
                            proveedor_id=id_proveedor,
                            nombres=prv_nombres,
                            apellidos=prv_apellidos,
                            utilidad=utilidad,
                            pais_id=pais_id,
                            usuario_crea=request.user.id
                        )
                        if infoCfg:
                            infoCfg.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_usuarios',
                     login_url='bases:sin_permisos')
def CfgTiempoVenta(request):
    template_name = "cfg/cfg_tmp_lim_form.html"
    form_registro = {}
    contexto = {}

    if request.method == 'GET':
        usuarios_lista = Usuarios.objects.\
            filter(pais_id=request.user.pais_id,
                   tipo_usuario_id=3)
        zonas_lista = Zonas.objects.\
            filter(grupo_empresarial=request.user.grupo_empresarial(),
                   estado__descripcion='ACTIVO')
        sectores_lista = Sectores.objects.\
            filter(grupo_empresarial=request.user.grupo_empresarial(),
                   estado__descripcion='ACTIVO')

        contexto = {
            'rel_usuarios': usuarios_lista,
            'rel_zonas': zonas_lista,
            'rel_sectores': sectores_lista,
            }

    if request.method == 'POST':

        pais_id = request.user.pais_id

        json_data = json.loads(request.body)
        id_item = json_data['id_item']
        tipo = json_data['tipo']
        tmp_lim_vta = json_data['tmp_lim_vta']

        if tipo == 1:
            usuario_mod = Usuarios.objects.\
                filter(id=id_item).first()
            if usuario_mod:
                # usuario_mod.tmp_lim_vta = tmp_lim_vta
                usuario_mod.usuario_modifica = request.user.id
                usuario_mod.save()

        if tipo == 2:
            usuarios = Usuarios.objects.filter(zona=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    # usuario.tmp_lim_vta = tmp_lim_vta
                    usuario.usuario_modifica = request.user.id
                    usuario.save()

        if tipo == 3:
            usuarios = Usuarios.objects.filter(sector_id=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    # usuario.tmp_lim_vta = tmp_lim_vta
                    usuario.usuario_modifica = request.user.id
                    usuario.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_usuarios',
                     login_url='bases:sin_permisos')
def CfgPermitirExterno(request):
    template_name = "cfg/cfg_ext_form.html"
    form_registro = {}
    contexto = {}

    if request.method == 'GET':
        usuarios_lista = Usuarios.objects.\
            filter(pais_id=request.user.pais_id,
                   tipo_usuario_id=3)
        zonas_lista = Zonas.objects.\
            filter(grupo_empresarial=request.user.grupo_empresarial(),
                   estado_id=1)
        sectores_lista = Sectores.objects.\
            filter(grupo_empresarial=request.user.grupo_empresarial(),
                   estado_id=1)

        contexto = {
            'rel_usuarios': usuarios_lista,
            'rel_zonas': zonas_lista,
            'rel_sectores': sectores_lista,
            }

    if request.method == 'POST':

        pais_id = request.user.pais_id

        json_data = json.loads(request.body)
        id_item = json_data['id_item']
        tipo = json_data['tipo']
        aut_externo = json_data['aut_externo']
        # if aut_externo == 'on':
        #     aut_externo = True
        # else:
        #     aut_externo = False

        if tipo == 1:
            usuario_mod = Usuarios.objects.\
                filter(id=id_item).first()
            if usuario_mod:
                usuario_mod.grupo_empresarial().aut_externo = aut_externo
                usuario_mod.usuario_modifica = request.user.id
                usuario_mod.save()

        if tipo == 2:
            usuarios = Usuarios.objects.filter(zona=id_item,
                                               tipo_usuario_id=3)

            if usuarios:
                for usuario in usuarios:
                    usuario_mod.grupo_empresarial().aut_externo = aut_externo
                    usuario.usuario_modifica = request.user.id
                    usuario.save()

        if tipo == 3:
            usuarios = Usuarios.objects.filter(user_usuariostiendas__tienda_id__sector_id=id_item,
                                               tipo_usuario_id=3)
            if usuarios:
                for usuario in usuarios:
                    usuario.grupo_empresarial().aut_externo = aut_externo
                    usuario.usuario_modifica = request.user.id
                    usuario.save()

    return render(request, template_name, contexto)


# @login_required(login_url='/login/')
# @permission_required('cfg.change_configgeneral',
#                      login_url='bases:sin_permisos')
# def CfgMermaTalleres(request):
#     template_name = "cfg/cfg_merma.html"
#     form_registro = {}
#     contexto = {}

#     if request.method == 'GET':
#         talleres_lista = Taller.objects.\
#             filter(pais_id=request.user.pais_id)

#         contexto = {
#             'talleres_lista': talleres_lista
#             }

#     if request.method == 'POST':

#         pais_id = request.user.pais_id

#     return render(request, template_name, contexto)


# class CfgMermaEditarView(SinPermisos, generic.UpdateView):
#     permission_required = "cfg.change_configgeneral"
#     model = Taller
#     template_name = "cfg/cfg_modificar_merma_modal.html"
#     context_object_name = "obj"
#     form_class = CfgMermaForm
#     success_url = reverse_lazy("cfg:cfg_merma")
#     login_url = "bases:login"

#     def form_valid(self, form):
#         form.instance.usuario_modifica = self.request.user.id
#         return super().form_valid(form)


class RubrosListaView(SinPermisos, generic.ListView):
    permission_required = "trn.view_rubrosasociados"
    model = RubrosAsociados
    template_name = "cfg/rubros_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.rol.descripcion == 'ADMIN OPERACIONES':
            return RubrosAsociados.objects.\
                filter(
                    tipo_rubro=2
                )
        else:
             return RubrosAsociados.objects.\
                filter(
                    tipo_rubro=1
                )

@login_required(login_url='/login/')
@permission_required('trn.add_rubrosasociados',
                     login_url='bases:sin_permisos')
def RubrosFormView(request, pk=None):
    template_name = "cfg/rubro_form_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        rubro = RubrosAsociados.objects.filter(id_rubro=pk).first()
        form_item = RubrosForm()
        if rubro:
            form_item = RubrosForm({'descripcion': rubro.descripcion})

        contexto = {
            'form': form_item,
            'rubro': rubro
        }

    if request.method == 'POST':
        rubro = RubrosAsociados.objects.filter(id_rubro=pk).first()
        json_data = json.loads(request.body)
        descripcion = json_data['descripcion']
        if request.user.rol.descripcion == 'ADMIN OPERACIONES':
            tipo = 2
            grupo_id = request.user.grupo_empresarial().id_grupo_empresarial
            taller_id = None
        else:
            tipo = 1
            taller_id = request.user.taller().id_taller
            grupo_id = None

        if rubro:
            rubro.descripcion = descripcion
            rubro.tipo_rubro = tipo
            rubro.save()
        else:
            infoRubro = RubrosAsociados(
                descripcion=descripcion,
                usuario_crea=request.user.id,
                tipo_rubro = tipo,
                grupo_id = grupo_id,
                taller_id = taller_id
            )

            if infoRubro:
                try:
                    infoRubro.save()
                    return HttpResponse('ok')
                except IntegrityError as e:
                    return HttpResponse('duplicado')

        return redirect("cfg:cfg_rubros_lista")

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('trn.change_rubrosasociados',
                     login_url='bases:sin_permisos')
def ActualizarRubroModal(request, pk):
    template_name = 'cfg/actualizar_rubro_modal.html'
    contexto = {}
    rubro = RubrosAsociados.objects.filter(pk=pk).first()

    if not rubro:
        return HttpResponse('No existe el rubro ' + str(pk))

    if request.method == 'GET':
        contexto = {'rubro': rubro}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        rubro.estado = estado
        rubro.save()
        return HttpResponse('Rubro actualizado')

    return render(request, template_name, contexto)




@login_required(login_url='/login/')
#permisos
def eliminar_rubro(request):

    if request.is_ajax  and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        rubro = request.GET.get("rubro", None)

        if rubro:
            try:
                rubro_obj = RubrosAsociados.objects.filter(id_rubro=rubro).first()
                solicitud_rubro = SolicitudRubros.objects.filter(rubro_id=rubro_obj.id_rubro).exists()
                if solicitud_rubro:
                    estado=2
                else:
                    RubrosAsociados.objects.filter(id_rubro=rubro).delete()
                    estado = 1
            except RubrosAsociados.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})

    return JsonResponse({}, status=400)


@login_required(login_url='/login/')
# @permission_required('cfg.env_reportes',
#                      login_url='bases:sin_permisos')
def EnvioReportesView(request, id_usuario=None):
    template_name = "cfg/cfg_envio_reportes.html"
    form_registro = {}
    contexto = {}

    if request.method == 'GET':
        dia = 1
        hora = 0
        usuarios_registrados = []
        nombre_tarea = 'envio_reporte_' + str(request.user.id) + \
            '_' + str(request.user.pais_id)
        tarea = PeriodicTask.objects.filter(
            name=nombre_tarea
        ).first()
        if tarea:
            dia = tarea.crontab.day_of_month
            hora = tarea.crontab.hour
            args = json.loads(tarea.kwargs)
            correos = json.loads(args.get('correos', None))
            for correo in correos:
                usuario = Usuarios.objects.\
                    filter(email=correo).first()
                if usuario:
                    usuarios_registrados.append(str(usuario.id))
            usuarios_registrados = json.dumps(usuarios_registrados)
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').\
            first()
        if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            usuarios_id = UsuariosGruposEmpresariales.objects.filter(usuario__pais=request.user.pais).values('usuario_id')
            usuarios = Usuarios.objects.\
                filter(
                    id__in=usuarios_id
                    )
        else:
            usuarios_id = UsuariosTalleres.objects.filter(usuario__pais=request.user.pais).values('usuario_id')
            usuarios = Usuarios.objects.\
                filter(id__in=usuarios_id)
        # print(usuarios_registrados)
        contexto = {
            'usuarios': usuarios,
            'usuarios_registrados': usuarios_registrados,
            'dia': dia,
            'hora': hora
        }

    if request.method == 'POST':
        usuarios_lista = request.POST.getlist('usuarios[]')
        usuarios_lista = json.loads(usuarios_lista[0])
        dia = request.POST['dia']
        hora = request.POST['hora']
        correos = []
        for usuario in usuarios_lista:
            user = Usuarios.objects.filter(id=int(usuario)).first()
            correos.append(user.email)
        correos = json.dumps(correos)
        usuario = request.user.username
        lista_correos = {'correos': correos, 'usuario': usuario}
        lista_correos = json.dumps(lista_correos)

        zona_horaria = request.user.pais.zona_horaria
        nombre_tarea = 'envio_reporte_' + str(request.user.id) + \
            '_' + str(request.user.pais_id)

        periodo, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour=hora,
            day_of_week='*',
            day_of_month=dia,
            month_of_year='*',
            timezone=zona_horaria
        )

        tarea = PeriodicTask.objects.filter(
            name=nombre_tarea
        ).first()

        if tarea:
            tarea.crontab = periodo
            tarea.kwargs = lista_correos
            tarea.save()
        else:
            PeriodicTask.objects.create(
                crontab=periodo,
                name=nombre_tarea,
                task='trn.tasks.enviarReporte',
                kwargs=lista_correos
            )

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('cfg.change_configuracionapisms',
#                      login_url='bases:sin_permisos')
def EnvioReporteUsuario(request):
    template_name="cfg/cfg_reporte_usuarios.html"
    contexto = {}
    if request.method == 'GET':
        if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            roles = Roles.objects.filter(grupo_id=request.user.grupo_empresarial().id_grupo_empresarial)
        # else:
        #     roles = Roles.objects.filter(taller_id=request.user.taller().id_taller)

        roles_asignados = []
        for cfg_reporte in roles:
            roles_asignados.append(str(cfg_reporte.id_rol))
        roles_asignados = json.dumps(roles_asignados)
        

        roles_ususario = Roles.objects.filter(grupo_id=request.user.grupo_empresarial().id_grupo_empresarial)
        contexto = {
            'roles_asignados': roles_asignados,
            'roles': roles_ususario
        }
    if request.method == 'POST':
        roles_lista = request.POST.getlist('roles[]')
        if len(roles_lista) != 0:
            roles_lista = json.loads(roles_lista[0])
        if roles_lista:
            usuario_reportes = ConfiguracionReporteUsuarios.objects.filter(grupo_empresarial_id=request.user.grupo_empresarial().id_grupo_empresarial)
            for rol_reporte in usuario_reportes:
                rol_reporte.delete()
            for rol in roles_lista:
                if rol:
                    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
                        reporte_usuario = ConfiguracionReporteUsuarios(
                            rol_id=rol,
                            usuario_crea=request.user.id,
                            grupo_empresarial_id=request.user.grupo_empresarial().id_grupo_empresarial
                        )
                    # else:
                    #     reporte_usuario = ConfiguracionReporteUsuarios(
                    #         rol_id=rol,
                    #         usuario_crea=request.user.id,
                    #         taller_id=request.user.taller().id_taller
                    #     )
                    reporte_usuario.save()
        else:
            return HttpResponseRedirect('/')
        

    return render(request, template_name, contexto)





@login_required(login_url='/login/')
@permission_required('cfg.change_configuracionapisms',
                     login_url='bases:sin_permisos')
def CfgApiMensajes(request, pk):
    template_name = "cfg/cfg_api_sms.html"
    contexto = {}
    URL_TOKEN = ConfiguracionApiSMS.objects.\
        filter(
            clave='URL_TOKEN',
            pais_id=pk
            ).first()
    client_id = ConfiguracionApiSMS.objects.\
        filter(
            clave='client_id',
            pais_id=pk
            ).first()
    client_secret = ConfiguracionApiSMS.objects.\
        filter(
            clave='client_secret',
            pais_id=pk
            ).first()
    URL_ENVIO_LISTA = ConfiguracionApiSMS.objects.\
        filter(
            clave='URL_ENVIO_LISTA',
            pais_id=pk
            ).first()
    CONTENIDO_SMS = ConfiguracionApiSMS.objects.\
        filter(
            clave='CONTENIDO_SMS',
            pais_id=pk
            ).first()

    if request.method == 'GET':

        contexto = {
            'URL_TOKEN': URL_TOKEN,
            'client_id': client_id,
            'client_secret': client_secret,
            'URL_ENVIO_LISTA': URL_ENVIO_LISTA,
            'CONTENIDO_SMS': CONTENIDO_SMS,
            }

    if request.method == 'POST':
        json_data = json.loads(request.body)
        txt_URL_TOKEN = json_data['URL_TOKEN']
        txt_client_id = json_data['client_id']
        txt_client_secret = json_data['client_secret']
        txt_URL_ENVIO_LISTA = json_data['URL_ENVIO_LISTA']
        txt_CONTENIDO_SMS = json_data['CONTENIDO_SMS']

        URL_TOKEN.valor = txt_URL_TOKEN
        client_id.valor = txt_client_id
        client_secret.valor = txt_client_secret
        URL_ENVIO_LISTA.valor = txt_URL_ENVIO_LISTA
        CONTENIDO_SMS.valor = txt_CONTENIDO_SMS

        URL_TOKEN.save()
        client_id.save()
        client_secret.save()
        URL_ENVIO_LISTA.save()
        CONTENIDO_SMS.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('est.env_reportes',
#                      login_url='bases:sin_permisos')
def PrioridadTalleresView(request, id_usuario=None):
    template_name = "cfg/prioridad_talleres.html"
    contexto = {}

    if request.user == 'AnonymousUser':
        return HttpResponseRedirect('/')
    else:
        talleres = Talleres.objects.\
            filter(pais=request.user.pais).\
            order_by('prioridad')


    if request.method == 'GET':
        contexto = {
            'talleres': talleres
            }

    if request.method == 'POST':
        talleres_orden = request.POST.getlist('talleresOrden[]')
        talleres_orden = json.loads(talleres_orden[0])
        # print(talleres_orden)
        for item in talleres_orden:
            # print(item.get('id'))
            taller = Talleres.objects.filter(id_taller=item.get('id')).first()
            taller.prioridad = item.get('orden')
            taller.save()

    return render(request, template_name, contexto)





# @login_required(login_url='/login/')
class ObservacionesListaView(LoginRequiredMixin, generic.ListView):
    # permission_required = "est.view_zonas"
    model = ConfiguracionRechazoSolicitudOrdenes
    template_name = "cfg/observaciones_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            return ConfiguracionRechazoSolicitudOrdenes.objects.filter(grupo_empresarial=self.request.user.grupo_empresarial())
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            return ConfiguracionRechazoSolicitudOrdenes.objects.filter(taller=self.request.user.taller())




class ObservacionesCrearView(LoginRequiredMixin, generic.CreateView):
    # permission_required = "est.add_zonas"
    model = ConfiguracionRechazoSolicitudOrdenes
    template_name = "cfg/obs_form.html"
    context_object_name = "obj"
    form_class = ObservacionForm
    success_url = reverse_lazy("cfg:obs_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            form.instance.grupo_empresarial_id = self.request.user.grupo_empresarial().id_grupo_empresarial
            form.instance.pais = self.request.user.pais
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            form.instance.taller_id = self.request.user.taller().id_taller
            form.instance.pais = self.request.user.pais
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return form.errors

    def get_form_kwargs(self):
        kwargs = super(ObservacionesCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs




class ObservacionesEditarView(LoginRequiredMixin, generic.UpdateView):
    # permission_required = "trn.change_configuracionrechazosolicitudordenes"
    model = ConfiguracionRechazoSolicitudOrdenes
    template_name = "cfg/obs_form.html"
    context_object_name = "obj"
    form_class = ObservacionForm
    success_url = reverse_lazy("cfg:obs_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ObservacionesEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



@login_required(login_url='/login/')
def eliminar_observacion(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        obs = request.GET.get("obs_id", None)

        if obs:
            try:
                obs_obj = ConfiguracionRechazoSolicitudOrdenes.objects.filter(id_obs_rechazo=obs).first()
                sol_observacion = SolicitudTrabajo.objects.filter(rechazo_id=obs).exists()
                orden_observacion = OrdenTrabajo.objects.filter(rechazo_id=obs).exists()
                if sol_observacion or orden_observacion:
                    estado = 2 
                else:
                    ConfiguracionRechazoSolicitudOrdenes.objects.filter(id_obs_rechazo=obs).delete()
                    estado = 1
            except ConfiguracionRechazoSolicitudOrdenes.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)


''' actualizar el estado de los motivos de rechazo'''
# @permission_required('ctg.change_acabados',
#                      login_url='bases:sin_permisos')
@login_required(login_url='/login/')
def ActualizarMotivoRechazo(request, pk):
    template_name = 'cfg/actualizar_rechazo_modal.html'
    contexto = {}
    rechazo = ConfiguracionRechazoSolicitudOrdenes.objects.filter(pk=pk).first()

    if request.method == 'GET':
        contexto = {'rechazo': rechazo}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'None':
            estado = 'INACTIVO'
        if estado == 'ACTIVO' :
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        rechazo.estado = estado
        rechazo.save()
        return HttpResponse('Rechazo actualizada')
    return render(request, template_name, contexto)

