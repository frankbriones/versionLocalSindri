from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import HttpResponseRedirect, resolve_url, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required


import json
from datetime import date
from datetime import datetime

from bases.views import SinPermisos
from usr.models import Usuarios, UsuariosTiendas, UsuariosGruposEmpresariales,\
                    UsuariosTalleres
from .models import GruposEmpresariales, Sociedades, \
    Tiendas, Talleres
from bases.models import Estados
from ubc.models import Paises, Ciudades
from est.models import Zonas, Sectores
from .forms import GrupoEmpresarialForm, SociedadForm, TiendaForm, \
    TallerForm


# class GruposEmpresarialesListaView(
#      SinPermisos, generic.ListView):
#     permission_required = "est.view_grupos_empresariales"
#     model = GruposEmpresariales
#     template_name = "est/grupos_empresariales_lista.html"
#     context_object_name = "obj"
#     login_url = "bases:login"

#     # def get_queryset(self):
#     #     return Roles.objects.filter(usuario_crea=self.request.user.id)

class GruposEmpresarialesListaView(SinPermisos, generic.ListView):
    model = GruposEmpresariales
    template_name = "est/grupos_empresariales_lista.html"
    permission_required = "est.view_gruposempresariales"
    context_object_name = "obj"
    login_url = "bases:login"

    # def get_queryset(self):
    #     return Roles.objects.filter(usuario_crea=self.request.user.id)


class GrupoEmpresarialCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_gruposempresariales"
    model = GruposEmpresariales
    template_name = "est/grupos_empresariales_form.html"
    success_url = reverse_lazy("est:grupos_empresariales_lista")
    form_class = GrupoEmpresarialForm

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GrupoEmpresarialCrearView, self).\
            get_context_data(**kwargs)
        context['paises'] = Paises.objects.all()
        return context


class GrupoEmpresarialEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_gruposempresariales"
    model = GruposEmpresariales
    template_name = "est/grupos_empresariales_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("est:grupos_empresariales_lista")
    form_class = GrupoEmpresarialForm

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GrupoEmpresarialEditarView, self).\
            get_context_data(**kwargs)
        context['paises'] = Paises.objects.all()
        return context


@login_required(login_url='/login/')
@permission_required('est.change_gruposempresariales',
                     login_url='bases:sin_permisos')
def ActualizarGrupoEmpresarialModal(request, pk):
    template_name = 'est/actualizar_grupo_modal.html'
    contexto = {}
    grupo_empresarial = GruposEmpresariales.objects.\
        filter(pk=pk).first()

    if not grupo_empresarial:
        return HttpResponse('No existe el grupo ' + str(pk))

    if request.method == 'GET':
        contexto = {'grupo_empresarial': grupo_empresarial}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        grupo_empresarial.estado = estado
        grupo_empresarial.save()
        return HttpResponse('Grupo actualizado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('est.delete_gruposempresariales',
                     login_url='bases:sin_permisos')
def EliminarGrupoEmpresarialModal(request, pk):
    template_name = 'est/eliminar_grupo_modal.html'
    contexto = {}
    grupo_empresarial = GruposEmpresariales.objects.\
        filter(pk=pk).first()

    if not grupo_empresarial:
        return HttpResponse('No existe el grupo ' + str(pk))

    if request.method == 'GET':
        contexto = {'grupo_empresarial': grupo_empresarial}

    if request.method == 'POST':
        grupo_empresarial.delete()
        return HttpResponse('Grupo eliminado')

    return render(request, template_name, contexto)



@login_required(login_url='/login/')
#vista para eliminar el grupoempresarial
def eliminar_grupo(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        grupo = request.GET.get("grupo", None)

        if grupo:
            try:
                grupo_obj = GruposEmpresariales.objects.filter(id_grupo_empresarial=grupo)
                usuario_grupo = UsuariosGruposEmpresariales.objects.filter(grupo_empresarial_id=grupo).exists()
                if usuario_grupo:
                    estado = 2
                else:
                    GruposEmpresariales.objects.filter(id_grupo_empresarial=grupo).delete()
                    estado = 1
            except GruposEmpresariales.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)




