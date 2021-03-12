from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError


from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, \
    permission_required
import json

from .models import Proveedores
from .forms import ProveedorForm
from bases.models import Estados
from trn.models import OrdenTrabajo, SolicitudTrabajo
from est.models import Talleres
from usr.models import Usuarios
from ctg.models import Items

from bases.views import SinPermisos


class ProveedoresListaView(SinPermisos,
                           generic.ListView):
    permission_required = "prv.view_proveedores"
    model = Proveedores
    template_name = "prv/proveedores_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
        if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
            return Proveedores.objects.\
                filter(pais_id=self.request.user.pais_id).\
                filter(zona__grupo_empresarial=self.request.user.grupo_empresarial())
        else:
            return Proveedores.objects.\
                filter(taller=self.request.user.taller().id_taller)


class ProveedoresCrearView(SinPermisos, generic.CreateView):
    permission_required = "prv.add_proveedores"
    model = Proveedores
    template_name = "prv/proveedores_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("prv:proveedores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        if self.request.user.tipo_usuario.descripcion == "USUARIO OPERACIONES":
            form.instance.taller = 1
        else:

            form.instance.taller = self.request.user.taller().id_taller
        form.instance.tipo_usuario = self.request.user.tipo_usuario_id
        form.instance.pais = self.request.user.pais
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "prv/proveedores_form.html",
                          {'mensaje': e.__cause__, 'form': form})

    def form_invalid(self, form):
        # print(form.errors)
        return render(self.request,
                          "prv/proveedores_form.html",
                          {'mensaje': form.errors, 'form': form})

    def get_form_kwargs(self):
        kwargs = super(ProveedoresCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ProveedoresEditarView(SinPermisos, generic.UpdateView):
    permission_required = "prv.change_proveedores"
    model = Proveedores
    template_name = "prv/proveedores_form.html"
    context_object_name = "obj"
    form_class = ProveedorForm
    success_url = reverse_lazy("prv:proveedores_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        secuencia_ordenes = form.instance.secuencia_ordenes
        secuencia_solicitudes = form.instance.secuencia_solicitudes
        ultima_orden = OrdenTrabajo.objects.\
            filter(proveedor=self.object).\
            order_by('-fecha_creacion').first()
        if ultima_orden:
            sec_orden_actual = int(ultima_orden.secuencia[-5:])
        else:
            sec_orden_actual = 1
        ultima_solicitud = SolicitudTrabajo.objects.\
            filter(proveedor=self.object).\
            order_by('-fecha_creacion').first()
        if ultima_solicitud:
            sec_solicitud_actual = int(ultima_solicitud.secuencia[-5:])
        else:
            sec_solicitud_actual = 1
        if secuencia_ordenes < sec_orden_actual:
            return render(self.request,
                          "prv/proveedores_form.html",
                          {
                              'mensaje': 'secuencia-ordenes',
                              'form': form}
                          )
        if secuencia_solicitudes < sec_solicitud_actual:
            return render(self.request,
                          "prv/proveedores_form.html",
                          {
                              'mensaje': 'secuencia-solicitudes',
                              'form': form}
                          )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProveedoresEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('prv.change_proveedores',
                     login_url='bases:sin_permisos')
def ActualizarProveedorModal(request, pk):
    template_name = 'prv/actualizar_proveedor_modal.html'
    contexto = {}
    proveedor = Proveedores.objects.filter(pk=pk).first()

    if not proveedor:
        return HttpResponse('No existe el proveedor ' + str(pk))

    if request.method == 'GET':
        contexto = {'proveedor': proveedor}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        proveedor.estado = estado
        proveedor.save()
        return HttpResponse('proveedor actualizado')

    return render(request, template_name, contexto)





@login_required(login_url='/login/')
# @permission_required('prv.change_proveedores',
#                      login_url='bases:sin_permisos')
def eliminar_proveedor(request):
    ''' Permite eliminar de un proovedor,
    en caso de no estar relacionado con un item.
    '''
    if request.is_ajax and request.method == "GET":
        usuario=get_object_or_404(Usuarios,id=request.user.id)
        proveedor = request.GET.get("proveedor", None)
        if proveedor:
            prv_obj = Proveedores.objects.filter(id=int(proveedor)).first()
            try:
                item_prv = Items.objects.filter(id_proveedor=prv_obj.id).first()
                if item_prv:
                    estado = 2
                else:
                    Proveedores.objects.filter(id=int(proveedor)).delete()
                    estado = 1
            except Proveedores.DoesNotExist:
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