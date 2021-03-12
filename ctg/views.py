from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.db import IntegrityError
from datetime import datetime, timezone, timedelta



from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Categorias, Colores, Adicionales, Items, \
    DetalleItems, ItemsColores, Tallas, TiposCatalogo, Piedras, \
    CategoriaPiedras, CategoriaAdicionales, DetallePiedras, \
    UnidadesMedida, ConteoCotizaciones, Divisiones, PreciosDefinidos, \
    TiposPrecios, ItemsImagenes, Acabados, PartesInternas, \
    Anchuras, Piezas, PiezasDetalles, PiezasAcabados, \
    PiezasPiedras

from .forms import CategoriaForm, ColoresForm, AdicionalesForm,\
    ItemsForm, DetallesForm, TallasForm, PiedrasForm, DetallesPiedraForm, \
    DivisionForm, PreciosDefinidosForm, AcabadosForm, PartesInternasForm, \
    AnchurasForm

from .serializers import DetallesSerializer, DetallePiedraSerializer, \
    ItemsSerializer, CategoriasSerializer, DivisionesSerializer, \
    ItemsListaSerializer, PiedrasSerializer, DetallesPiedraSerializer, \
    AnchurasSerializer, PiezasDetallesSerializer, PiezasPiedrasSerializer,\
    PiezasDetallesPesosSerializer, PiezasPiedrasItemSerializer

from usr.models import Usuarios
from ubc.models import Paises
from est.models import Zonas, Sectores, GruposEmpresariales, Talleres
from bases.models import Estados
from cfg.models import ConfiguracionSistema, ConfigGeneral
from prv.models import Proveedores
from trn.models import SolicitudTrabajo, SolicitudesPiedras, DetalleOrden, DetalleSolicitud, OrdenesPiedras

from bases.views import SinPermisos





class PreciosDefinidosListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_preciosdefinidos"
    model = PreciosDefinidos
    template_name = "ctg/precios_definidos_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            return PreciosDefinidos.objects.\
                filter(taller=self.request.user.taller())
        else:
            if self.request.user.\
                    tipo_usuario.descripcion == 'USUARIO OPERACIONES':
                return PreciosDefinidos.objects.\
                    filter(grupo_empresarial_id=self.request.user.grupo_empresarial().id_grupo_empresarial)


class PreciosCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_preciosdefinidos"
    model = PreciosDefinidos
    template_name = "ctg/precios_definidos_form.html"
    context_object_name = "obj"
    form_class = PreciosDefinidosForm
    success_url = reverse_lazy("ctg:precios_definidos_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_neutro = Talleres.objects.\
            filter(nombre='NEUTRO').first()

        grupo_empresarial_neutro = GruposEmpresariales.objects.filter(estado__descripcion='ACTIVO',
            pais_id=self.request.user.pais_id).first()

        form.instance.usuario_crea = self.request.user.id

        taller_obj = self.request.user.taller()
        grupo_obj = self.request.user.grupo_empresarial()
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':

            form.instance.taller_id = taller_obj.id_taller
            form.instance.grupo_empresarial_id = grupo_empresarial_neutro.id_grupo_empresarial

        elif self.request.user.tipo_usuario.\
                descripcion == 'USUARIO OPERACIONES':
            form.instance.taller_id = taller_neutro.id_taller
            form.instance.grupo_empresarial_id = grupo_obj.id_grupo_empresarial
            # form.instance.prct_utilidad = 0
            # form.instance.costo = 0

        try:
            return super().form_valid(form)
        except IntegrityError as e:
            return render(self.request,
                          "ctg/precios_definidos_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})

    
    def form_invalid(self, form):
        print(form.errors)
        return form.errors

    def get_context_data(self, **kwargs):
        context = super(PreciosCrearView, self).get_context_data(**kwargs)
        context['tipos'] = TiposPrecios.objects.all()
        return context


class PreciosEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_preciosdefinidos"
    model = PreciosDefinidos
    template_name = "ctg/precios_definidos_form.html"
    form_class = PreciosDefinidosForm
    success_url = reverse_lazy("ctg:precios_definidos_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        costo = form.instance.costo
        prct_utilidad = form.instance.prct_utilidad
        precio = form.instance.precio
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            categorias = Categorias.objects.\
                filter(precio_taller_id=self.object.id_precio)
            if categorias:
                for categoria in categorias:
                    categoria.costo_taller = costo
                    categoria.prct_utilidad_taller = prct_utilidad
                    categoria.precio_taller = precio
                    categoria.save()
            items = Items.objects.\
                filter(categoria__precio_taller_id=self.object.id_precio)
            if items:
                for item in items:
                    item.costo_taller = costo
                    item.prct_utilidad_taller = prct_utilidad
                    item.precio_taller = precio
                    item.save()
        elif self.request.user.tipo_usuario.\
                descripcion == 'USUARIO OPERACIONES':
            categorias = Categorias.objects.\
                filter(precio_empresa_id=self.object.id_precio)
            if categorias:
                for categoria in categorias:
                    categoria.prct_utilidad_empresa = prct_utilidad
                    categoria.precio_empresa = precio
                    categoria.save()
            items = Items.objects.\
                filter(categoria__precio_empresa_id=self.object.id_precio)
            if items:
                for item in items:
                    item.prct_utilidad_empresa = prct_utilidad
                    item.precio_empresa = precio
                    item.save()
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/precios_definidos_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})
    

    def form_invalid(self, form):
        print(form.errors)
        return form.errors

    def get_context_data(self, **kwargs):
        context = super(PreciosEditarView, self).get_context_data(**kwargs)
        context['tipos'] = TiposPrecios.objects.all()
        context['talleres'] = Talleres.objects.all()
        context['grupos'] = GruposEmpresariales.objects.all()
        context['obj'] = self.object
        return context


@login_required(login_url='/login/')
@permission_required('ctg.change_preciosdefinidos',
                     login_url='bases:sin_permisos')
def ActualizarPrecioModal(request, pk):
    template_name = 'ctg/actualizar_precio_modal.html'
    contexto = {}
    precio = PreciosDefinidos.objects.filter(pk=pk).first()

    if not precio:
        return HttpResponse('No existe el precio ' + str(pk))

    if request.method == 'GET':
        contexto = {'precio': precio}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        precio.estado = estado
        precio.save()
        return HttpResponse('Precio actualizado')

    return render(request, template_name, contexto)



#eliminar precio definido si no contiene una relacion con categorias
@login_required(login_url='/login/')
#permisos
def eliminar_precio(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        precio = request.GET.get('precio', None)
        if precio:
            try:
                precio_obj = PreciosDefinidos.objects.filter(id_precio=precio).first()
                categoria_precio_ta = Categorias.objects.filter(precio_taller_id=precio_obj.id_precio).exists()
                categoria_precio_op = Categorias.objects.filter(precio_empresa_id=precio_obj.id_precio).exists()
                if categoria_precio_ta or categoria_precio_op:
                    estado = 2
                else:
                    PreciosDefinidos.objects.filter(id_precio=precio).delete()
                    estado = 1
            except PreciosDefinidos.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)
                
            


class DivisionesListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_divisiones"
    model = Divisiones
    template_name = "ctg/divisiones_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return Divisiones.objects.filter(taller_id=self.request.user.taller())


class DivisionesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_divisiones"
    model = Divisiones
    template_name = "ctg/divisiones_form.html"
    context_object_name = "obj"
    form_class = DivisionForm
    success_url = reverse_lazy("ctg:divisiones_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/divisiones_form.html",
                          {'mensaje': e.__cause__,
                           'tipos': TiposCatalogo.objects.all(),
                           'form': form})

    def get_context_data(self, **kwargs):
        context = super(DivisionesCrearView, self).get_context_data(**kwargs)
        context['tipos'] = TiposCatalogo.objects.all()
        return context


class DivisionesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_divisiones"
    model = Divisiones
    template_name = "ctg/divisiones_form.html"
    form_class = DivisionForm
    success_url = reverse_lazy("ctg:divisiones_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_modifica = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/divisiones_form.html",
                          {'mensaje': e.__cause__,
                           'tipos': TiposCatalogo.objects.all(),
                           'form': form})

    def get_context_data(self, **kwargs):
        context = super(DivisionesEditarView, self).get_context_data(**kwargs)
        context['tipos'] = TiposCatalogo.objects.all()
        id_division = self.kwargs['pk']
        context['obj'] = Divisiones.objects.\
            filter(id_division=id_division).first()
        return context


@login_required(login_url='/login/')
@permission_required('ctg.change_divisiones',
                     login_url='bases:sin_permisos')
def ActualizarDivisionModal(request, pk):
    template_name = 'ctg/actualizar_division_modal.html'
    contexto = {}
    division = Divisiones.objects.filter(pk=pk).first()

    if not division:
        return HttpResponse('No existe la división ' + str(pk))

    if request.method == 'GET':
        contexto = {'division': division}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        division.estado = estado
        division.save()
        return HttpResponse('División actualizada')

    return render(request, template_name, contexto)


class BusquedaDivisionesApiView(APIView):
    def get(self, request, taller, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        divisiones = Divisiones.objects.filter(
            taller=taller,
            estado=estado,
            tipo_catalogo_id=tipo
        )
        data = DivisionesSerializer(divisiones, many=True).data
        return Response(data)



#eliminar Divisiones si no contiene una relacion con  Categorias
@login_required(login_url='/login/')
#permisos
def eliminar_division(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        division = request.GET.get('division', None)
        if division:
            try:
                division_obj = Divisiones.objects.filter(id_division=division).first()
                categoria_division = Categorias.objects.filter(division_id=division_obj.id_division).exists()
                if categoria_division:
                    estado = 2
                else:
                    Divisiones.objects.filter(id_division=division).delete()
                    estado = 1
            except Divisiones.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)




class CategoriasListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_categorias"
    model = Categorias
    template_name = "ctg/categorias_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        taller_obj = self.request.user.taller()
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            return Categorias.objects.\
                filter(division__taller_id=taller_obj.id_taller)
        elif self.request.user.\
                tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            return Categorias.objects.\
                filter(division__taller__pais=self.request.user.pais)


class CategoriasCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_categorias"
    model = Categorias
    template_name = "ctg/categorias_form.html"
    context_object_name = "obj"
    form_class = CategoriaForm
    success_url = reverse_lazy("ctg:categorias_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        id_precio = self.request.POST['precio_definido']
        precio = PreciosDefinidos.objects.\
            filter(id_precio=id_precio).first()
        form.instance.usuario_crea = self.request.user.id
        form.instance.precio_taller_id = precio.id_precio
        form.instance.costo_taller = precio.costo
        form.instance.prct_utilidad_taller = precio.prct_utilidad
        form.instance.precio_taller = precio.precio
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/categorias_form.html",
                          {'mensaje': e.__cause__,
                           'tipos': TiposCatalogo.objects.all(),
                           'form': form})

    def get_context_data(self, **kwargs):
        context = super(CategoriasCrearView, self).get_context_data(**kwargs)
        context['precios'] = PreciosDefinidos.objects.\
            filter(taller=self.request.user.taller())
        return context

    def get_form_kwargs(self):
        kwargs = super(CategoriasCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CategoriasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_categorias"
    model = Categorias
    template_name = "ctg/categorias_form.html"
    form_class = CategoriaForm
    success_url = reverse_lazy("ctg:categorias_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        id_precio = self.request.POST['precio_definido']
        if not id_precio:
            return HttpResponse('No ah elejido un precio.')

        precio = PreciosDefinidos.objects.\
            filter(id_precio=id_precio).first()
        items = Items.objects.\
            filter(categoria=self.object)
        print(items)
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            form.instance.precio_taller_id = precio.id_precio
            form.instance.costo_taller = precio.costo
            form.instance.prct_utilidad_taller = precio.prct_utilidad
            form.instance.precio_taller = precio.precio
            if items:
                for item in items:
                    item.costo_taller = precio.costo
                    item.prct_utilidad_taller = precio.prct_utilidad
                    item.precio_taller = precio.precio
                    item.save()
        elif self.request.user.\
                tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            form.instance.precio_empresa_id = precio.id_precio
            form.instance.prct_utilidad_empresa = precio.prct_utilidad
            form.instance.precio_empresa = precio.precio
            if items:
                for item in items:
                    item.prct_utilidad_empresa = self.object.prct_utilidad_empresa
                    item.precio_empresa = self.object.precio_empresa
                    item.save()
        form.instance.usuario_modifica = self.request.user.id
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/categorias_form.html",
                          {'mensaje': e.__cause__,
                           'tipos': TiposCatalogo.objects.all(),
                           'form': form})

    def get_context_data(self, **kwargs):
        context = super(CategoriasEditarView, self).get_context_data(**kwargs)
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            context['precios'] = PreciosDefinidos.objects.\
                filter(taller=self.request.user.taller())
        elif self.request.user.\
                tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            context['precios'] = PreciosDefinidos.objects.\
                filter(grupo_empresarial=self.request.user.grupo_empresarial())
        id_categoria = self.kwargs['pk']
        context['obj'] = Categorias.objects.\
            filter(id_categoria=id_categoria).first()
        return context

    def get_form_kwargs(self):
        kwargs = super(CategoriasEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['categoria'] = self.object
        return kwargs


@login_required(login_url='/login/')
@permission_required('ctg.change_categorias',
                     login_url='bases:sin_permisos')
def ActualizarCategoriaModal(request, pk):
    template_name = 'ctg/actualizar_categoria_modal.html'
    contexto = {}
    categoria = Categorias.objects.filter(pk=pk).first()

    if not categoria:
        return HttpResponse('No existe la categoría ' + str(pk))

    if request.method == 'GET':
        contexto = {'categoria': categoria}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        categoria.estado = estado
        categoria.save()
        return HttpResponse('Categoría actualizada')

    return render(request, template_name, contexto)


class BusquedaCategoriasApiView(APIView):
    def get(self, request, division, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        categorias = Categorias.objects.filter(
            division_id=division,
            estado=estado,
            tipo_catalogo_id=tipo
        )
        data = CategoriasSerializer(categorias, many=True).data
        return Response(data)



#eliminar Categorias si no contiene una relacion con  Items
@login_required(login_url='/login/')
#permisos
def eliminar_categoria(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        categoria = request.GET.get('categoria', None)
        if categoria:
            try:
                categoria_obj = Categorias.objects.filter(id_categoria=categoria).first()
                categoria_items = Items.objects.filter(categoria_id=categoria_obj.id_categoria).exists()
                if categoria_items:
                    estado = 2
                else:
                    Categorias.objects.filter(id_categoria=categoria).delete()
                    estado = 1
            except Categorias.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)


class TallasListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_tallas"
    model = Tallas
    template_name = "ctg/tallas_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        # taller = Talleres.objects.filter(nombre='NEUTRO').first()
        taller_obj = self.request.user.taller()
        return Tallas.objects.\
            filter(taller=taller_obj,
                   estandar_id=taller_obj.estandar_tallas)


class TallasCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_tallas"
    model = Tallas
    template_name = "ctg/tallas_form.html"
    context_object_name = "obj"
    form_class = TallasForm
    success_url = reverse_lazy("ctg:tallas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/tallas_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


class TallasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_tallas"
    model = Tallas
    template_name = "ctg/tallas_form.html"
    context_object_name = "obj"
    form_class = TallasForm
    success_url = reverse_lazy("ctg:tallas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        form.instance.taller_id = self.request.user.taller().id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/tallas_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


@login_required(login_url='/login/')
@permission_required('ctg.change_tallas',
                     login_url='bases:sin_permisos')
def ActualizarTallaModal(request, pk):
    template_name = 'ctg/actualizar_talla_modal.html'
    contexto = {}
    talla = Tallas.objects.filter(pk=pk).first()

    if not talla:
        return HttpResponse('No existe la talla ' + str(pk))

    if request.method == 'GET':
        contexto = {'talla': talla}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        talla.estado = estado
        talla.save()
        return HttpResponse('Talla actualizada')

    return render(request, template_name, contexto)



#eliminar Talla si no contiene una relacion con  SolicitudTrabajo
@login_required(login_url='/login/')
#permisos
def eliminar_talla(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        talla = request.GET.get('talla', None)
        if talla:
            try:
                talla_obj = Tallas.objects.filter(id_talla=talla).first()
                solicitud_talla = SolicitudTrabajo.objects.filter(talla_id=talla_obj.id_talla).exists()
                if solicitud_talla:
                    estado = 2
                else:
                    Tallas.objects.filter(id_talla=talla).delete()
                    estado = 1
            except Tallas.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)




class ColoresListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_colores"
    model = Colores
    template_name = "ctg/colores_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            return Colores.objects.\
                filter(
                    pais_id=self.request.user.pais_id
                )

        else:
            return Colores.objects.\
                filter(
                    taller_id=self.request.user.taller().id_taller
                )


class ColoresCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_colores"
    model = Colores
    template_name = "ctg/colores_form.html"
    context_object_name = "obj"
    form_class = ColoresForm
    success_url = reverse_lazy("ctg:colores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        form.instance.pais_id = self.request.user.pais_id
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return form.errors



class ColoresEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_colores"
    model = Colores
    template_name = "ctg/colores_form.html"
    context_object_name = "obj"
    form_class = ColoresForm
    success_url = reverse_lazy("ctg:colores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            form.instance.usuario_modifica = self.request.user.id
            return super().form_valid(form)

        else:
            form.instance.usuario_modifica = self.request.user.id
            return super().form_valid(form)

        # taller_obj = self.request.user.taller()
        # form.instance.usuario_modifica = self.request.user.id
        # form.instance.taller_id = taller_obj.id_taller
        # form.instance.pais_id = self.request.user.pais_id
        # return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('ctg.change_colores',
                     login_url='bases:sin_permisos')
def ActualizarColorModal(request, pk):
    template_name = 'ctg/actualizar_color_modal.html'
    contexto = {}
    color = Colores.objects.filter(pk=pk).first()

    if not color:
        return HttpResponse('No existe el color ' + str(pk))

    if request.method == 'GET':
        contexto = {'color': color}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        color.estado = estado
        color.save()
        return HttpResponse('Color actualizado')

    return render(request, template_name, contexto)


#eliminar Color si no contiene una relacion con  ItemsColores
@login_required(login_url='/login/')
#permisos
def eliminar_color(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        color = request.GET.get('color', None)
        if color:
            try:
                color_obj = Colores.objects.filter(id_color=color).first()
                item_color = ItemsColores.objects.filter(color_id=color_obj.id_color).exists()
                if item_color:
                    estado = 2
                else:
                    Colores.objects.filter(id_color=color).delete()
                    estado = 1
            except Colores.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)



class AdicionalesListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_adicionales"
    model = Adicionales
    template_name = "ctg/adicionales_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Adicionales.objects.all()
        else:
            if self.request.user.tipo_usuario_id == 2:
                return Adicionales.objects.\
                    filter(taller_id=self.request.user.taller())
            if self.request.user.tipo_usuario_id == 3:
                return Adicionales.objects.\
                    filter(pais_id=self.request.user.pais_id)


class AdicionalesModalListaView(AdicionalesListaView):
    template_name = "ctg/adicional_agregar_modal.html"

    def get_queryset(self):
        id_item = self.kwargs['pk']
        item = Items.objects.filter(id_item=id_item).first()
        return CategoriaAdicionales.objects.\
            filter(categoria_id=item.categoria_id)

    def get_context_data(self, **kwargs):
        context = super(AdicionalesModalListaView, self).\
            get_context_data(**kwargs)
        context['id_orden'] = self.kwargs['pk']
        return context


class AdicionalesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_adicionales"
    model = Adicionales
    template_name = "ctg/adicionales_form.html"
    context_object_name = "obj"
    form_class = AdicionalesForm
    success_url = reverse_lazy("ctg:adicionales_lista")
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_adicional_crear',
                       kwargs={'pk': self.object.id_adicional})

    def form_valid(self, form):
        utilidad = form.instance.utilidad_operaciones
        costo = form.instance.costo_taller
        precio = float(costo)*float(1+(utilidad/100))
        form.instance.precio_taller = round(precio, 2)
        form.instance.usuario_crea = self.request.user.id
        taller_obj = self.request.user.taller()
        form.instance.taller_id = taller_obj.id_taller
        form.instance.pais_id = self.request.user.pais_id
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/adicionales_form.html",
                          {'mensaje': e.__cause__, 'form': form})

    def get_context_data(self, **kwargs):
        context = super(AdicionalesCrearView, self).get_context_data(**kwargs)
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        return context
    def get_form_kwargs(self):
        kwargs = super(AdicionalesCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs




@login_required(login_url='/login/')
@permission_required('ctg.add_adicionales',
                     login_url='bases:sin_permisos')
def DetalleAdicionalCrearView(request, pk=None):
    template_name = "ctg/detalles_adicional_form.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        adicional = Adicionales.objects.filter(id_adicional=pk).first()
        form_adicional = AdicionalesForm(request=request)
        categorias_lista = Categorias.objects.filter(division__taller_id=adicional.taller_id)
        lista_categorias = []
        categorias_adicional_lista = CategoriaAdicionales.objects.\
            filter(adicional_id=adicional.id_adicional)
        for categoria_adicional in categorias_adicional_lista:
            categoria = [
                str(categoria_adicional.categoria_id)
            ]
            lista_categorias.append(categoria)
        categorias_adicional_lista = json.dumps(lista_categorias)

        categorias_marcar = []
        categorias = Categorias.objects.filter(division__taller_id=adicional.taller_id)
        for categoria in categorias:
            categorias_tmp = {
                'categoria_id': str(categoria.id_categoria)
            }
            categorias_marcar.append(categorias_tmp)
        categorias_marcar = json.dumps(categorias_marcar)


        contexto = {
            'categorias_lista': categorias_lista,
            'form': form_adicional,
            'adicional': adicional,
            'categorias_adicional_lista': categorias_adicional_lista,
            'categorias_marcar': categorias_marcar
            }

    if request.method == 'POST':
        pais_id = request.user.pais_id
        categorias = request.POST.getlist('categorias[]')
        categorias_lista = json.loads(categorias[0])

        categorias_adicional = CategoriaAdicionales.objects.\
            filter(adicional_id=pk)
        if categorias_adicional:
            for categoria_adicional in categorias_adicional:
                categoria_adicional.delete()

        taller_obj = request.user.taller()
        for categoria in categorias_lista:
            infoCategoria = CategoriaAdicionales(
                categoria_id=categoria,
                adicional_id=pk,
                pais_id=request.user.pais_id,
                taller_id=taller_obj.id_taller,
                usuario_crea=request.user.id
            )
            if infoCategoria:
                infoCategoria.save()
        return redirect("ctg:adicionales_lista")

    return render(request, template_name, contexto)


class AdicionalesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_adicionales"
    model = Adicionales
    template_name = "ctg/adicionales_form.html"
    context_object_name = "obj"
    form_class = AdicionalesForm
    # success_url = reverse_lazy("ctg:adicionales_lista")
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_adicional_crear',
                       kwargs={'pk': self.object.id_adicional})

    def form_valid(self, form):
        utilidad = form.instance.utilidad_operaciones
        
        form.instance.costo_taller
        # precio = float(costo)*float(1+(utilidad/100))
        taller_obj = self.request.user.taller()
        form.instance.precio_taller
        form.instance.usuario_modifica = self.request.user.id

        form.instance.taller_id = taller_obj.id_taller
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AdicionalesEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('ctg.change_adicionales',
                     login_url='bases:sin_permisos')
def ActualizarAdicionalModal(request, pk):
    template_name = 'ctg/actualizar_adicional_modal.html'
    contexto = {}
    adicional = Adicionales.objects.filter(pk=pk).first()

    if not adicional:
        return HttpResponse('No existe el adicional ' + str(pk))

    if request.method == 'GET':
        contexto = {'adicional': adicional}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        adicional.estado = estado
        adicional.save()
        return HttpResponse('Adicional actualizado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.view_adicionales',
                     login_url='bases:sin_permisos')
def adicionalDetalleView(request, id_adicional=None):
    template_name = "ctg/detalle_adicional_modal.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        adicional = Adicionales.objects.filter(pk=id_adicional).first()
        categorias = CategoriaAdicionales.objects.filter(adicional=adicional)

        contexto = {
                    'adicional': adicional,
                    'categorias': categorias
                    }
    if request.method == 'POST':
        if id_adicional is None:
            pass
        else:
            json_data = json.loads(request.body)
            utilidad_oper = json_data['utilidad_operaciones']
            adicional = Adicionales.objects.filter(pk=id_adicional).first()
            try:
                adicional.utilidad_operaciones = utilidad_oper
                adicional.save()
            except FileNotFoundError:
                adicional.save()

    return render(request, template_name, contexto)


class PiedrasListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_piedras"
    model = Piedras
    template_name = "ctg/piedras_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Piedras.objects.all()
        else:
            if self.request.user.tipo_usuario_id == 2:
                return Piedras.objects.\
                    filter(taller=self.request.user.taller())
            if self.request.user.tipo_usuario_id == 3:
                return Piedras.objects.\
                    filter(pais=self.request.user.pais)


class PiedrasModalListaView(PiedrasListaView):
    template_name = "ctg/piedra_agregar_modal.html"


    def get_queryset(self):
        id_item = self.kwargs['pk']
        item = Items.objects.filter(id_item=id_item).first()

        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            return Piedras.objects.filter(
                taller=self.request.user.taller(),
                estado__descripcion='ACTIVO'
            )
        else:
            piedras_id = CategoriaPiedras.objects.filter(
                categoria_id=item.categoria_id,
                taller_id=item.taller_id,
                piedra__estado__descripcion='ACTIVO'
            ).values('piedra_id')
            return Piedras.objects.filter(
                id_piedra__in=piedras_id
            )


    def get_context_data(self, **kwargs):
        context = super(PiedrasModalListaView, self).get_context_data(**kwargs)
        context['id_orden'] = self.kwargs['pk']
        return context


class PiedrasCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_piedras"
    model = Piedras
    template_name = "ctg/piedras_form.html"
    context_object_name = "obj"
    form_class = PiedrasForm
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_piedra_crear',
                       kwargs={'pk': self.object.id_piedra})

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        form.instance.pais_id = self.request.user.pais_id
        taller_obj = Talleres.objects.filter(estado__descripcion='ACTIVO', pais_id= self.request.user.pais_id).first()
        form.instance.taller_id = taller_obj.id_taller

        try:
            return super().form_valid(form)
        except IntegrityError as e:
            return render(self.request,
                          "ctg/piedras_form.html",
                          {'mensaje': e.__cause__, 'form': form})

    def get_context_data(self, **kwargs):
        context = super(PiedrasCrearView, self).get_context_data(**kwargs)
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        return context


    def get_form_kwargs(self):
        kwargs = super(PiedrasCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PiedrasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_piedras"
    model = Piedras
    template_name = "ctg/piedras_form.html"
    context_object_name = "obj"
    form_class = PiedrasForm
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_piedra_crear',
                       kwargs={'pk': self.object.id_piedra})

    def form_valid(self, form):
        id_piedra = self.kwargs['pk']
        detalles = DetallePiedras.objects.filter(piedra_id=id_piedra)
        # if detalles:
        #     for detalle in detalles:
        #         costo = detalle.costo
        #         utilidad = form.instance.utilidad_sobre_piedras
        #         precio = float(costo)*float(1+(utilidad/100))
        #         precio = round(precio, 2)
        #         detalle.precio = precio
        #         detalle.save()
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PiedrasEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('ctg.add_piedras',
                     login_url='bases:sin_permisos')
def PiedrasFormView(request, template_name='ctg/piedras_form.html', pk=None):
    form_piedra = PiedrasForm()
    contexto = {}
    piedra = Piedras.objects.filter(id_piedra=pk).first()
    detalles = None
    num_detalles = None
    lista_categorias = []
    categorias_piedra_lista = None

    if request.method == 'GET':
        if piedra:
            form_piedra = PiedrasForm(request=request, instance=piedra)
            detalles = DetallePiedras.objects.filter(piedra=piedra)
            detalles = DetallePiedraSerializer(detalles, many=True).data
            detalles = json.dumps(detalles)
            categorias_piedra_lista = CategoriaPiedras.objects.\
                filter(piedra_id=piedra.id_piedra)
            for categoria_piedra in categorias_piedra_lista:
                categoria = [
                    str(categoria_piedra.categoria_id)
                ]
                lista_categorias.append(categoria)
            categorias_piedra_lista = json.dumps(lista_categorias)
        categorias_lista = Categorias.objects.\
            filter(
                division__taller=request.user.taller(),
                estado__descripcion='ACTIVO'
                )
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()

        contexto = {
            'categorias_lista': categorias_lista,
            'form': form_piedra,
            'detalles': detalles,
            'piedra': piedra,
            'peso_max_img': peso_max_img,
            'ext_perm_img': ext_perm_img,
            'categorias_piedra_lista': categorias_piedra_lista
            }

    if request.method == 'POST':
        imagen = request.FILES.getlist('imagen')
        if imagen:
            imagen = imagen[0]
        sku = request.POST['sku']
        descripcion = request.POST['descripcion']
        detalles = request.POST.getlist('detalles_lista[]')
        detalles_editados = request.POST.getlist('detalles_editados[]')
        categorias = request.POST.getlist('categorias_lista[]')
        detalles = json.loads(detalles[0])
        if detalles_editados:
            detalles_editados = json.loads(detalles_editados[0])
        categorias = json.loads(categorias[0])
        if not piedra:
            infoPiedra = Piedras(
                sku=sku,
                descripcion=descripcion,
                taller=request.user.taller(),
                imagen=imagen,
                pais=request.user.pais,
                usuario_crea=request.user.id
            )
            if infoPiedra:
                infoPiedra.save()
        else:
            if len(imagen) > 0:
                piedra.imagen = imagen[0]
            piedra.descripcion = descripcion
            categorias_piedra = CategoriaPiedras.objects.\
                filter(piedra=piedra)
            if categorias_piedra:
                for categoria_piedra in categorias_piedra:
                    categoria_piedra.delete()
            piedra.usuario_modifica = request.user.id
            piedra.save()
            if len(detalles_editados) > 0:
                for detalle in detalles_editados:
                    detalle_editado = DetallePiedras.objects.\
                        filter(
                            id_detalle_piedra=detalle.get('id')
                        ).first()
                    detalle_editado.costo_taller = detalle.get('costo')
                    detalle_editado.precio_taller = detalle.get('precio')
                    detalle_editado.usuario_modifica = request.user.id
                    detalle_editado.save()
            infoPiedra = piedra
        if len(detalles) > 0:
            for detalle in detalles:
                infoDetalle = DetallePiedras(
                    piedra=infoPiedra,
                    taller=infoPiedra.taller,
                    medida=detalle.get('medida'),
                    costo_taller=detalle.get('costo'),
                    precio_taller=detalle.get('precio'),
                    pais=infoPiedra.pais,
                    usuario_crea=request.user.id
                )
                if infoDetalle:
                    infoDetalle.save()
        if len(categorias) > 0:
            for categoria in categorias:
                infoCategoria = CategoriaPiedras(
                    piedra=infoPiedra,
                    categoria_id=categoria,
                    taller=infoPiedra.taller,
                    pais=infoPiedra.pais,
                    usuario_crea=request.user.id
                )
                if infoCategoria:
                    infoCategoria.save()

    return render(request, template_name, contexto)




def AdicionalSolicitudCrear(request, pk=None):
    template_name= 'ctg/adicionales_form_modal.html'
    contexto = {}
    if request.method == 'POST':
        form = AdicionalesForm(request.POST)
        if form.is_valid():
            print('correcto')        
    return render(request, template_name, contexto)

'''agregar adicionales a solicitud '''



@login_required(login_url='/login/')
@permission_required('ctg.add_piedras',
                     login_url='bases:sin_permisos')
def AdicionalesFormView(request, template_name='ctg/adicionales_form_modal.html'):
    form_adicional = AdicionalesForm()
    contexto = {}
    if request.method == 'GET':
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        contexto = {
            'form': form_adicional,
            'peso_max_img': peso_max_img,
            'ext_perm_img': ext_perm_img,
            }

    if request.method == 'POST':
        imagen = request.FILES.getlist('imagen')
        if imagen:
            imagen = imagen[0]
        sku = request.POST['sku']
        descripcion = request.POST['descripcion']
        costo_taller = request.POST['costo_taller']
        precio_taller = request.POST['precio_taller']

        infoAdicional = Adicionales(
            sku=sku,
            descripcion=descripcion,
            costo_taller=request.POST['costo_taller'],
            imagen=imagen,
            precio_taller=request.POST['precio_taller'],
            usuario_crea=request.user.id,
            taller=request.user.taller(),
            pais_id=request.user.pais_id

        )
        if infoAdicional:
            infoAdicional.save()
    return render(request, template_name, contexto)



@login_required(login_url='/login/')
@permission_required('ctg.add_piedras',
                     login_url='bases:sin_permisos')
def DetallePiedraCrearView(request, pk=None):
    template_name = "ctg/detalles_piedra_form.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        piedra = Piedras.objects.filter(id_piedra=pk).first()
        form_piedra = PiedrasForm(request=request)
        detalles = DetallePiedras.objects.filter(piedra_id=pk)
        num_detalles = DetallePiedras.objects.\
            filter(piedra_id=pk).count()
        categorias_lista = CategoriaPiedras.objects.\
            filter(taller_id=piedra.taller_id)

        contexto = {
            'categorias_lista': categorias_lista,
            'form': form_piedra,
            'detalles': detalles,
            'piedra': piedra,
            'num_detalles': num_detalles
            }

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_piedras',
                     login_url='bases:sin_permisos')
def DetallePiedraCategoriasView(request, pk=None):
    template_name = "ctg/detalles_categorias_piedra_form.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        piedra = Piedras.objects.filter(id_piedra=pk).first()
        form_piedra = PiedrasForm(request=request)
        detalles = DetallePiedras.objects.filter(piedra_id=pk)
        num_detalles = DetallePiedras.objects.\
            filter(piedra_id=pk).count()
        categorias_lista = CategoriaPiedras.objects.\
            filter(taller_id=piedra.taller_id)
        lista_categorias = []
        categorias_piedra_lista = CategoriaPiedras.objects.\
            filter(piedra_id=piedra.id_piedra)
        for categoria_piedra in categorias_piedra_lista:
            categoria = [
                str(categoria_piedra.categoria_id)
            ]
            lista_categorias.append(categoria)
        categorias_piedra_lista = json.dumps(lista_categorias)

        contexto = {
            'categorias_lista': categorias_lista,
            'form': form_piedra,
            'detalles': detalles,
            'piedra': piedra,
            'num_detalles': num_detalles,
            'categorias_piedra_lista': categorias_piedra_lista
            }

    if request.method == 'POST':
        pais_id = request.user.pais_id
        categorias = request.POST.getlist('categorias[]')
        categorias_lista = json.loads(categorias[0])

        categorias_piedra = CategoriaPiedras.objects.filter(piedra_id=pk)
        if categorias_piedra:
            for categoria_piedra in categorias_piedra:
                categoria_piedra.delete()

        for categoria in categorias_lista:
            infoCategoria = CategoriaPiedras(
                categoria_id=categoria,
                piedra_id=pk,
                pais_id=request.user.pais_id,
                taller_id=request.user.taller(),
                usuario_crea=request.user.id
            )
            if infoCategoria:
                infoCategoria.save()
        return redirect("ctg:piedras_lista")

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.add_piedras',
                     login_url='bases:sin_permisos')
def DetallePiedraAgregarView(request, pk=None):
    template_name = "ctg/detalle_piedra_agregar_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        form_item = DetallesPiedraForm()
        piedra = Piedras.objects.filter(id_piedra=pk).first()

        contexto = {
            'form': form_item,
            'piedra': piedra
            }

    if request.method == 'POST':
        piedra = Piedras.objects.filter(id_piedra=pk).first()
        json_data = json.loads(request.body)
        medida = json_data['medida']
        costo = json_data['costo']
        precio = float(costo)*float(1+(piedra.utilidad_sobre_piedras/100))
        precio = round(precio, 2)

        infoDetalle = DetallePiedras(
            medida=medida,
            costo=costo,
            precio=precio,
            usuario_crea=request.user.id,
            pais_id=request.user.pais_id,
            piedra_id=piedra.id_piedra,
            taller_id=piedra.taller_id
        )

        if infoDetalle:
            infoDetalle.save()
            return redirect("ctg:detalles_piedra_crear", pk=piedra.id_piedra)

    return render(request, template_name, contexto)


class DetallePiedraEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_piedras"
    model = DetallePiedras
    template_name = "ctg/detalle_piedra_editar_modal.html"
    context_object_name = "obj"
    form_class = DetallesPiedraForm
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_piedra_crear',
                       kwargs={'pk': self.object.piedra_id})

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        # form.instance.taller_id = self.request.user.taller_id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('ctg.view_piedras',
                     login_url='bases:sin_permisos')