@login_required()
def obtener_grupos(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        if usuario:
            grupos=GruposEmpresariales.objects.all().order_by('-id_grupo_empresarial')
            grupos_html=""

            for grupo in grupos:
                grupo_fila="<tr>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(grupo.nombre)+"</p>"+\
                "</td>"+\
                "<td>"+\
                    "<p style='white-space: normal;'>"+str(grupo.pais)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(grupo.estado)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(grupo.fecha_creacion.strftime('%d/%m/%Y'))+"</p>"+\
                "</td>"+\
                "<td>"+\
                "<div class='invoice-action'>"
                grupo_fila=grupo_fila+" <a class='btn btn-icon rounded-circle btn-outline-warning mr-1 mb-1 editar_grupo' data-grupo='"+str(grupo.id_grupo_empresarial)+"'"+\
                    "role='button' data-original-title='"+str(_('editar'))+"'>"+\
                        "<i class='bx bx-edit font-medium-1'></i>"+\
                    "</a>"
                grupo_fila=grupo_fila+" <a class='btn btn-icon rounded-circle btn-outline-danger mr-1 mb-1 eliminar_grupoempresarial' data-grupo='"+str(grupo.id_grupo_empresarial)+"'"+\
                    "data-nombregrupo='"+grupo.nombre+"'  data-target='#modal_eliminargrupo' "+\
                    "role='button' title='' data-original-title='"+str(_('eliminar'))+"'>"+\
                        "<i class=' bx bx-trash font-medium-1'></i>"+\
                    "</a>"
                    
                grupo_fila = grupo_fila+"</div></td></tr>"
                grupos_html=grupos_html+grupo_fila

            return JsonResponse({'grupos_html': grupos_html})
        else:
            return HttpResponseRedirect('/')
    return JsonResponse({}, status=400)


class SociedadesListaView(SinPermisos, generic.ListView):
    permission_required = "est.view_sociedades"
    model = Sociedades
    template_name = "est/sociedades_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        return Sociedades.objects.\
            filter(
                grupo_empresarial=self.request.user.grupo_empresarial()
            )


class SociedadesCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_sociedades"
    model = Sociedades
    template_name = "est/sociedades_form.html"
    success_url = reverse_lazy("est:sociedades_lista")
    form_class = SociedadForm

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SociedadesCrearView, self).\
            get_context_data(**kwargs)
        context['grupos'] = GruposEmpresariales.objects.\
            filter(
                pais=self.request.user.pais,
                estado__descripcion='ACTIVO'
            )
        return context


class SociedadesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_sociedades"
    model = Sociedades
    template_name = "est/sociedades_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("est:sociedades_lista")
    form_class = SociedadForm

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SociedadesEditarView, self).\
            get_context_data(**kwargs)
        context['grupos'] = GruposEmpresariales.objects.\
            filter(
                pais=self.request.user.pais,
                estado__descripcion='ACTIVO'
            )
        return context


@login_required(login_url='/login/')
@permission_required('est.change_sociedades',
                     login_url='bases:sin_permisos')
def ActualizarSociedadModal(request, pk):
    template_name = 'est/actualizar_sociedad_modal.html'
    contexto = {}
    sociedad = Sociedades.objects.\
        filter(pk=pk).first()

    if not sociedad:
        return HttpResponse('No existe la sociedad ' + str(pk))

    if request.method == 'GET':
        contexto = {'sociedad': sociedad}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        sociedad.estado = estado
        sociedad.save()
        return HttpResponse('Sociedad actualizada')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('est.delete_sociedades',
                     login_url='bases:sin_permisos')
def EliminarSociedadModal(request, pk):
    template_name = 'est/eliminar_sociedad_modal.html'
    contexto = {}
    sociedad = Sociedades.objects.\
        filter(pk=pk).first()

    if not sociedad:
        return HttpResponse('No existe la sociedad ' + str(pk))

    if request.method == 'GET':
        contexto = {'sociedad': sociedad}

    if request.method == 'POST':
        sociedad.delete()
        return HttpResponse('Sociedad eliminada')

    return render(request, template_name, contexto)


class TiendasListaView(SinPermisos, generic.ListView):
    permission_required = "est.view_tiendas"
    model = Tiendas
    template_name = "est/tiendas_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"
    def get_queryset(self):
        return Tiendas.objects.\
            filter(
                sociedad__grupo_empresarial=self.request.user.grupo_empresarial()
            )


class TiendasCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_tiendas"
    model = Tiendas
    template_name = "est/tiendas_form.html"
    success_url = reverse_lazy("est:tiendas_lista")
    form_class = TiendaForm

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TiendasCrearView, self).\
            get_context_data(**kwargs)
        context['sociedades'] = Sociedades.objects.\
            filter(
                grupo_empresarial__pais=self.request.user.pais,
                estado__descripcion='ACTIVO'
            )
        context['zonas'] = Zonas.objects.\
            filter(
                grupo_empresarial=self.request.user.grupo_empresarial(),
                estado__descripcion='ACTIVO'
            )
        context['ciudades'] = Ciudades.objects.\
            filter(
                localidad__pais=self.request.user.pais,
                estado__descripcion='ACTIVO'
            )
        context['sectores'] = Sectores.objects.\
            filter(
                grupo_empresarial=self.request.user.grupo_empresarial(),
                estado__descripcion='ACTIVO'
            )
        return context


