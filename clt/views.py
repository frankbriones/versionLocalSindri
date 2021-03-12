from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core import serializers
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
import json


from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Clientes
from .forms import ClientesForm
from .serializer import ClientesSerializer

from bases.views import SinPermisos
from bases.models import Estados
from usr.models import Usuarios
from trn.models import OrdenTrabajo, SolicitudTrabajo


class ClientesListaView(SinPermisos,
                        generic.ListView):
    permission_required = "clt.view_clientes"
    model = Clientes
    template_name = "clt/clientes_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.rol.admin:
            return Clientes.objects.\
                filter(pais_id=self.request.user.pais_id)
        else:
            return Clientes.objects.\
                filter(usuario_crea=self.request.user.id)


class ClientesCrearView(SinPermisos, generic.CreateView):
    permission_required = "clt.add_clientes"
    model = Clientes
    template_name = "clt/clientes_form.html"
    context_object_name = "obj"
    form_class = ClientesForm
    success_url = reverse_lazy("clt:clientes_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_crea = self.request.user.id
        form.instance.pais = self.request.user.pais
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            print(e.__cause__)
            return render(self.request,
                          "clt/clientes_form.html",
                          {'mensaje': e.__cause__, 'form': form})

    def get_form_kwargs(self):
        kwargs = super(ClientesCrearView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ClientesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "clt.change_clientes"
    model = Clientes
    template_name = "clt/clientes_form.html"
    context_object_name = "obj"
    form_class = ClientesForm
    success_url = reverse_lazy("clt:clientes_lista")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ClientesEditarView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required(login_url='/login/')
@permission_required('clt.change_clientes',
                     login_url='bases:sin_permisos')
def ActualizarClienteModal(request, pk):
    template_name = 'clt/actualizar_cliente_modal.html'
    contexto = {}
    cliente = Clientes.objects.filter(pk=pk).first()

    if not cliente:
        return HttpResponse('No existe el cliente ' + str(pk))

    if request.method == 'GET':
        contexto = {'cliente': cliente}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        cliente.estado = estado
        cliente.save()
        return HttpResponse('Cliente actualizado')

    return render(request, template_name, contexto)


class ClientesModalView(generic.TemplateView):
    template_name = "clt/clientes_modal.html"


class ClientesListaAPIView(APIView):
    def get(self, request):
        clientes = Clientes.objects.all()
        data = ClientesSerializer(clientes, many=True).data
        return Response(data)


class BusquedaCliente(APIView):
    def get(self, request, identificacion):
        cliente = get_object_or_404(Clientes,
                                    identificacion=identificacion,
                                    pais_id=request.user.pais_id)
        data = ClientesSerializer(cliente).data
        return Response(data)


@login_required(login_url='/login/')
@permission_required('clt.add_clientes',
                     login_url='bases:sin_permisos')
def ClientesCrearModal(request, id_trn=None, tipo=None):
    template_name = "clt/clientes_modal.html"
    form_rol = {}
    contexto = {}

    if request.method == 'GET':
        form = ClientesForm(request=request)

        contexto = {
                    'form': form,
                    'id_trn': id_trn,
                    'tipo': tipo
                    }

    if request.method == 'POST':
        tipo_usuario = request.user.tipo_usuario
        json_data = json.loads(request.body)
        identificacion = json_data['identificacion']
        nombres = json_data['nombres']
        apellidos = json_data['apellidos']
        ciudad = json_data['ciudad']
        direccion = json_data['direccion']
        telefono = json_data['telefono']
        correo = json_data['correo']

        infoCliente = Clientes(
            identificacion=identificacion,
            nombres=nombres,
            apellidos=apellidos,
            ciudad_id=ciudad,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            usuario_crea=request.user.id,
            pais_id=request.user.pais_id
        )

        if infoCliente:
            try:
                infoCliente.save()
                cliente_nuevo = serializers.serialize('json', [infoCliente, ])
                cliente_json = json.loads(cliente_nuevo)
                cliente_data = json.dumps(cliente_json[0])
                return HttpResponse(
                    cliente_data,
                    content_type='text/json-comment-filtered'
                )
            except IntegrityError as e:
                mensaje_error = str(e.__cause__)
                return HttpResponse(json.dumps({'mensaje': mensaje_error}))

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
#permisos
def eliminar_cliente(request):
    """Peticion POST: permite eliminar cliente
    ---------

    si la validacion es correcta, redirige a la pagina de lista de clientes"""
    if request.is_ajax and request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=request.user.id)
        cliente = request.GET.get('cliente', None)
        if cliente:
            try:
                cliente_obj = Clientes.objects.filter(id_cliente=cliente).first()
                cliente_orden = OrdenTrabajo.objects.filter(cliente_id=cliente_obj.id_cliente).first()
                if cliente_orden:
                    estado = 2
                else:
                    Clientes.objects.filter(id_cliente=cliente).delete()
                    estado = 1
            except Clientes.DoesNotExist:
                estado=0
                return HttpResponseRedirect('/')
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)