def PiedraDetalleView(request, id_piedra=None):
    template_name = "ctg/detalle_piedra_modal.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        piedra = Piedras.objects.filter(pk=id_piedra).first()
        detalles = DetallePiedras.objects.filter(piedra=piedra)
        categorias = CategoriaPiedras.objects.filter(piedra=piedra)

        contexto = {
                    'piedra': piedra,
                    'detalles': detalles,
                    'categorias': categorias
                    }
    if request.method == 'POST':
        if id_piedra is None:
            pass
        else:
            json_data = json.loads(request.body)
            utilidad_op = json_data['prct_utilidad']
            piedra = Piedras.objects.filter(pk=id_piedra).first()
            try:
                piedra.prct_utilidad_op = utilidad_op
                piedra.save()
            except FileNotFoundError:
                piedra.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_piedras',
                     login_url='bases:sin_permisos')
def ActualizarDetallePiedraModal(request, pk):
    template_name = 'ctg/actualizar_detalle_piedra_modal.html'
    contexto = {}
    detalle = DetallePiedras.objects.filter(pk=pk).first()

    if not detalle:
        return HttpResponse('No existe el detalle ' + str(pk))

    if request.method == 'GET':
        contexto = {'detalle': detalle}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        detalle.estado = estado
        detalle.save()
        return HttpResponse('Detalle actualizado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_piedras',
                     login_url='bases:sin_permisos')
def DetallePiedraEliminarView(request, id_detalle=None):
    template_name = "ctg/detalles_piedra_form.html"
    form_rol = {}
    contexto = {}

    if request.method == 'POST':
        detalle = DetallePiedras.objects.\
            filter(id_detalle_piedra=id_detalle).first()
        piedra = Piedras.objects.\
            filter(id_piedra=detalle.piedra_id).first()
        detalle.delete()
        return redirect("ctg:detalles_piedra_crear", pk=piedra.id_piedra)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_piedras',
                     login_url='bases:sin_permisos')
def ActualizarPiedraModal(request, pk):
    template_name = 'ctg/actualizar_piedra_modal.html'
    contexto = {}
    piedra = Piedras.objects.filter(pk=pk).first()

    if not piedra:
        return HttpResponse('No existe la piedra ' + str(pk))

    if request.method == 'GET':
        contexto = {'piedra': piedra}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        piedra.estado = estado
        piedra.save()
        return HttpResponse('Piedra actualizada')

    return render(request, template_name, contexto)





#eliminar Piedra si no contiene registros dentro de la tabla de solicitudPiedras
@login_required(login_url='/login/')
#permisos
def eliminar_piedra(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        piedra = request.GET.get('piedra', None)
        if piedra:
            try:
                piedra_obj = Piedras.objects.filter(id_piedra=piedra).first()
                item_piedra = SolicitudesPiedras.objects.filter(piedra_id=piedra_obj.id_piedra).exists()
                if item_piedra:
                    estado = 2
                else:
                    Piedras.objects.filter(id_piedra=piedra).delete()
                    estado = 1
            except Piedras.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status = 400)




class ItemsListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/items_lista.html"
    login_url = "bases:login"

    def get_context_data(self, **kwargs):
        context = super(ItemsListaView, self).get_context_data(**kwargs)
        taller_obj = self.request.user.taller()
        if taller_obj is None:
            taller_obj = Talleres.objects.filter(nombre='NEUTRO').first()
        tipo = int(self.kwargs['tipo'])
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'

        divisiones = Divisiones.objects.\
            filter(
                taller_id=taller_obj.id_taller
                )
        categorias = Categorias.objects.\
            filter(
                permite_solicitud=solicitud,
                division__tipo_catalogo__descripcion=tipoCatalogo,
                division__taller=taller_obj
                )
        context['tipo'] = tipo
        context['divisiones'] = divisiones
        context['categorias'] = categorias
        return context