@login_required(login_url='/login/')
@permission_required('est.change_tiendas',
                     login_url='bases:sin_permisos')
def TiendasEditarView(request, pk):
    template_name = "est/tiendas_form.html"
    tienda = Tiendas.objects.get(id_tienda=pk)
    form = TiendaForm(instance=tienda)
    sociedades = Sociedades.objects.\
    filter(
        grupo_empresarial__pais= request.user.pais,
        estado__descripcion='ACTIVO'
    )

    zonas = Zonas.objects.\
    filter(
        grupo_empresarial= request.user.grupo_empresarial(),
        estado__descripcion='ACTIVO'
    )

    ciudades = Ciudades.objects.\
    filter(
        localidad__pais=request.user.pais,
        estado__descripcion='ACTIVO'
    )
    sectores = Sectores.objects.\
    filter(
        grupo_empresarial=request.user.grupo_empresarial(),
        estado__descripcion='ACTIVO'
    )

    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        sociedad = request.POST['sociedad']
        email = request.POST['email']
        direccion_tienda = request.POST['direccion_tienda']
        telefono = request.POST['telefono']
        zona = request.POST['zona']
        ciudad = request.POST['ciudad']
        sector = request.POST['sector']

        sociedad_obj = Sociedades.objects.get(id_sociedad=sociedad)
        zona_obj = Zonas.objects.get(id_zona=zona)
        ciudad_obj = Ciudades.objects.get(id_ciudad=ciudad)
        sector_obj = Sectores.objects.get(id_sector=sector)

        if zona_obj != tienda.zona:
            user_mart = UsuariosTiendas.objects.filter(tienda_id=tienda.id_tienda)
            for j in user_mart:
                j.delete()
                
        tienda.fecha_modificacion = datetime.now()
        tienda.usuario_modifica = request.user.id
        tienda.codigo = codigo
        tienda.nombre = nombre
        tienda.sociedad = sociedad_obj
        tienda.zona = zona_obj
        tienda.ciudad = ciudad_obj
        tienda.sector = sector_obj
        tienda.email = email
        tienda.direccion_tienda = direccion_tienda
        tienda.telefono = telefono

        tienda.save()
        return HttpResponseRedirect('/establecimientos/tiendas/lista')    
    data = {
        'form': form,
        'sociedades': sociedades,
        'zonas': zonas,
        'ciudades': ciudades,
        'sectores': sectores,
        'tienda': tienda,
        }
    return render(request, template_name, data)



@login_required(login_url='/login/')
@permission_required('est.change_tiendas',
                     login_url='bases:sin_permisos')
def ActualizarTiendaModal(request, pk):
    template_name = 'est/actualizar_tienda_modal.html'
    contexto = {}
    tienda = Tiendas.objects.\
        filter(pk=pk).first()

    if not tienda:
        return HttpResponse('No existe la tienda ' + str(pk))

    if request.method == 'GET':
        contexto = {'tienda': tienda}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        tienda.estado = estado
        tienda.save()
        return HttpResponse('Tienda actualizada')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('est.delete_tiendas',
                     login_url='bases:sin_permisos')
def EliminarTiendaModal(request, pk):
    template_name = 'est/eliminar_tienda_modal.html'
    contexto = {}
    tienda = Tiendas.objects.\
        filter(pk=pk).first()

    if not tienda:
        return HttpResponse('No existe la tienda ' + str(pk))

    if request.method == 'GET':
        contexto = {'tienda': tienda}

    if request.method == 'POST':
        tienda.delete()
        return HttpResponse('Tienda eliminada')

    return render(request, template_name, contexto)




@login_required(login_url='/login/')
def eliminar_tienda(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        tienda = request.GET.get("tienda", None)

        if tienda:
            try:
                tienda_obj = Tiendas.objects.filter(id_tienda=tienda)
                # usuario_grupo_emp = UsuariosGruposEmpresariales.objects.filter(usuario_id=usuario.id)
                usuario_tienda = UsuariosTiendas.objects.filter(tienda_id=tienda).exists()
                if usuario_tienda:
                    estado = 2
                else:
                    Tiendas.objects.filter(id_tienda=tienda).delete()
                    estado = 1
            except Tiendas.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)


# vista para obtener las tiendas despues de eliminar alguna tienda


