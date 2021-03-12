from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse


from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, \
    permission_required
import json
import pytz

from .models import Regiones, Paises, Localidades, Ciudades
from .forms import RegionForm, PaisForm, LocalidadForm, ZonaForm,\
    CiudadForm, SectorForm
from bases.models import Estados
from cfg.models import ConfiguracionSistema, ConfiguracionApiSMS
from est.models import Zonas, Sectores, Tiendas, Ciudades
from bases.views import SinPermisos
from usr.models import Usuarios
from ubc.models import Localidades


class RegionesListaView(SinPermisos, generic.ListView):
    permission_required = "ubc.view_regiones"
    model = Regiones
    template_name = "ubc/regiones_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"


class RegionesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ubc.add_regiones"
    model = Regiones
    template_name = "ubc/regiones_form.html"
    context_object_name = "obj"
    form_class = RegionForm
    success_url = reverse_lazy("ubc:regiones_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)


class RegionesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ubc.change_regiones"
    model = Regiones
    template_name = "ubc/regiones_form.html"
    context_object_name = "obj"
    form_class = RegionForm
    success_url = reverse_lazy("ubc:regiones_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)


class PaisesListaView(SinPermisos, generic.ListView):
    permission_required = "ubc.view_paises"
    model = Paises
    template_name = "ubc/paises_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"


class PaisesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ubc.add_paises"
    model = Paises
    template_name = "ubc/paises_form.html"
    context_object_name = "obj"
    form_class = PaisForm
    success_url = reverse_lazy("ubc:paises_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        configuraciones_api = ConfiguracionApiSMS.objects.\
            values('clave').distinct()
        for configuracion in configuraciones_api:
            print(configuracion.get('clave'))
            infoConfig = ConfiguracionApiSMS(
                clave=configuracion.get('clave'),
                pais_id=self.object.id_pais
            )
            if infoConfig:
                infoConfig.save()
        return reverse('ubc:paises_lista')

    def get_context_data(self, **kwargs):
        context = super(PaisesCrearView, self).get_context_data(**kwargs)
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['zonas_horarias'] = pytz.common_timezones
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        return context


class PaisesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ubc.change_paises"
    model = Paises
    template_name = "ubc/paises_form.html"
    context_object_name = "obj"
    form_class = PaisForm
    success_url = reverse_lazy("ubc:paises_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaisesEditarView, self).get_context_data(**kwargs)
        peso_max_img = ConfiguracionSistema.objects.\
            filter(clave='PESO_MAX_IMAGEN').first()
        ext_perm_img = ConfiguracionSistema.objects.\
            filter(clave='EXT_PERMITIDAS_IMAGEN').first()
        context['zonas_horarias'] = pytz.common_timezones
        context['peso_max_img'] = peso_max_img
        context['ext_perm_img'] = ext_perm_img
        return context


class LocalidadesListaView(SinPermisos, generic.ListView):
    permission_required = "ubc.view_localidades"
    model = Localidades
    template_name = "ubc/localidades_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Localidades.objects.all()
        else:
            return Localidades.objects.\
                filter(pais_id=self.request.user.pais_id)
    
    

class LocalidadesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ubc.add_localidades"
    model = Localidades
    template_name = "ubc/localidades_form.html"
    context_object_name = "obj"
    form_class = LocalidadForm
    success_url = reverse_lazy("ubc:localidades_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(LocalidadesCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class LocalidadesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ubc.change_localidades"
    model = Localidades
    template_name = "ubc/localidades_form.html"
    context_object_name = "obj"
    form_class = LocalidadForm
    success_url = reverse_lazy("ubc:localidades_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(LocalidadesEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs




@login_required(login_url='/login/')
@permission_required('ubc.change_localidades',
                     login_url='bases:sin_permisos')
def ActualizarLocalidadModal(request, pk):
    template_name = 'ubc/actualizar_localidad_modal.html'
    contexto = {}
    localidad = Localidades.objects.filter(pk=pk).first()

    if not localidad:
        return HttpResponse('No existe la localidad ' + str(pk))

    if request.method == 'GET':
        contexto = {'localidad': localidad}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        localidad.estado = estado
        localidad.save()
        return HttpResponse('Localidad actualizada')

    return render(request, template_name, contexto)



@login_required(login_url='/login/')
@permission_required('ubc.change_localidades',
                     login_url='bases:sin_permisos')
def eliminar_localidad(request):

    if request.is_ajax and request.method == "GET":
        usuario =get_object_or_404(Usuarios,id=request.user.id)
        localidad = request.GET.get("localidad", None)
        
        if localidad:
            try:
                localidad_obj = Localidades.objects.filter(id_localidad=localidad).first()
                ciudad_localidad = Ciudades.objects.filter(localidad_id=localidad_obj.id_localidad).exists()
                if ciudad_localidad:
                    estado = 2
                else:
                    Localidades.objects.filter(id_localidad=localidad).delete()
                    estado = 1
            except Localidades.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)





class ZonasListaView(SinPermisos, generic.ListView):
    permission_required = "est.view_zonas"
    model = Zonas
    template_name = "ubc/zonas_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Zonas.objects.all()
        else:
            return Zonas.objects.filter(grupo_empresarial=self.request.user.grupo_empresarial())


class ZonasCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_zonas"
    model = Zonas
    template_name = "ubc/zonas_form.html"
    context_object_name = "obj"
    form_class = ZonaForm
    success_url = reverse_lazy("ubc:zonas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ZonasCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ZonasEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_zonas"
    model = Zonas
    template_name = "ubc/zonas_form.html"
    context_object_name = "obj"
    form_class = ZonaForm
    success_url = reverse_lazy("ubc:zonas_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ZonasEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('est.change_zonas',
                     login_url='bases:sin_permisos')
def ActualizarZonaModal(request, pk):
    template_name = 'ubc/actualizar_zona_modal.html'
    contexto = {}
    zona = Zonas.objects.filter(pk=pk).first()

    if not zona:
        return HttpResponse('No existe la zona ' + str(pk))

    if request.method == 'GET':
        contexto = {'zona': zona}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        zona.estado = estado
        zona.save()
        return HttpResponse('zona actualizada')

    return render(request, template_name, contexto)



@login_required(login_url='/login/')
# @permission_required('est.delete_zonas',
#                      login_url='bases:sin_permisos')
def eliminar_zona(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        zona = request.GET.get("zona", None)
        if zona:
            zona_obj = Zonas.objects.filter(id_zona=int(zona)).first()
            try:
                tienda_zona = Tiendas.objects.filter(zona_id=zona_obj.id_zona).first()
                if tienda_zona:
                    estado = 2
                    tienda = tienda_zona.nombre
                else:
                    tienda = ""
                    Zonas.objects.filter(id_zona=int(zona)).delete()
                    estado = 1
            except Zonas.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse(
            {
                "estado": estado,
                "tienda": tienda
            },
            safe=True,
        )
    return JsonResponse({}, status = 400)



class CiudadesListaView(SinPermisos, generic.ListView):
    permission_required = "ubc.view_ciudades"
    model = Ciudades
    template_name = "ubc/ciudades_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Ciudades.objects.all()
        else:
            return Ciudades.objects.\
                filter(pais_id=self.request.user.pais_id)


class CiudadesCrearView(SinPermisos, generic.CreateView):
    permission_required = "ubc.add_ciudades"
    model = Ciudades
    template_name = "ubc/ciudades_form.html"
    context_object_name = "obj"
    form_class = CiudadForm
    success_url = reverse_lazy("ubc:ciudades_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        localidad = self.request.POST.get("localidad")
        localidad = Localidades.objects.filter(pk=localidad).first()
        form.instance.pais_id = localidad.pais_id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CiudadesCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CiudadEditarView(SinPermisos, generic.UpdateView):
    permission_required = "ubc.change_ciudades"
    model = Ciudades
    template_name = "ubc/ciudades_form.html"
    context_object_name = "obj"
    form_class = CiudadForm
    success_url = reverse_lazy("ubc:ciudades_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CiudadEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('ubc.change_ciudades',
                     login_url='bases:sin_permisos')
def ActualizarCiudadModal(request, pk):
    template_name = 'ubc/actualizar_ciudad_modal.html'
    contexto = {}
    ciudad = Ciudades.objects.filter(pk=pk).first()

    if not ciudad:
        return HttpResponse('No existe la ciudad ' + str(pk))

    if request.method == 'GET':
        contexto = {'ciudad': ciudad}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        ciudad.estado = estado
        ciudad.save()
        return HttpResponse('ciudad actualizada')

    return render(request, template_name, contexto)


#eliminar ciudad

@login_required(login_url='/login/')
# @permission_required('ubc.delete_ciudades',
#                      login_url='bases:sin_permisos')
def eliminar_ciudad(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        ciudad = request.GET.get("ciudad", None)
        
        
        if ciudad:
            ciudad_obj = Ciudades.objects.filter(id_ciudad=int(ciudad)).first()
            try:
                tienda_ciudad = Tiendas.objects.filter(ciudad_id=ciudad_obj.id_ciudad).first()
                if tienda_ciudad:
                    estado = 2
                    tienda = tienda_ciudad.nombre
                else:
                    Ciudades.objects.filter(id_ciudad=int(ciudad)).delete()
                    estado = 1
                    tienda = ""
            except Ciudades.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse(
            {
                "estado": estado,
                "tienda": tienda
            }
        )
    return JsonResponse({}, status = 400)







class SectoresListaView(SinPermisos, generic.ListView):
    permission_required = "est.view_sectores"
    model = Sectores
    template_name = "ubc/sectores_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Sectores.objects.all()
        else:
            return Sectores.objects.filter(grupo_empresarial=self.request.user.grupo_empresarial())
            


class SectoresCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_sectores"
    model = Sectores
    template_name = "ubc/sectores_form.html"
    context_object_name = "obj"
    form_class = SectorForm
    success_url = reverse_lazy("ubc:sectores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(SectoresCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SectoresEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_sectores"
    model = Sectores
    template_name = "ubc/sectores_form.html"
    context_object_name = "obj"
    form_class = SectorForm
    success_url = reverse_lazy("ubc:sectores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(SectoresEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('est.change_sectores',
                     login_url='bases:sin_permisos')
def ActualizarSectorModal(request, pk):
    template_name = 'ubc/actualizar_sector_modal.html'
    contexto = {}
    sector = Sectores.objects.filter(pk=pk).first()

    if not sector:
        return HttpResponse('No existe el sector ' + str(pk))

    if request.method == 'GET':
        contexto = {'sector': sector}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        sector.estado = estado
        sector.save()
        return HttpResponse('sector actualizado')

    return render(request, template_name, contexto)



#eliminar sector

@login_required(login_url='/login/')
# @permission_required('ubc.delete_ciudades',
#                      login_url='bases:sin_permisos')
def eliminar_sector(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        sector = request.GET.get("sector", None)
        
        
        if sector:
            sector_obj = Sectores.objects.filter(id_sector=int(sector)).first()
            try:
                tienda_sector = Tiendas.objects.filter(sector_id=sector_obj.id_sector).first()
                if tienda_sector:
                    estado = 2
                else:
                    Sectores.objects.filter(id_sector=int(sector)).delete()
                    estado = 1
            except Sectores.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse(
            {
                "estado": estado
            }
        )
    return JsonResponse({}, status = 400)