class BusquedaItemsTallerApiView(APIView):
    def post(self, request):
        # print('**************************')
        divisiones = self.request.POST['divisionesBusqueda[]']
        divisiones = json.loads(divisiones)
        categorias = self.request.POST['categoriasBusqueda[]']
        categorias = json.loads(categorias)
        clave = self.request.POST['claveBusqueda']
        limite = int(self.request.POST['limite'])
        tipo = int(self.request.POST['tipo'])

        # taller_prioridad_mayor  = Talleres.objects.filter(pais=self.request.user.pais, id_taller=self.reques.user.taller().taller_id).values('prioridad')
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'
        items1 = Items.objects.filter(
            descripcion__icontains=clave,
            categoria__permite_solicitud=solicitud,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
            categoria__categoria_alianzas=False
        ) | Items.objects.filter(
            sku__icontains=clave,
            categoria__permite_solicitud=solicitud,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
            categoria__categoria_alianzas=False
        )
        items2 = Items.objects.filter(
            categoria__division_id__in=divisiones,
            categoria__permite_solicitud=solicitud,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
            categoria__categoria_alianzas=False
        )
        items3 = Items.objects.filter(
            categoria_id__in=categorias,
            categoria__permite_solicitud=solicitud,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
            categoria__categoria_alianzas=False
        )
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
             items4 = Items.objects.filter(
                taller=self.request.user.taller(),
                categoria__permite_solicitud=solicitud,
                categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
                categoria__categoria_alianzas=False,
                estado__descripcion='ACTIVO'
            )

        else:
            items4 = Items.objects.filter(
                taller=self.request.user.taller(),
                categoria__permite_solicitud=solicitud,
                categoria__division__tipo_catalogo__descripcion=tipoCatalogo,
                categoria__categoria_alianzas=False,
            )
        if clave == '' and len(divisiones) == 0 and len(categorias) == 0:
            items = (items4).order_by('sku', 'taller__prioridad')[:limite]
        elif clave == '' and len(divisiones) == 0 and len(categorias) > 0:
            items = (items3).order_by('sku', 'taller__prioridad')[:limite]
        elif clave == '' and len(divisiones) > 0 and len(categorias) == 0:
            items = (items2).order_by('sku', 'taller__prioridad')[:limite]
        elif clave == '' and len(divisiones) > 0 and len(categorias) > 0:
            items = (items2 & items3).order_by('sku', 'taller__prioridad')[:limite]
        elif clave != '' and len(divisiones) == 0 and len(categorias) == 0:
            items = (items4 & items1).order_by('sku', 'taller__prioridad')[:limite]
        elif clave != '' and len(divisiones) == 0 and len(categorias) > 0:
            items = (items1 & items3).order_by('sku', 'taller__prioridad')[:limite]
        elif clave != '' and len(divisiones) > 0 and len(categorias) == 0:
            items = (items1 & items2).order_by('sku', 'taller__prioridad')[:limite]
        elif clave != '' and len(divisiones) > 0 and len(categorias) > 0:
            items = (items1 & items2 & items3).order_by('sku', 'taller__prioridad')[:limite]
        
        data = ItemsSerializer(items, many=True).data
        return Response(data)


class ProductosListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/productos_lista.html"
    login_url = "bases:login"


class ItemsListaProductosApiView(APIView):
    def get(self, request, tipo, limite):
        if tipo == 1:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='PRODUCTOS',
                taller_id=request.user.taller(),
                categoria__permite_solicitud=True
            ).order_by('-fecha_creacion')[:limite]
        else:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='PRODUCTOS',
                taller_id=request.user.taller(),
                categoria__permite_solicitud=False
            ).order_by('-fecha_creacion')[:limite]
        data = ItemsListaSerializer(items, many=True).data
        return Response(data)


class ServiciosListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/servicios_lista.html"
    login_url = "bases:login"


class ItemsListaServiciosApiView(APIView):
    def get(self, request, tipo, limite):
        if tipo == 1:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='SERVICIOS',
                taller_id=request.user.taller(),
                categoria__permite_solicitud=True
            ).order_by('-fecha_creacion')[:limite]
        else:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='SERVICIOS',
                taller_id=request.user.taller(),
                categoria__permite_solicitud=False
            ).order_by('-fecha_creacion')[:limite]
        data = ItemsListaSerializer(items, many=True).data
        return Response(data)


class ProductosOpeListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/productos_ope_lista.html"
    login_url = "bases:login"


class ItemsOpeListaProductosApiView(APIView):
    def get(self, request, tipo, limite):
        if tipo == 1:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='PRODUCTOS',
                taller__pais=request.user.pais,
                categoria__permite_solicitud=True
            ).order_by('-fecha_creacion')[:limite]
        else:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='PRODUCTOS',
                taller__pais=request.user.pais,
                categoria__permite_solicitud=False
            ).order_by('-fecha_creacion')[:limite]
        data = ItemsListaSerializer(items, many=True).data
        return Response(data)


class ServiciosOpeListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/servicios_ope_lista.html"
    login_url = "bases:login"


class ItemsOpeListaServiciosApiView(APIView):
    def get(self, request, tipo, limite):
        if tipo == 1:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='SERVICIOS',
                taller__pais=request.user.pais,
                categoria__permite_solicitud=True
            ).order_by('-fecha_creacion')[:limite]
        else:
            items = Items.objects.filter(
                tipo_catalogo__descripcion='SERVICIOS',
                taller__pais=request.user.pais,
                categoria__permite_solicitud=False
            ).order_by('-fecha_creacion')[:limite]
        data = ItemsListaSerializer(items, many=True).data
        # return Response(data)
        return JsonResponse({'items': data, 'cantidad': 10})


class CatalogoItemsView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/catalogo_items.html"
    login_url = "bases:login"

    def get_context_data(self, **kwargs):
        context = super(CatalogoItemsView, self).get_context_data(**kwargs)
        tipo = int(self.kwargs['tipo'])
        talleres = Talleres.objects.\
            filter(pais=self.request.user.pais)
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'
        categorias = Categorias.objects.\
            filter(
                estado__descripcion='ACTIVO',
                permite_solicitud=solicitud,
                division__tipo_catalogo__descripcion=tipoCatalogo,
                division__taller__pais=self.request.user.pais
            ).\
            order_by('division__taller__prioridad')

        print(tipo)
        context['tipo'] = tipo
        context['talleres'] = talleres
        context['categorias'] = categorias
        return context


class BusquedaItemsApiView(APIView):
    def post(self, request):
        talleres = self.request.POST['talleresBusqueda[]']
        talleres = json.loads(talleres)
        categorias = self.request.POST['categoriasBusqueda[]']
        categorias = json.loads(categorias)
        clave = self.request.POST['claveBusqueda']
        limite = int(self.request.POST['limite'])
        tipo = int(self.request.POST['tipo'])
        print(tipo)
        print(clave)
        print(len(categorias))
        print('**********')
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'
        items1 = Items.objects.filter(
            estado__descripcion='ACTIVO',
            descripcion__icontains=clave,
            categoria__permite_solicitud=solicitud,
            categoria__categoria_alianzas=False,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo
        ) | Items.objects.filter(
            estado__descripcion='ACTIVO',
            sku__icontains=clave,
            categoria__permite_solicitud=solicitud,
            categoria__categoria_alianzas=False,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo
        )
        items2 = Items.objects.filter(
            estado__descripcion='ACTIVO',
            taller_id__in=talleres,
            taller__pais=self.request.user.pais,
            categoria__permite_solicitud=solicitud,
            categoria__categoria_alianzas=False,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo
        )
        items3 = Items.objects.filter(
            estado__descripcion='ACTIVO',
            categoria_id__in=categorias,
            categoria__permite_solicitud=solicitud,
            categoria__categoria_alianzas=False,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo
        )
        items4 = Items.objects.filter(
            estado__descripcion='ACTIVO',
            taller__pais=self.request.user.pais,
            categoria__permite_solicitud=solicitud,
            categoria__categoria_alianzas=False,
            categoria__division__tipo_catalogo__descripcion=tipoCatalogo
        )

        if clave == '' and len(talleres) == 0  and len(categorias) == 0:
            items = (items4).order_by('taller__prioridad', 'sku')[:limite]
        elif clave == '' and len(talleres) == 0 and len(categorias) > 0:
            items = (items3).order_by('taller__prioridad', 'sku')[:limite]
        elif clave == '' and len(talleres) > 0 and len(categorias) == 0:
            items = (items2).order_by('taller__prioridad', 'sku')[:limite]
        elif clave == '' and len(talleres) > 0 and len(categorias) > 0:
            items = (items2 & items3).order_by('taller__prioridad', 'sku')[:limite]
        elif clave != ''  and len(talleres) == 0 and len(categorias) == 0:
            items = (items4 & items1).order_by('taller__prioridad', 'sku')[:limite]
        elif clave != '' and len(talleres) == 0 and len(categorias) > 0:
            items = (items1 & items3).order_by('taller__prioridad', 'sku')[:limite]
        elif clave != '' and len(talleres) > 0 and len(categorias) == 0:
            items = (items1 & items2).order_by('taller__prioridad', 'sku')[:limite]
        elif clave != '' and len(talleres) > 0 and len(categorias) > 0:
            items = (items1 & items2 & items3).order_by('taller__prioridad', 'sku')[:limite]

        # print(items)  
        items_lista = []
        for item in items:
            if item.taller.estado_id == 1:
                items_lista.append(item)
            else:
                pass
        data = ItemsSerializer((items_lista), many=True).data
        return Response(data)