@login_required()
def obtener_tiendas(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        if usuario:
            tiendas=Tiendas.objects.all().order_by('-id_tienda')
            tiendas_html=""

            for tienda in tiendas:
                tienda_fila="<tr>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(tienda.codigo)+"</p>"+\
                "</td>"+\
                "<td>"+\
                    "<p style='white-space: normal;'>"+str(tienda.nombre)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(tienda.sociedad)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(tienda.zona)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(tienda.estado)+"</p>"+\
                "</td>"+\
                "<td >"+\
                    "<p style='white-space: normal;'>"+str(tienda.fecha_creacion.strftime('%d/%m/%Y'))+"</p>"+\
                "</td>"+\
                "<td>"+\
                "<div class='invoice-action'>"
                tienda_fila=tienda_fila+" <a class='btn btn-icon rounded-circle btn-outline-warning mr-1 mb-1 editar_tienda' data-tienda='"+str(tienda.id_tienda)+"'"+\
                    "role='button' data-original-title='"+str(_('editar'))+"'>"+\
                        "<i class='bx bx-edit font-medium-1'></i>"+\
                    "</a>"
                tienda_fila=tienda_fila+" <a class='btn btn-icon rounded-circle btn-outline-danger mr-1 mb-1 eliminar_tienda' data-tienda='"+str(tienda.id_tienda)+"'"+\
                    "data-descripcion='"+tienda.nombre+"'  data-target='#modal_eliminartienda' "+\
                    "role='button' title='' data-original-title='"+str(_('eliminar'))+"'>"+\
                        "<i class=' bx bx-trash font-medium-1'></i>"+\
                    "</a>"
                    
                tienda_fila = tienda_fila+"</div></td></tr>"
                tiendas_html=tiendas_html+tienda_fila

            return JsonResponse({'tiendas_html': tiendas_html})
        else:
            return HttpResponseRedirect('/')
    return JsonResponse({}, status = 400)







class TalleresListaView(SinPermisos, generic.ListView):
    permission_required = "est.view_talleres"
    model = Talleres
    template_name = "est/talleres_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    # def get_queryset(self):
    #     return Roles.objects.filter(usuario_crea=self.request.user.id)


class TalleresCrearView(SinPermisos, generic.CreateView):
    permission_required = "est.add_talleres"
    model = Talleres
    template_name = "est/talleres_form.html"
    success_url = reverse_lazy("est:talleres_lista")
    form_class = TallerForm

    def form_valid(self, form):
        cant_talleres = Talleres.objects.\
            filter(pais=form.instance.pais).count()
        form.instance.prioridad = cant_talleres + 1
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TalleresCrearView, self).\
            get_context_data(**kwargs)
        context['paises'] = Paises.objects.all()
        return context


class TalleresEditarView(SinPermisos, generic.UpdateView):
    permission_required = "est.change_talleres"
    model = Talleres
    template_name = "est/talleres_form.html"
    context_object_name = "obj"
    success_url = reverse_lazy("est:talleres_lista")
    form_class = TallerForm

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TalleresEditarView, self).\
            get_context_data(**kwargs)
        context['paises'] = Paises.objects.all()
        return context


@login_required(login_url='/login/')
@permission_required('est.change_talleres',
                     login_url='bases:sin_permisos')
def ActualizarGrupoEmpresarialModal(request, pk):
    template_name = 'est/actualizar_taller_modal.html'
    contexto = {}
    taller = Talleres.objects.\
        filter(pk=pk).first()

    if not taller:
        return HttpResponse('No existe el taller ' + str(pk))

    if request.method == 'GET':
        contexto = {'taller': taller}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        taller.estado = estado
        taller.save()
        return HttpResponse('Taller actualizado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('est.delete_talleres',
                     login_url='bases:sin_permisos')
def EliminarTallerModal(request, pk):
    template_name = 'est/eliminar_taller_modal.html'
    contexto = {}
    taller = Talleres.objects.\
        filter(pk=pk).first()

    if not taller:
        return HttpResponse('No existe el taller ' + str(pk))

    if request.method == 'GET':
        contexto = {'taller': taller}

    if request.method == 'POST':
        taller.delete()
        return HttpResponse('Taller eliminado')

    return render(request, template_name, contexto)



@login_required(login_url='/login/')
def eliminar_taller(request):

    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        taller = request.GET.get("taller", None)

        if taller:
            try:
                taller_obj = Talleres.objects.filter(id_taller=taller)
                usuario_taller = UsuariosTalleres.objects.filter(taller_id=int(taller)).exists()
                if usuario_taller:
                    estado = 2
                else:
                    Talleres.objects.filter(id_taller=taller).delete()
                    estado = 1
            except Talleres.DoesNotExist:
                estado = 0
                return HttpResponseRedirect('/')
        else:
            estado = 0

        return JsonResponse({"estado": estado})
    return JsonResponse({}, status = 400)