class ItemsTodosApiView(APIView):
    def get(self, request, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        items = Items.objects.filter(
            tipo_catalogo=tipo,
            taller__pais_id=request.user.pais_id,
            estado=estado
        )
        data = ItemsSerializer(items, many=True).data
        return Response(data)


class ItemsPorTallerApiView(APIView):
    def get(self, request, taller, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        items = Items.objects.filter(
            tipo_catalogo=tipo,
            pais_id=request.user.pais_id,
            estado=estado,
            taller_id=taller
        )
        data = ItemsSerializer(items, many=True).data
        return Response(data)


class ItemsPorDivisionApiView(APIView):
    def get(self, request, division, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        items = Items.objects.filter(
            tipo_catalogo=tipo,
            pais_id=request.user.pais_id,
            estado=estado,
            categoria__division_id=division
        )
        data = ItemsSerializer(items, many=True).data
        return Response(data)


class ItemsPorCategoriaApiView(APIView):
    def get(self, request, categoria, tipo):
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        items = Items.objects.filter(
            tipo_catalogo=tipo,
            pais_id=request.user.pais_id,
            estado=estado,
            categoria_id=categoria
        )
        data = ItemsSerializer(items, many=True).data
        return Response(data)


@login_required(login_url='/login/')
@permission_required('ctg.view_items',
                     login_url='bases:sin_permisos')
def FijoListaView(request):
    template_name = "ctg/catalogo_fijo.html"
    contexto = {}
    estado = Estados.objects.\
        filter(descripcion='ACTIVO').first()

    if request.method == 'GET':
        productos = Items.objects.\
            filter(
                categoria__division__tipo_catalogo__descripcion='PRODUCTOS',
                categoria__permite_solicitud=True
                ).\
            filter(taller__pais_id=request.user.pais_id).\
            filter(estado=estado)
        servicios = Items.objects.\
            filter(
                categoria__division__tipo_catalogo__descripcion='SERVICIOS',
                categoria__permite_solicitud=True
                ).\
            filter(taller__pais_id=request.user.pais_id).\
            filter(estado=estado)
        talleres = Talleres.objects.filter(
            pais=request.user.pais
        )

        contexto = {
            'productos': productos,
            'servicios': servicios,
            'talleres': talleres
        }

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.add_items',
                     login_url='bases:sin_permisos')
def ItemsCrearView(request, tipo=None):
    template_name = "ctg/items_form.html"
    form = ItemsForm()
    contexto = {}
    taller_obj = request.user.taller()

    if request.method == 'GET':
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'
        categorias = Categorias.objects.filter(
            division__taller=request.user.taller(),
            division__tipo_catalogo__descripcion=tipoCatalogo,
            permite_solicitud=solicitud
        )
        proveedores = Proveedores.objects.\
            filter(taller= taller_obj.id_taller)

        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        contexto = {
            'tipo': tipo,
            'categorias': categorias,
            'proveedores': proveedores,
            'solicitud': solicitud,
            'peso_max_img': peso_max_img,
            'ext_perm_img': ext_perm_img,
            'form': form,
                    }
    if request.method == 'POST':
        sku = request.POST['sku']
        categoria = request.POST['categoria']
        categoria = Categorias.objects.\
            filter(id_categoria=categoria).first()
        descripcion = request.POST['descripcion']
        costo_taller = request.POST['costo']
        prct_utilidad_taller = request.POST['utilidad']
        precio_taller = request.POST['precio']
        escala_peso = request.POST['escala_peso']
        costo_gramo_dif = request.POST['valor_gramo_dif']
        if costo_gramo_dif == '':
            costo_gramo_dif = 0
        peso_dif = request.POST['peso_max_dif']
        if peso_dif == '':
            peso_dif = 0
        cantidad_piedras = request.POST['cantidad_piedras']
        if cantidad_piedras == '':
            cantidad_piedras = 0
        costo_piedras = request.POST['costo_piedras']
        if costo_piedras == '':
            costo_piedras = 0
        parte_interna = request.POST['parte_interna']
        acabado = request.POST['acabado']
        tmp_ent_min = request.POST['tiempo_entrega_min']
        if tmp_ent_min == '':
            tmp_ent_min = 0
        tmp_ent_max = request.POST['tiempo_entrega_max']
        if tmp_ent_max == '':
            tmp_ent_max = 0
        id_proveedor = int(request.POST['proveedor'])
        if id_proveedor == 0:
            id_proveedor = None
        datos_extras = request.POST['datos_extras']
        if datos_extras:
            if datos_extras == 'true':
                datos_extras = True
            else:
                datos_extras = False
        else:
            datos_extras = None
        imagenes = request.FILES.getlist('imagen')

        infoItem = Items(
            sku=sku,
            descripcion=descripcion,
            tipo_catalogo=categoria.division.tipo_catalogo,
            taller=categoria.division.taller,
            categoria=categoria,
            costo_taller=costo_taller,
            precio_taller=precio_taller,
            prct_utilidad_taller=prct_utilidad_taller,
            valor_gramo_dif=costo_gramo_dif,
            peso_max_dif=peso_dif,
            escala_peso=escala_peso,
            parte_interna=parte_interna,
            acabado=acabado,
            cantidad_piedras=cantidad_piedras,
            costo_piedras=costo_piedras,
            tiempo_entrega_min=tmp_ent_min,
            tiempo_entrega_max=tmp_ent_max,
            datos_extra=datos_extras,
            id_proveedor=id_proveedor,
            usuario_crea=request.user.id,
            unidad_medida=categoria.unidad_medida,
            precio_empresa=categoria.precio_empresa,
            prct_utilidad_empresa = categoria.prct_utilidad_empresa
        )
        if infoItem:
            try:
                infoItem.save()
            except IntegrityError as e:
                return JsonResponse(
                    {'mensaje': str(e.__cause__)},
                    status=500)

        for imagen in imagenes:
            infoImg = ItemsImagenes(
                usuario_crea=request.user.id,
                imagen=imagen,
                item=infoItem,
                taller=infoItem.taller
            )
            if infoImg:
                infoImg.save()


        if categoria.permite_solicitud or \
                categoria.precio_taller_obj().tipo.descripcion == 'UNIDAD' or \
                categoria.division.tipo_catalogo.descripcion == 'SERVICIOS':
            unidad = UnidadesMedida.objects.\
                filter(descripcion='TALLA').first()
            sin_color = Colores.objects.\
                filter(descripcion='SIN COLOR').first()
            infoItemColor = ItemsColores(
                color_id=sin_color.id_color,
                item_id=infoItem.id_item,
                usuario_crea=request.user.id
            )
            if infoItemColor:
                infoItemColor.save()

            infoDetalle = DetalleItems(
                medida=0,
                estandar='AMERICANO',
                peso_minimo=0,
                peso_maximo=0,
                cantidad_piedras=0,
                id_item_id=infoItem.id_item,
                usuario_crea=request.user.id
            )
            if infoDetalle:
                infoDetalle.save()
            redireccion = 1
        else:
            redireccion = 2
        return JsonResponse(
            {
                'mensaje': 'correcto',
                'id_item': infoItem.id_item,
                'redireccion': redireccion
            },
            status=200)
    return render(request, template_name, contexto)




class CategoriasTalleresApiView(APIView):
    def post(self, request):
        print('holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        talleres = self.request.POST['talleresBusqueda[]']
        talleres = json.loads(talleres)
        # categorias = self.request.POST['categoriasBusqueda[]']
        # categorias = json.loads(categorias)
        # clave = self.request.POST['claveBusqueda']
        # limite = int(self.request.POST['limite'])
        tipo = int(self.request.POST['tipo'])
        if tipo == 1:
            solicitud = False
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 2:
            solicitud = False
            tipoCatalogo = 'SERVICIOS'
        elif tipo == 3:
            solicitud = True
            tipoCatalogo = 'PRODUCTOS'
        elif tipo == 4:
            solicitud = True
            tipoCatalogo = 'SERVICIOS'
        categorias1 = Categorias.objects.filter(
            estado__descripcion='ACTIVO',
            permite_solicitud=solicitud,
            division__tipo_catalogo__descripcion=tipoCatalogo,
            division__taller__pais=self.request.user.pais
        )
        categorias2 = Categorias.objects.filter(
            estado__descripcion='ACTIVO',
            permite_solicitud=solicitud,
            division__tipo_catalogo__descripcion=tipoCatalogo,
            division__taller_id__in=talleres
        )
        if len(talleres) == 0:
            categorias = (categorias1).order_by('descripcion')
        else:
            categorias = (categorias2).order_by('descripcion')
        data = CategoriasSerializer(categorias, many=True).data

        return Response(data)



class ItemsEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_items"
    model = Items
    template_name = "ctg/items_editar_form.html"
    form_class = ItemsForm
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        categoria_id = self.request.POST['categoria']
        categoria = Categorias.objects.\
            filter(id_categoria=categoria_id).first()
        form.instance.categoria = categoria
        form.instance.tipo_catalogo = categoria.division.tipo_catalogo
        costo_taller = self.request.POST['costo']
        prct_utilidad_taller = self.request.POST['utilidad']
        precio_taller = self.request.POST['precio']
        print('**************')
        print(costo_taller)
        print(precio_taller)
        print(prct_utilidad_taller)
        print('**************')
        form.instance.costo_taller = costo_taller
        form.instance.prct_utilidad_taller = prct_utilidad_taller
        form.instance.precio_taller = precio_taller
        id_proveedor = (self.request.POST.get('proveedor', None))
        print(id_proveedor)
        if id_proveedor is None :
            id_proveedor = 0
        form.instance.id_proveedor = id_proveedor
        self.object = form.save()
        editar_imagenes = self.request.POST['editar_imagenes']
        if editar_imagenes == 'true':
            imagenes_lista = ItemsImagenes.objects.\
                filter(item=self.object)
            for imagen in imagenes_lista:
                imagen.delete()
            imagenes = self.request.FILES.getlist('imagen')
            for imagen in imagenes:
                infoImg = ItemsImagenes(
                    usuario_crea=self.request.user.id,
                    imagen=imagen,
                    item=self.object,
                    taller=self.object.taller
                )
                if infoImg:
                    infoImg.save()
        if categoria.permite_solicitud or \
                categoria.precio_taller_obj().tipo.descripcion == 'UNIDAD' or \
                categoria.division.tipo_catalogo.descripcion == 'SERVICIOS':
            redireccion = 1
        else:
            redireccion = 2
        return JsonResponse(
            {
                'mensaje': 'correcto',
                'id_item': self.object.id_item,
                'redireccion': redireccion
            },
            status=200)

    def get_context_data(self, **kwargs):
        taller_obj = self.request.user.taller()
        context = super(ItemsEditarView, self).get_context_data(**kwargs)
        id_item = self.kwargs['pk']
        item = Items.objects.filter(id_item=id_item).first()
        context['obj'] = item
        categorias = Categorias.objects.filter(
            division__taller=taller_obj,
            division__tipo_catalogo=item.categoria.division.tipo_catalogo,
            permite_solicitud=item.categoria.permite_solicitud
        )
        context['categorias'] = categorias
        imagenes = []
        imagenes_lista = ItemsImagenes.objects.\
            filter(item=item)
        context['imagenes'] = imagenes_lista
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        if taller_obj != None:
            context['proveedores'] = Proveedores.objects.\
                filter(taller=taller_obj.id_taller)
        # print(context['proveedores'])
        return context


@login_required(login_url='/login/')
@permission_required('ctg.view_items',
                     login_url='bases:sin_permisos')
def ActualizarPrecioOpeView(request, id_item=None):
    template_name = "ctg/actualizar_precio_ope_modal.html"
    form_rol = {}
    contexto = {}
    item = Items.objects.filter(pk=id_item).first()

    if request.method == 'GET':
        imagenes = ItemsImagenes.objects.\
            filter(item=item)

        contexto = {
                    'item': item,
                    'imagenes': imagenes,
                    }

    if request.method == 'POST':
        json_data = json.loads(request.body)
        precio = json_data['precio']
        utilidad = json_data['utilidad']
        item.precio_empresa = precio
        item.prct_utilidad_empresa = utilidad
        item.save()
        if item.categoria.division.\
                tipo_catalogo.descripcion == 'PRODUCTOS':
            redireccion = 1
        elif item.categoria.division.\
                tipo_catalogo.descripcion == 'SERVICIOS':
            redireccion = 2
        return JsonResponse(
                    {'redireccion': redireccion},
                    status=200)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.add_items',
                     login_url='bases:sin_permisos')
def DetalleCrearView(request, pk=None):
    template_name = "ctg/detalles_form.html"
    form_item = {}
    contexto = {}
    detalles = None

    if request.method == 'GET':
        item = Items.objects.filter(id_item=pk).first()
        detalles_lista = DetalleItems.objects.filter(id_item_id=item.id_item)
        detalles = DetallesSerializer(detalles_lista, many=True).data
        detalles = json.dumps(detalles)

        num_detalles = DetalleItems.objects.\
            filter(id_item_id=pk).count()
        colores_lista = Colores.objects.\
            filter(pais_id=request.user.pais_id,
                   taller=request.user.taller())
        imagenes = ItemsImagenes.objects.\
            filter(item_id=pk)

        contexto = {
            'colores_lista': colores_lista,
            'imagenes': imagenes,
            'form': form_item,
            'detalles_lista': detalles,
            'item': item,
            'num_detalles': num_detalles
            }
    return render(request, template_name, contexto)



@login_required(login_url='/login/')
# @permission_required('ctg.add_items',
#                      login_url='bases:sin_permisos')
def detalles_editados(request, pk=None):
    if request.method == 'POST':
        item_obj = Items.objects.filter(id_item=pk).first()
        detalles_actualizados = request.POST.getlist('detallesEdit[]')
        detalles_actualizados = json.loads(detalles_actualizados[0])
        longitud = len(detalles_actualizados)
        if longitud > 0:
            for detalle in detalles_actualizados:
                # actualizamos los valores por detalle de la lista
                detalleInfo = DetalleItems.objects.filter(id_detalle_item=detalle.get('id')).first()
                # print(detalleInfo)
                detalleInfo.peso_minimo = detalle.get('peso_minimo')
                detalleInfo.peso_maximo = detalle.get('peso_maximo')
                detalleInfo.cantidad_piedras = detalle.get('piedras')
                detalleInfo.costo_piedras = detalle.get('costo_piedras')
                detalleInfo.usuario_modifica = request.user.id
                detalleInfo.save()
            return HttpResponse('Detalle actualizado')



@login_required(login_url='/login/')
def eliminar_detalle_item(request):
    if request.is_ajax and request.method == "GET":
        detalle=request.GET['id']
        print(detalle)
        if detalle:
            try:
                detalle_obj = DetalleItems.objects.filter(id_detalle_item=int(detalle)).first()
                detalle_orden = DetalleOrden.objects.filter(id_detalle_item=detalle_obj.id_detalle_item).exists()
                detalle_solicitud = DetalleSolicitud.objects.filter(item_id=detalle_obj.id_item_id).exists()
                if detalle_orden == True or detalle_solicitud == True:
                    estado = 0
                else:
                    detalle_obj.delete()
                    estado=1
            except DetalleItems.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
                
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)





class DetalleEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_items"
    model = DetalleItems
    template_name = "ctg/detalle_editar_modal.html"
    context_object_name = "obj"
    form_class = DetallesForm
    login_url = "bases:login"

    def get_success_url(self, **kwargs):
        return reverse('ctg:detalles_crear',
                       kwargs={'pk': self.object.id_item_id})

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('ctg.add_items',
                     login_url='bases:sin_permisos')
def ActualizarDetalleItemModal(request, pk):
    template_name = 'ctg/actualizar_detalle_item_modal.html'
    contexto = {}
    detalle = DetalleItems.objects.filter(pk=pk).first()

    if not detalle:
        return HttpResponse('No existe detalle ' + str(pk))

    if request.method == 'GET':
        contexto = {
            'detalle': detalle
            }

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        detalle.estado = estado
        detalle.save()
        return HttpResponse('Detalle actualizado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.add_items',
                     login_url='bases:sin_permisos')
def DetalleColoresAgregarView(request, pk=None):
    template_name = "ctg/detalles_colores_form.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        taller_obj = request.user.taller()
        item = Items.objects.filter(id_item=pk).first()
        # tipo = item.tipo_catalogo_id
        taller = Talleres.objects.filter(nombre='NEUTRO').first()
        # form_item = ItemsForm(tipo=tipo, request=request)
        detalles = DetalleItems.objects.filter(id_item_id=pk)
        num_detalles = DetalleItems.objects.\
            filter(id_item_id=pk).count()
        colores_lista = Colores.objects.\
            filter(pais_id=request.user.pais_id,
                   taller_id=taller_obj.id_taller)
        item_colores = []
        colores_item_lista = ItemsColores.objects.\
            filter(item_id=pk)
        for color_item in colores_item_lista:
            color = [
                str(color_item.color_id)
            ]
            item_colores.append(color)
        colores_item_lista = json.dumps(item_colores)
        imagenes = ItemsImagenes.objects.\
            filter(item_id=pk)

        contexto = {
            'colores_lista': colores_lista,
            'form': form_item,
            'detalles': detalles,
            'item': item,
            'num_detalles': num_detalles,
            'colores_item_lista': colores_item_lista,
            'imagenes': imagenes
            }

    if request.method == 'POST':
        pais_id = request.user.pais_id
        colores = request.POST.getlist('colores[]')
        colores_lista = json.loads(colores[0])

        colores_item = ItemsColores.objects.filter(item_id=pk)
        if colores_item:
            for color_item in colores_item:
                color_item.delete()

        for color in colores_lista:
            infoColor = ItemsColores(
                color_id=color,
                item_id=pk,
                usuario_crea=request.user.id
            )
            if infoColor:
                infoColor.save()
        return redirect("ctg:items_lista", tipo=1)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.add_items',
                     login_url='bases:sin_permisos')
def DetalleAgregarView(request, pk=None):
    template_name = "ctg/detalle_agregar_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        taller_obj = request.user.taller()
        form_item = DetallesForm(request=request)
        item = Items.objects.filter(id_item=pk).first()
        sin_talla = Tallas.objects.filter(talla=0).first()
        tallas = Tallas.objects.\
            filter(taller=taller_obj,
                   estandar_id=taller_obj.estandar_tallas)

        contexto = {
            'form': form_item,
            'item': item,
            'sin_talla': sin_talla,
            'tallas': tallas
            }

    if request.method == 'POST':
        item = Items.objects.filter(id_item=pk).first()
        json_data = json.loads(request.body)
        tipo = json_data['tipo']
        peso_minimo = json_data['peso_minimo']
        peso_maximo = json_data['peso_maximo']
        cantidad_piedras = json_data['cantidad_piedras']
        costo_piedras = json_data['costo_piedras']
        if tipo == 1:
            talla_min = json_data['talla_min']
            talla_min = float(talla_min.replace(',', '.'))
            talla_max = json_data['talla_max']
            talla_max = float(talla_max.replace(',', '.'))
            tallas = Tallas.objects.\
                filter(talla__gte=talla_min,
                       talla__lte=talla_max).\
                filter(taller_id=item.taller_id).\
                order_by('talla')
            for talla in tallas:
                infoDetalle = DetalleItems(
                    medida=talla.talla,
                    peso_minimo=peso_minimo,
                    peso_maximo=peso_maximo,
                    cantidad_piedras=cantidad_piedras,
                    costo_piedras=costo_piedras,
                    id_item_id=item.id_item,
                    estandar=talla.estandar.descripcion,
                    usuario_crea=request.user.id
                )

                if infoDetalle:
                    try:
                        infoDetalle.save()
                    except IntegrityError as e:
                        return HttpResponse('duplicado')
            return HttpResponse('ok')

        if tipo == 2:
            medida = json_data['medida']
            infoDetalle = DetalleItems(
                medida=medida,
                peso_minimo=peso_minimo,
                peso_maximo=peso_maximo,
                cantidad_piedras=cantidad_piedras,
                costo_piedras=costo_piedras,
                id_item_id=item.id_item,
                usuario_crea=request.user.id
            )

            if infoDetalle:
                try:
                    infoDetalle.save()
                    return HttpResponse('ok')
                except IntegrityError as e:
                    return HttpResponse('duplicado')

        return redirect("ctg:detalles_crear", pk=item.id_item)

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.view_items',
                     login_url='bases:sin_permisos')
def ItemDetalleView(request, id_item=None):
    template_name = "ctg/detalle_item_modal.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        item = Items.objects.filter(pk=id_item).first()
        detalles = DetalleItems.objects.filter(id_item=item)
        colores = ItemsColores.objects.filter(item=item)
        imagenes = ItemsImagenes.objects.\
            filter(item=item)

        contexto = {
                    'item': item,
                    'detalles': detalles,
                    'colores': colores,
                    'imagenes': imagenes
                    }

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_items',
                     login_url='bases:sin_permisos')
def InactivarItemModal(request, id_item):
    template_name = 'ctg/inactivar_item_modal.html'
    contexto = {}
    item = Items.objects.filter(pk=id_item).first()

    if not item:
        return HttpResponse('No existe el ítem ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'item': item}

    if request.method == 'POST':
        estado = Estados.objects.\
            filter(descripcion='INACTIVO').first()
        item.estado = estado
        item.save()
        return HttpResponse('Ítem inactivado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.change_items',
                     login_url='bases:sin_permisos')
def ActivarItemModal(request, id_item):
    template_name = 'ctg/activar_item_modal.html'
    contexto = {}
    item = Items.objects.filter(pk=id_item).first()

    if not item:
        return HttpResponse('No existe el ítem ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'item': item}

    if request.method == 'POST':
        estado = Estados.objects.\
            filter(descripcion='ACTIVO').first()
        item.estado = estado
        item.save()
        return HttpResponse('Ítem activado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('ctg.view_items',
                     login_url='bases:sin_permisos')
def ContarCotizacion(request, id_item, tipo):
    template_name = 'ctg/contar_cotizacion_modal.html'
    contexto = {}
    item = Items.objects.filter(pk=id_item).first()

    if not item:
        return HttpResponse('No existe el ítem ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'item': item}

    if request.method == 'POST':
        cotizacion = ConteoCotizaciones(
            usuario=request.user,
            item=item,
            tipo=tipo
        )
        cotizacion.save()
        return HttpResponse(item.categoria.categoria_alianzas)

    return render(request, template_name, contexto)


class BusquedaDetalle(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item, medida):
        detalle = get_object_or_404(DetalleItems, id_item_id=item,
                                    id_detalle_item=medida)
        # print(item)
        # print(medida)
        data = DetallesSerializer(detalle).data
        return Response(data)


class BusquedaDetallePiedra(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id_detalle):
        detalle = get_object_or_404(DetallePiedras,
                                    id_detalle_piedra=id_detalle)
        data = DetallePiedraSerializer(detalle).data
        return Response(data)


class ObtenerCostoColorProveedor(APIView):
    def get(self, request, id_color, id_proveedor):
        costo_color = ColoresProveedor.objects.filter(
            color_id=id_color,
            proveedor_id=id_proveedor
        ).first()
        return Response({'costo': costo_color.costo_adicional})


# ADAPTACION BRASIL ##############################


class AcabadosListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_acabados"
    model = Acabados
    template_name = "ctg/acabados_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return Acabados.objects.filter(taller_id=self.request.user.taller())


class AcabadosCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_acabados"
    model = Acabados
    template_name = "ctg/acabados_form.html"
    form_class = AcabadosForm
    success_url = reverse_lazy("ctg:acabados_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/acabados_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})

    def get_context_data(self, **kwargs):
        context = super(AcabadosCrearView, self).get_context_data(**kwargs)
        context['tipos'] = TiposCatalogo.objects.all()
        return context


class AcabadosEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_acabados"
    model = Acabados
    template_name = "ctg/acabados_form.html"
    context_object_name = "obj"
    form_class = AcabadosForm
    success_url = reverse_lazy("ctg:acabados_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_modifica = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/acabados_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


@login_required(login_url='/login/')
@permission_required('ctg.change_acabados',
                     login_url='bases:sin_permisos')
def ActualizarAcabadoModal(request, pk):
    template_name = 'ctg/actualizar_acabados_modal.html'
    contexto = {}
    acabado = Acabados.objects.filter(pk=pk).first()

    if not acabado:
        return HttpResponse('No existe el acabado ' + str(pk))

    if request.method == 'GET':
        contexto = {'acabado': acabado}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        acabado.estado = estado
        acabado.save()
        return HttpResponse('Acabado actualizado')

    return render(request, template_name, contexto)


class PartesInternasListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_partesinternas"
    model = PartesInternas
    template_name = "ctg/partes_internas_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return PartesInternas.objects.\
            filter(taller_id=self.request.user.taller())


class PartesInternasCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_partesinternas"
    model = PartesInternas
    template_name = "ctg/partes_internas_form.html"
    form_class = PartesInternasForm
    success_url = reverse_lazy("ctg:partes_internas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/partes_internas_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


class PartesInternasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_partesinternas"
    model = PartesInternas
    template_name = "ctg/partes_internas_form.html"
    context_object_name = "obj"
    form_class = PartesInternasForm
    success_url = reverse_lazy("ctg:partes_internas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_modifica = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/partes_internas_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


@login_required(login_url='/login/')
@permission_required('ctg.change_partesinternas',
                     login_url='bases:sin_permisos')
def ActualizarParteInternaModal(request, pk):
    template_name = 'ctg/actualizar_partes_internas_modal.html'
    contexto = {}
    parte_interna = PartesInternas.objects.filter(pk=pk).first()

    if not parte_interna:
        return HttpResponse('No existe la parte interna ' + str(pk))

    if request.method == 'GET':
        contexto = {'parte_interna': parte_interna}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        parte_interna.estado = estado
        parte_interna.save()
        return HttpResponse('Parte interna actualizado')

    return render(request, template_name, contexto)


class AnchurasListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_anchuras"
    model = Anchuras
    template_name = "ctg/anchuras_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return Anchuras.objects.filter(taller_id=self.request.user.taller())


class AnchurasCrearView(SinPermisos, generic.CreateView):
    permission_required = "ctg.add_anchuras"
    model = Anchuras
    template_name = "ctg/anchuras_form.html"
    form_class = AnchurasForm
    success_url = reverse_lazy("ctg:anchuras_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_crea = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/anchuras_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})

    def form_invalid(self, form):
        print(form.errors)
        return form.errors


class AnchurasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ctg.change_anchuras"
    model = Anchuras
    template_name = "ctg/anchuras_form.html"
    context_object_name = "obj"
    form_class = AnchurasForm
    success_url = reverse_lazy("ctg:anchuras_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        taller_obj = self.request.user.taller()
        form.instance.usuario_modifica = self.request.user.id
        form.instance.taller_id = taller_obj.id_taller
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "ctg/anchuras_form.html",
                          {'mensaje': e.__cause__,
                           'form': form})


@login_required(login_url='/login/')
@permission_required('ctg.change_acabados',
                     login_url='bases:sin_permisos')
def ActualizarAnchurasModal(request, pk):
    template_name = 'ctg/actualizar_anchuras_modal.html'
    contexto = {}
    anchura = Anchuras.objects.filter(pk=pk).first()

    if not anchura:
        return HttpResponse('No existe la anchura ' + str(pk))

    if request.method == 'GET':
        contexto = {'anchura': anchura}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        anchura.estado = estado
        anchura.save()
        return HttpResponse('Anchura actualizada')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
def AlianzasCrearView(request):
    template_name = 'ctg/alianzas_crear.html'
    contexto = {}

    categorias = Categorias.objects.filter(
        division__taller=request.user.taller(),
        categoria_alianzas=True
    )
    acabados = Acabados.objects.filter(
        taller=request.user.taller()
    )

    anchuras = Anchuras.objects.filter(
        taller=request.user.taller()
    )

    partes_internas = PartesInternas.objects.filter(
        taller=request.user.taller()
    )

    tallas = Tallas.objects.filter(
        taller=request.user.taller()
    )

    colores = Colores.objects.filter(
        taller=request.user.taller()
    )

    peso_max_img = ConfiguracionSistema.objects.\
        filter(clave='PESO_MAX_IMAGEN').first()
    ext_perm_img = ConfiguracionSistema.objects.\
        filter(clave='EXT_PERMITIDAS_IMAGEN').first()
    proveedores = Proveedores.objects.\
            filter(taller= request.user.taller().id_taller)
    if request.method == 'GET':
        contexto = {
            'form': ItemsForm,
            'categorias': categorias,
            'acabados': acabados,
            'anchuras': anchuras,
            'partes_internas': partes_internas,
            'tallas': tallas,
            'colores': colores,
            'peso_max_img': peso_max_img,
            'ext_perm_img': ext_perm_img,
            'proveedores': proveedores
        }

    if request.method == 'POST':
        imagenes = request.FILES.getlist('imagen')
        sku = request.POST['sku']
        categoria = request.POST['categoria']
        categoria = Categorias.objects.\
            filter(id_categoria=categoria).first()
        descripcion = request.POST['descripcion']
        costo_taller = request.POST['costo']
        prct_utilidad_taller = request.POST['utilidad']
        precio_taller = request.POST['precio']
        talla_minima_a = int(request.POST['talla_minima_a'])
        talla_maxima_a = int(request.POST['talla_maxima_a'])
        talla_minima_b = int(request.POST['talla_minima_b'])
        talla_maxima_b = int(request.POST['talla_maxima_b'])
        longitud_inscripcion = int(request.POST['longitud_inscripcion'])
        tmp_ent_min = request.POST['tiempo_entrega_min']
        if tmp_ent_min == '':
            tmp_ent_min = 0
        tmp_ent_max = request.POST['tiempo_entrega_max']
        if tmp_ent_max == '':
            tmp_ent_max = 0
        id_proveedor = int(request.POST['proveedor'])
        if id_proveedor == 0:
            id_proveedor = None
        datos_extras = request.POST['datos_extras']
        if datos_extras:
            if datos_extras == 'true':
                datos_extras = True
            else:
                datos_extras = False
        else:
            datos_extras = None
        piezas = request.POST.getlist('piezas[]')
        piezas = json.loads(piezas[0])
        colores_lista = request.POST.getlist('coloresDisponibles[]')
        colores_lista = json.loads(colores_lista[0])
        acabados_lista = request.POST.getlist('acabadosDisponibles[]')
        acabados_lista = json.loads(acabados_lista[0])
        cantidad_piedras = request.POST['cantidad_piedras']
        infoItem = Items(
            sku=sku,
            descripcion=descripcion,
            tipo_catalogo=categoria.division.tipo_catalogo,
            taller=categoria.division.taller,
            categoria=categoria,
            costo_taller=costo_taller,
            precio_taller=precio_taller,
            prct_utilidad_taller=prct_utilidad_taller,
            prct_utilidad_empresa=0,
            tiempo_entrega_min=tmp_ent_min,
            tiempo_entrega_max=tmp_ent_max,
            datos_extra=datos_extras,
            id_proveedor=id_proveedor,
            usuario_crea=request.user.id,
            unidad_medida=categoria.unidad_medida,

        )
        if infoItem:
            try:
                infoItem.save()
            except IntegrityError as e:
                return JsonResponse(
                    {'mensaje': str(e.__cause__)},
                    status=500)
            # infoDetalle = DetalleItems(
            #     medida=0,
            #     estandar='AMERICANO',
            #     peso_minimo=0,
            #     peso_maximo=0,
            #     cantidad_piedras=0,
            #     id_item_id=infoItem.id_item,
            #     usuario_crea=request.user.id
            # )
            # if infoDetalle:
            #     infoDetalle.save()
            
        for imagen in imagenes:
            infoImg = ItemsImagenes(
                usuario_crea=request.user.id,
                imagen=imagen,
                item=infoItem,
                taller=infoItem.taller
            )
            if infoImg:
                infoImg.save()

        colores_item = ItemsColores.objects.\
            filter(item=infoItem)
        if colores_item:
            for color_item in colores_item:
                color_item.delete()

        for color in colores_lista:
            infoColor = ItemsColores(
                color_id=color,
                item=infoItem,
                usuario_crea=request.user.id
            )
            if infoColor:
                try:
                    infoColor.save()
                except IntegrityError as e:
                    print(str(e.__cause__))

        infoPieza = Piezas(
            sku=infoItem.sku,
            talla_minima_a=talla_minima_a,
            talla_maxima_a=talla_maxima_a,
            talla_minima_b=talla_minima_b,
            talla_maxima_b=talla_maxima_b,
            longitud_inscripcion=longitud_inscripcion,
            item=infoItem,
            taller=infoItem.taller,
            usuario_crea=request.user.id
        )
        if infoPieza:
            try:
                infoPieza.save()
            except IntegrityError as e:
                print(str(e.__cause__))

        for acabado in acabados_lista:
            infoAcabado = PiezasAcabados(
                pieza=infoPieza,
                acabado_id=acabado,
                usuario_crea=request.user.id
            )
            if infoAcabado:
                try:
                    infoAcabado.save()
                except IntegrityError as e:
                    print(str(e.__cause__))

        for pieza_detalle in piezas:
            parte_interna_id = pieza_detalle.get('id_confort')
            anchura_id = pieza_detalle.get('id_anchura')
            pesos = pieza_detalle.get('pesos')
            for peso_detalle in pesos:
                peso = peso_detalle.get('peso')
                infoPiezaDetalle = PiezasDetalles(
                    parte_interna_id=parte_interna_id,
                    anchura_id=anchura_id,
                    peso=peso,
                    pieza=infoPieza,
                    usuario_crea=request.user.id
                )
                if infoPiezaDetalle:
                    try:
                        infoPiezaDetalle.save()
                    except IntegrityError as e:
                        print(str(e.__cause__))
                piedras = peso_detalle.get('piedras')
                for piedra in piedras:
                    medida = piedra.get('medida')
                    piedra_sku = piedra.get('sku')
                    piedra_cantidad = piedra.get('cantidad')
                    piedra_detalle = DetallePiedras.objects.filter(
                        medida=medida,
                        taller=infoItem.taller,
                        piedra__sku=piedra_sku
                    ).first()
                    infoPiezaPiedra = PiezasPiedras(
                        detalle_pieza=infoPiezaDetalle,
                        detalle_piedra=piedra_detalle,
                        cantidad=piedra_cantidad,
                        usuario_crea=request.user.id
                    )
                    if infoPiezaPiedra:
                        try:
                            infoPiezaPiedra.save()
                        except IntegrityError as e:
                            print(str(e.__cause__))
        # return HttpResponse('Anchura actualizada')

    return render(request, template_name, contexto)



@login_required(login_url='/login/')
def eliminar_alianzas(request):
    '''aliminar la alianza.
    en caso de tener una orden relacionada a la alianza,
    se emite una alerta'''
    if request.is_ajax and request.method == "GET":
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        alianza=request.GET.get('alianza', None)
        if alianza:
            try:
                alianza_obj = PiezasDetalles.objects.filter(pieza__sku=alianza).first()
                pieza_obj = Piezas.objects.filter(id_pieza=alianza_obj.pieza_id).first()
                item_obj = Items.objects.filter(id_item=pieza_obj.item_id).first()
                ordenes_alianza = DetalleOrden.objects.filter(id_item=item_obj.id_item).exists()
                if ordenes_alianza:
                    estado = 2
                else:
                    alianza_item = PiezasDetalles.objects.filter(pieza__sku=alianza).delete()
                    piezas_piedras_obj = PiezasPiedras.objects.filter(detalle_pieza=alianza_obj).delete()
                    piezas_acabados = PiezasAcabados.objects.filter(pieza__sku=alianza).delete()
                    pieza_obj = Piezas.objects.filter(sku=alianza).delete()
                    item_obj = Items.objects.filter(sku=alianza, categoria__categoria_alianzas=True).delete()
                    estado=1
            except PiezasDetalles.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
                
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)




@login_required(login_url='/login/')
def eliminar_detalle_alianza(request):
    
    if request.is_ajax and request.method == "GET":
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        item=request.GET['id']
        # parte_interna=int(request.GET['parte_interna'])
        # anchura = int(request.GET['anchura'])
        detalles = request.GET.get('detalles')
        detalles_id = json.loads(detalles)
        print(item)
        if item:
            lista_resultado = []
            for detalle in detalles_id:
                # print(detalle.get('id'))
                detalle_orden = DetalleOrden.objects.filter(id_pieza_detalle=detalle.get('id')).exists()
                lista_resultado.append(str(detalle_orden))
        
            if 'True' in lista_resultado:
                estado=2
            else:
                print(detalles, 'detalles')
                if len(detalles_id) == 0:
                    estado = 1
                else:
                    piezas_piedras = PiezasPiedras.objects.filter(detalle_pieza_id=detalle.get('id'))
                    for piedra in piezas_piedras:
                        piedra.delete()
                    pieza_detalle = PiezasDetalles.objects.filter(id_pieza_detalle=detalle.get('id'))
                    pieza_detalle.delete()

                    estado=1
        else:
            estado=0
            
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)




# eliminar detallede alianza de acuerdo al id que se envia  por GET
@login_required(login_url='/login/')
def eliminar_un_detalle(request):
    
    if request.is_ajax and request.method == "GET":
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        detalle=request.GET['id']
        item = request.GET['item']        
        if detalle:
            detalle_orden = DetalleOrden.objects.filter(id_pieza_detalle=detalle).exists()
            if detalle_orden:
                estado=2
            else:
                piedras_relacionadas = PiezasPiedras.objects.filter(detalle_pieza_id=detalle)
                for piedra in piedras_relacionadas:
                    piedra.delete()
                pieza_detalle = PiezasDetalles.objects.filter(id_pieza_detalle=detalle).first()
                pieza_detalle.delete()

                estado=1
        else:
            estado=0
            
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)





@login_required(login_url='/login/')
def eliminar_piedra_detalle(request):
    
    if request.is_ajax and request.method == "GET":
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        piedra=request.GET['id']
        item = request.GET['id_item']

        if piedra:
            try:
                pieza_piedra = PiezasPiedras.objects.filter(id_pieza_piedra=piedra).first()
                detalle_orden =  DetalleOrden.objects.filter(id_pieza_detalle=pieza_piedra.detalle_pieza_id).exists()
                if detalle_orden:
                    estado=2
                else:
                    try:
                        pieza_piedra = PiezasPiedras.objects.filter(id_pieza_piedra=piedra).first()
                        pieza_piedra.delete()
                        estado =1
                    except PiezasPiedras.DoesNotExist:
                        estado=0
                        return HttpResponseRedirect('/')

            except PiezasPiedras.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
                
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)

    




@login_required(login_url='/login/')
def eliminar_item(request):
    '''
        aliminar la alianza.
        en caso de tener una orden relacionada a la alianza,
        se emite una alerta
    '''
    if request.is_ajax and request.method == "GET":
        # usuario = get_object_or_404(Usuarios, id=request.user.id)
        item=request.GET.get('item', None)

        if item:
            try:
                item_obj = Items.objects.filter(sku=item).first()
                ordenes = DetalleOrden.objects.filter(id_item=item_obj.id_item).exists()
                solicitudes = DetalleSolicitud.objects.filter(item_id=item_obj.id_item).exists()

                if ordenes or solicitudes:
                    estado = 2
                else:
                    alianza_item = Items.objects.filter(sku=item).delete()
                    estado=1
            except Items.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
                
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)




# obtener las piedras relacionadas con las alianzas
@login_required(login_url='/login/')
def obtener_piedras(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        item_id = request.GET.get('item_id', None)
        colores_html = ""
        lista_color = []
        lista_color2 = []
        if item_id:
            try:
                colores_item = ItemsColores.objects.filter(item_id=item_id)
                for color in colores_item:
                    li_lista = '<li class="select2-selection__choice" title="'+color.color.descripcion+'">'+\
                                '<span class="select2-selection__choice__remove" role="presentation">×'+\
                                '</span>'+color.color.descripcion+'</li>'
                    lista_color.append(color.color_id)
                    lista_color2.append(color.color.descripcion)
                    colores_html=colores_html+li_lista
                estado = 1
            except ItemsColores.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado=0
        return JsonResponse({'estado': estado, 'color_id': lista_color, 'color_descripcion': lista_color2, 'colores_html': colores_html}, safe=False)
    return JsonResponse({}, statud=400)       
           
                
            
# obtener los acabados que se relacionen con las piezas de la alianza
@login_required(login_url='/login/')
def obtener_acabados(request):

    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        item_id = request.GET.get('item_id', None)
        acabados_html = ""
        lista_acabado = []
        if item_id:
            try:
                estado = 1
                pieza_id = Piezas.objects.filter(item_id=item_id).values('id_pieza')
                acabados_pieza = PiezasAcabados.objects.filter(pieza_id__in=pieza_id)
                for acabado in acabados_pieza:
                    li_lista_acabados = '<li class="select2-selection__choice" title="'+acabado.acabado.descripcion+'">'+\
                                '<span class="select2-selection__choice__remove" role="presentation">×'+\
                                '</span>'+acabado.acabado.descripcion+'</li>'
                    lista_acabado.append(acabado.acabado_id)
                    acabados_html=acabados_html+li_lista_acabados
                
            except PiezasAcabados.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado=0
        return JsonResponse({'estado': estado, 'acabados_id': lista_acabado, 'acabados_html': acabados_html}, safe=False) 
    return JsonResponse({}, statud=400)    


@login_required(login_url='/login/')
def AlianzasEditarView(request, id_item):
    template_name = 'ctg/alianzas_editar.html'
    contexto = {}

    item = Items.objects.filter(
        id_item=id_item
    ).first()
    imagenes_alianza = ItemsImagenes.objects.filter(
        item_id=id_item
    )

    pieza = Piezas.objects.filter(
        item=item
    ).first()

    categorias = Categorias.objects.filter(
        division__taller=request.user.taller(),
        categoria_alianzas=True
    )

    acabados = Acabados.objects.filter(
        taller=request.user.taller()
    )

    anchuras = Anchuras.objects.filter(
        taller=request.user.taller()
    )

    partes_internas = PartesInternas.objects.filter(
        taller=request.user.taller()
    )

    tallas = Tallas.objects.filter(
        taller=request.user.taller()
    )

    colores = Colores.objects.filter(
        taller=request.user.taller()
    )
    lista_colores = []
    colores_asignados = ItemsColores.objects.filter(item_id=item.id_item)
    for color in colores_asignados:
        lista_colores.append(color.color_id)
    
    lista_acabados = []
    acabados_asignados = PiezasAcabados.objects.filter(pieza_id=pieza.id_pieza)
    for acabado in acabados_asignados:
        lista_acabados.append(acabado.acabado_id)

    # detalle de las piezas
    # detalle_piezas = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza)
    lista_parte = []
    partes_internas_relacionadas = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza)
    for parte in partes_internas_relacionadas:
        lista_parte.append(parte.parte_interna_id)
    
    lista_anchura = []
    anchuras_relacionadas = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza)
    for parte in partes_internas_relacionadas:
        lista_anchura.append(parte.anchura_id)

    lista_proveedores = []
    proveedores_relacionados = Proveedores.objects.\
        filter(
            taller=item.taller_id,
            id=item.id_proveedor
        )
    # print(proveedores_relacionados)

    for proveedor in proveedores_relacionados:
        lista_proveedores.append(proveedor.id)
    
    pesos = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza).values('peso', 'id_pieza_detalle')
    # for i in pesos:
    #     piedras_piezas = 
    pesos = PiezasDetallesPesosSerializer(pesos, many=True).data 
    pesos = json.dumps(pesos)

    # print(pesos)
    # piedras_pieza
    pieza_detalle = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza).values('id_pieza_detalle')
    # print(pieza_detalle)
    piedras_pieza = PiezasPiedras.objects.filter(detalle_pieza_id__in=pieza_detalle)
    # print(piedras_pieza)
    piedras_pieza = PiezasPiedrasItemSerializer(piedras_pieza, many=True).data
    # print(piedras_pieza, 'serializer')
    piedras_pieza = json.dumps(piedras_pieza)

    piezas_detalles = PiezasDetalles.objects.filter(pieza_id=pieza.id_pieza)

    combinaciones = PiezasDetalles.objects.filter(
        pieza_id=pieza.id_pieza
    ).\
    order_by(
        'anchura_id'
    ).\
    values(
        'anchura_id',
        'parte_interna_id',
    ).distinct()

    combinaciones = combinaciones.distinct()
    print(combinaciones)

    lista = []
    for combinacion in combinaciones:
        detalle = {
            # 'id_detalle': combinacion.get('id_pieza_detalle'),
            'anchura_id': combinacion.get('anchura_id'),
            'parte_interna_id': combinacion.get('parte_interna_id'),
            'pesos': []
        }
        lista.append(detalle)
        pesos = PiezasDetalles.objects.filter(
            pieza_id=pieza.id_pieza,
            anchura_id=combinacion.get('anchura_id'),
            parte_interna_id=combinacion.get('parte_interna_id')
        ).values('peso', 'id_pieza_detalle')
        print(pesos)
        for peso in pesos:
            piedras = PiezasPiedras.objects.filter(
                detalle_pieza_id=str(peso.get('id_pieza_detalle'))
            )
            detalle_peso = {
                'id_detalle': peso.get('id_pieza_detalle'),
                'peso': str(peso.get('peso')),
                'piedras': []
            }
            detalle.get('pesos').append(detalle_peso)
            piedras = PiezasPiedrasItemSerializer(piedras, many=True).data
            for piedra in piedras:
                detalle_piedra = {
                    'id_pieza_piedra': piedra.get('id_pieza_piedra'),
                    'sku': piedra.get('sku'),
                    'descripcion': piedra.get('descripcion'),
                    'puntos': piedra.get('puntos'),
                    'cantidad': piedra.get('cantidad')
                }
                detalle_peso.get('piedras').append(detalle_piedra)
    # print(lista)



    peso_max_img = ConfiguracionSistema.objects.\
        filter(clave='PESO_MAX_IMAGEN').first()
    ext_perm_img = ConfiguracionSistema.objects.\
        filter(clave='EXT_PERMITIDAS_IMAGEN').first()

    if request.method == 'GET':
        contexto = {
            'form': ItemsForm,
            'categorias': categorias,
            'acabados': acabados,
            'acabados_asignados': lista_acabados,
            'anchuras': anchuras,
            'anchura_relacionada': lista_anchura,
            'partes_internas': partes_internas,
            'partes_relacionadas': lista_parte,
            'tallas': tallas,
            'colores': colores,
            'colores_asignados': lista_colores,
            'peso_max_img': peso_max_img,
            'ext_perm_img': ext_perm_img,
            'item': item,
            'imagenes_alianza': imagenes_alianza,
            'pieza': pieza,
            'pesos': pesos,
            'piedras_pieza': piedras_pieza,
            'lista_detalle': lista,
            'proveedores': Proveedores.objects.filter(taller=request.user.taller().id_taller),
            'proveedor_relacionado': lista_proveedores
        }

    if request.method == 'POST':
        imagenes = request.FILES.getlist('imagen')
        sku = request.POST['sku']
        categoria = request.POST['categoria']
        categoria = Categorias.objects.\
            filter(id_categoria=categoria).first()
        descripcion = request.POST['descripcion']
        costo_taller = request.POST['costo']
        prct_utilidad_taller = request.POST['utilidad']
        precio_taller = request.POST['precio']
        

        talla_minima_a = int(request.POST['talla_minima_a'])
        talla_maxima_a = int(request.POST['talla_maxima_a'])
        talla_minima_b = int(request.POST['talla_minima_b'])
        talla_maxima_b = int(request.POST['talla_maxima_b'])
        longitud_inscripcion = int(request.POST['longitud_inscripcion'])
        tmp_ent_min = request.POST['tiempo_entrega_min']
        if tmp_ent_min == '':
            tmp_ent_min = 0
        tmp_ent_max = request.POST['tiempo_entrega_max']
        if tmp_ent_max == '':
            tmp_ent_max = 0
        # print('********')
        # print(tmp_ent_min)
        # print(tmp_ent_max)
        # print('***********')

        # print(categoria)
        id_proveedor = None
        if categoria.proveedor:
            id_proveedor = request.POST['proveedor']
        
        datos_extras = request.POST['datos_extras']
        if datos_extras:
            if datos_extras == 'true':
                datos_extras = True
            else:
                datos_extras = False
        else:
            datos_extras = None
        piezas = request.POST.getlist('piezas[]')
        # print(piezas)
        piezas = json.loads(piezas[0])
        colores_lista = request.POST.getlist('coloresDisponibles[]')
        colores_lista = json.loads(colores_lista[0])
        acabados_lista = request.POST.getlist('acabadosDisponibles[]')
        acabados_lista = json.loads(acabados_lista[0])

        try:
            producto = Items.objects.filter(id_item=id_item).first()
            producto.descripcion = descripcion
            producto.tipo_catalogo_id=categoria.division.tipo_catalogo_id
            producto.taller_id=categoria.division.taller_id
            producto.categoria_id=categoria.id_categoria
            producto.costo_taller=(costo_taller)
            producto.precio_taller=(precio_taller)
            producto.prct_utilidad_taller=prct_utilidad_taller
            producto.tiempo_entrega_min=tmp_ent_min
            producto.tiempo_entrega_max=tmp_ent_max
            producto.datos_extra=datos_extras
            producto.id_proveedor=id_proveedor
            producto.usuario_modifica=request.user.id
            producto.fecha_modificacion = datetime.now(timezone.utc)
            producto.save()
            
            imagenes_relacionadas = ItemsImagenes.objects.filter(item_id=producto.id_item)
            for img in imagenes_relacionadas:
                if len(imagenes) > 0:
                    img.delete()
            for imagen in imagenes:
                infoImg = ItemsImagenes(
                    usuario_crea=request.user.id,
                    imagen=imagen,
                    item=producto,
                    taller=producto.taller
                )
                if infoImg:
                    infoImg.save()

            colores_item = ItemsColores.objects.\
                filter(item=producto)
            for color_item in colores_item:
                color_item.delete()
            for color in colores_lista:
                infoColor = ItemsColores(
                    color_id=color,
                    item=producto,
                    usuario_crea=request.user.id,
                    usuario_modifica=request.user.id
                )
                if infoColor:
                    infoColor.save()
            
            pieza_actual = Piezas.objects.get(item_id=id_item)
            # pieza_actual.sku=producto.sku,
            pieza_actual.talla_minima_a=talla_minima_a
            pieza_actual.talla_maxima_a=talla_maxima_a
            pieza_actual.talla_minima_b=talla_minima_b
            pieza_actual.talla_maxima_b=talla_maxima_b
            pieza_actual.item_id=producto
            pieza_actual.longitud_inscripcion=longitud_inscripcion
            pieza_actual.save()

            acabados_pieza = PiezasAcabados.objects.filter(pieza_id=pieza_actual.id_pieza)
            for acabadop in acabados_pieza:
                acabadop.delete()
            for acabado in acabados_lista:
                infoAcabado = PiezasAcabados(
                    pieza=pieza_actual,
                    acabado_id=acabado,
                    usuario_crea=request.user.id
                )
                if infoAcabado:
                    infoAcabado.save()
            '''
                Metodo utilizado para eliminar los detalles,
                 y agregar los nuevos datos traidos del template 
            '''

            # pieza_detalles = PiezasDetalles.objects.filter(pieza=pieza_actual)
            # if pieza_detalles:
            #     for detalle in pieza_detalles:
            #         print(detalle)
            #         piedras_piezas = PiezasPiedras.objects.filter(detalle_pieza_id=detalle.id_pieza_detalle)
            #         for p in piedras_piezas:
            #             p.delete()
            #         detalle.delete()


            detalles_anteriores = PiezasDetalles.objects.filter(pieza_id=pieza_actual.id_pieza).values('id_pieza_detalle')
            lista_anterior = []
            for detalle in detalles_anteriores:
                lista_anterior.append(str(detalle.get('id_pieza_detalle')))

            lista_actual = []
            for pieza_detalle in piezas:
                anchura= pieza_detalle.get('id_anchura')
                parte_interna = pieza_detalle.get('id_confort')
                for peso in pieza_detalle.get('pesos'):
                    lista_actual.append(peso.get('id_detalle'))
                    if peso.get('id_detalle') != '':
                        detalle_obj = PiezasDetalles.objects.filter(id_pieza_detalle=peso.get('id_detalle')).first();
                        detalle_obj.anchura_id=int(anchura)
                        detalle_obj.parte_interna_id=int(parte_interna)
                        detalle_obj.peso = peso.get('peso')
                        detalle_obj.save()
                        for piedra in peso.get('piedras'):
                            if piedra.get('id_pieza_piedra') != '':
                                piedra_obj = PiezasPiedras.objects.filter(id_pieza_piedra=piedra.get('id_pieza_piedra')).first()
                                piedra_obj.cantidad = piedra.get('cantidad')
                                piedra_obj.save()
                            else:
                                piedra_obj = Piedras.objects.filter(sku=piedra.get('sku'), descripcion=piedra.get('piedra')).first()
                                detalle_piedra = DetallePiedras.objects.filter(piedra_id=piedra_obj.id_piedra, medida=piedra.get('medida')).first()
                                infoPiedra = PiezasPiedras(
                                    cantidad = piedra.get('cantidad'),
                                    detalle_pieza_id = peso.get('id_detalle'),
                                    detalle_piedra_id= detalle_piedra.id_detalle_piedra,
                                    usuario_crea = request.user.id
                                )
                                try:
                                    infoPiedra.save()
                                except IntegrityError as e:
                                    return JsonResponse(
                                        {'mensaje': str('Ya existe un piedra con la misma medida.')}, status=500)
                    else:
                        
                        infoPiezaDetalle = PiezasDetalles(
                            peso=peso.get('peso'),
                            anchura_id=int(anchura),
                            parte_interna_id=int(parte_interna),
                            estado_id=1,
                            pieza_id=pieza_actual.id_pieza,
                            usuario_crea=request.user.id
                        )
                        infoPiezaDetalle.save()
                        for piedra in peso.get('piedras'):
                            if piedra.get('id_pieza_piedra') == '':
                                piedra_obj = Piedras.objects.filter(sku=piedra.get('sku')).first()
                                detalle_piedra = DetallePiedras.objects.filter(piedra_id=piedra_obj.id_piedra, medida=piedra.get('medida') ).first()
                                infoPiedra = PiezasPiedras(
                                    cantidad = piedra.get('cantidad'),
                                    detalle_pieza_id = infoPiezaDetalle.id_pieza_detalle,
                                    detalle_piedra_id= detalle_piedra.id_detalle_piedra,
                                    usuario_crea = request.user.id
                                )
                                infoPiedra.save()


            for detalle in lista_anterior:
                if not detalle in lista_actual:
                    ''' consultar si el detalle esta relacionado alguna orden antes de eliminar'''
                    detalle_obj = PiezasDetalles.objects.filter(id_pieza_detalle=detalle).first()
                    detalle_obj.delete()

            return HttpResponse('ok')
        except Items.DoesNotExist:
             return HttpResponseRedirect('/')
        
    return render(request, template_name, contexto)


class PiedrasAgregarModalListaView(SinPermisos, generic.ListView):
    permission_required = "ctg.view_piedras"
    model = Piedras
    template_name = "ctg/piedra_agregar_lista_modal.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return Piedras.objects.\
            filter(taller_id=self.request.user.taller())


class PiedrasListaApi(APIView):
    def get(self, request):
        piedras = Piedras.objects.\
            filter(taller_id=self.request.user.taller())
        data = PiedrasSerializer(piedras, many=True).data
        return Response(data)


class DetallePiedraApi(APIView):
    def get(self, request, id_piedra):
        piedra = Piedras.objects.\
            filter(id_piedra=id_piedra).first()
        detalles = DetallePiedras.objects.\
            filter(piedra=piedra)
        piedra = PiedrasSerializer(piedra).data
        detalles = DetallesPiedraSerializer(detalles, many=True).data
        return JsonResponse(
            {
                'piedra': piedra,
                'detalles': detalles
            })


@login_required(login_url='/login/')
@permission_required('ctg.view_piedras',
                     login_url='bases:sin_permisos')
def PiedraAgregarAItemView(request, id_piedra=None):
    template_name = "ctg/piedra_agregar_a_item_modal.html"
    form_item = {}
    contexto = {}

    if request.method == 'GET':
        piedra = Piedras.objects.filter(id_piedra=id_piedra).first()
        detalles_piedra = DetallePiedras.objects.\
            filter(piedra_id=piedra.id_piedra, estado_id=1)
        # config = ConfigUtilidadTaller.objects.filter(
        #     id_taller=piedra.taller_id,
        #     id_usuario_op=request.user.id
        # ).first()
        # if config:
        #     utilidad_fab_op = config.utilidad
        # else:
        #     utilidad_fab_op = request.user.config_gen.utilidad_sobre_taller

        contexto = {
            'piedra': piedra,
            'detalles_piedra': detalles_piedra,
            # 'id_orden': id_orden,
            # 'utilidad_fab_op': utilidad_fab_op
            }

    return render(request, template_name, contexto)


class AlianzasListaView(SinPermisos, generic.TemplateView):
    permission_required = "ctg.view_items"
    template_name = "ctg/alianzas_lista.html"
    login_url = "bases:login"

    def get_context_data(self, **kwargs):
        context = super(AlianzasListaView, self).get_context_data(**kwargs)
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            taller_obj = self.request.user.taller()
            talleres = None
            categorias = Categorias.objects.\
                filter(
                    categoria_alianzas=True,
                    division__taller=taller_obj
                    )
        else:
            talleres = Talleres.objects.\
                filter(pais=self.request.user.pais)
            categorias = Categorias.objects.\
                filter(
                    estado__descripcion='ACTIVO',
                    categoria_alianzas=True,
                    division__taller__pais=self.request.user.pais
                    )
        context['categorias'] = categorias
        context['talleres'] = talleres
        return context


class BusquedaAlianzasApiView(APIView):
    def post(self, request):
        # talleres = self.request.POST['talleresBusqueda[]']
        # talleres = json.loads(talleres)
        categorias = self.request.POST['categoriasBusqueda[]']
        categorias = json.loads(categorias)
        clave = self.request.POST['claveBusqueda']
        limite = int(self.request.POST['limite'])
        items1 = Items.objects.filter(
            descripcion__icontains=clave,
            categoria__categoria_alianzas=True,
            taller__pais=self.request.user.pais

        ) | Items.objects.filter(
            sku__icontains=clave,
            categoria__categoria_alianzas=True,
            taller__pais=self.request.user.pais

        )
        items2 = Items.objects.filter(
            # taller_id__in=talleres,
            categoria__categoria_alianzas=True,
            taller__pais=self.request.user.pais

        )
        items3 = Items.objects.filter(
            categoria_id__in=categorias,
            categoria__categoria_alianzas=True,
            taller__pais=self.request.user.pais

        )
        if self.request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
            items4 = Items.objects.filter(
                taller=self.request.user.taller(),
                categoria__categoria_alianzas=True,
                taller__pais=self.request.user.pais
            )
        else:

            items4 = Items.objects.filter(
                taller__pais=self.request.user.pais,
                categoria__categoria_alianzas=True,
                estado__descripcion='ACTIVO'
            )
        if clave == ''  and len(categorias) == 0:
            items = (items4).order_by('sku')[:limite]
        if clave == ''  and len(categorias) > 0:
            items = (items3).order_by('sku')[:limite]
        elif clave == '' and len(categorias) == 0:
            items = (items2).order_by('sku')[:limite]
        elif clave == '' and len(categorias) > 0:
            items = (items2 & items3).order_by('sku')[:limite]
        elif clave != ''  and len(categorias) == 0:
            items = (items4 & items1).order_by('sku')[:limite]
        elif clave != ''  and len(categorias) > 0:
            items = (items1 & items3).order_by('sku')[:limite]
        elif clave != '' and len(categorias) == 0:
            items = (items1 & items2).order_by('sku')[:limite]
        elif clave != '' and len(categorias) > 0:
            items = (items1 & items2 & items3).order_by('sku')[:limite]

        items_lista = []
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            for item in items:
                if item.estado_id == 1:
                    items_lista.append(item)
        else:
            for item in items:
                items_lista.append(item)

                    

        data = ItemsSerializer(items_lista, many=True).data
        print(len(data))
        return Response(data)


class BusquedaAnchuras(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pieza_id = int(self.request.POST['id_pieza'])
        pieza = Piezas.objects.filter(
            id_pieza=pieza_id
        ).first()
        parte_interna_id = int(self.request.POST['id_parte_interna'])
        parte_interna = PartesInternas.objects.filter(
            id_parte_interna=parte_interna_id
        ).first()
        anchuras_id = PiezasDetalles.objects.filter(
            pieza=pieza,
            parte_interna=parte_interna
        ).values('anchura').distinct()
        anchuras = Anchuras.objects.filter(
            id_anchura__in=anchuras_id
        )
        data = AnchurasSerializer(anchuras, many=True).data
        return Response(data)


class BusquedaPesos(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pieza_id = int(self.request.POST['id_pieza'])
        pieza = Piezas.objects.filter(
            id_pieza=pieza_id
        ).first()
        parte_interna_id = int(self.request.POST['id_parte_interna'])
        parte_interna = PartesInternas.objects.filter(
            id_parte_interna=parte_interna_id
        ).first()
        anchura_id = int(self.request.POST['id_anchura'])
        anchura = Anchuras.objects.filter(
            id_anchura=anchura_id
        ).first()
        pesos = PiezasDetalles.objects.filter(
            pieza=pieza,
            parte_interna=parte_interna,
            anchura=anchura
        )
        data = PiezasDetallesSerializer(pesos, many=True).data
        return Response(data)


class BusquedaPiedras(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pieza_detalle_id = int(self.request.POST['id_pieza_detalle'])
        pieza_detalle = PiezasDetalles.objects.filter(
            id_pieza_detalle=pieza_detalle_id
        ).first()
        piedras = PiezasPiedras.objects.filter(
            detalle_pieza=pieza_detalle
        )
        print(piedras)
        data = PiezasPiedrasSerializer(piedras, many=True).data
        return Response(data)
