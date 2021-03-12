from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib import messages

import json
import datetime
import pdb
from random import choice

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group, ContentType
from django.shortcuts import HttpResponseRedirect, resolve_url, get_object_or_404


from .models import TipoUsuarios, Roles, Usuarios, UsuariosGrupos, \
    GruposPermisos, UsuariosGruposEmpresariales, UsuariosTalleres,\
    RolesGruposEmpresariales, RolesTalleres, UsuariosTiendas
# from cfg.models import ConfigGeneral
from ubc.models import Ciudades, Paises
from ctg.models import EstandarTallas
from bases.models import Estados
from est.models import GruposEmpresariales, Talleres, Tiendas, Sectores, Zonas
from est.serializers import TiendasSerializer

from .forms import TipoUsuarioForm, RolForm, RegistroForm, \
    EditarUsuarioForm, EditarForm, RolGrupoForm, UsuarioGrupoForm,\
    EditarPerfilForm

from bases.views import SinPermisos

from .tasks import enviarCorreoContrasena

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class TipoUsuarioView(LoginRequiredMixin, generic.ListView):
    model = TipoUsuarios
    template_name = "usr/tipo_usuarios_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"


class TipoUsuarioFormView(LoginRequiredMixin, generic.CreateView):
    model = TipoUsuarios
    template_name = "usr/tipo_usuario_form.html"
    context_object_name = "obj"
    form_class = TipoUsuarioForm
    success_url = reverse_lazy("usr:lista_tipo_usuarios")
    login_url = "bases:login"


class RolListaView(SinPermisos,
                   generic.ListView):
    permission_required = "usr.view_roles"
    model = Roles
    template_name = "usr/roles_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.tipo_usuario.tipo_usuario == 'TALLER':
            return RolesTalleres.objects.filter(
                taller=self.request.user.taller()
            )
        else:
            return RolesGruposEmpresariales.objects.filter(
                grupo_empresarial=self.request.user.grupo_empresarial()
            )


class RolesCrearView(SinPermisos, generic.CreateView):
    permission_required = "usr.add_roles"
    model = Roles
    template_name = "usr/roles_form.html"
    context_object_name = "obj"
    form_class = RolForm

    def get_success_url(self, **kwargs):
        return reverse('usr:roles_permisos',
                       kwargs={'rol_id': self.object.id_rol})

    def form_valid(self, form):
        tipo_usuario = self.request.user.tipo_usuario
        if tipo_usuario.tipo_usuario == 'TALLER':
            entidad = self.request.user.taller.nombre
        else:
            if tipo_usuario.tipo_usuario == 'OPERACIONES':
                entidad = self.request.user.config_gen.empresa
            else:
                entidad = 'neutral'
        incial = self.request.user.pais.iniciales
        tipo = self.request.user.tipo_usuario.tipo_usuario
        descripcion = form.instance.descripcion
        descripcion_grupo = \
            incial + '_' + tipo + '_' + entidad + '_' + descripcion
        infoGrupo = Group(
            name=descripcion_grupo
        )
        if infoGrupo:
            try:
                infoGrupo.save()
            except IntegrityError as e:
                return render(self.request,
                              'usr/roles_form.html',
                              {'mensaje': e.__cause__,
                               'form': form})
        form.instance.tipo_usuario = tipo_usuario
        form.instance.grupo = infoGrupo
        form.instance.pais = self.request.user.pais
        form.instance.conf_general = self.request.user.config_gen
        form.instance.taller = self.request.user.taller
        form.instance.usuario_crea = self.request.user.id
        return super().form_valid(form)


class RolesEditarView(SinPermisos, generic.UpdateView):
    permission_required = "usr.add_roles"
    model = Roles
    template_name = "usr/roles_form.html"
    context_object_name = "obj"
    form_class = RolForm

    def get_success_url(self, **kwargs):
        return reverse('usr:roles_permisos',
                       kwargs={'rol_id': self.object.id_rol})

    def form_valid(self, form):
        tipo_usuario = self.request.user.tipo_usuario
        if tipo_usuario.tipo_usuario == 'TALLER':
            entidad = self.request.user.taller.nombre
        else:
            if tipo_usuario.tipo_usuario == 'OPERACIONES':
                entidad = self.request.user.config_gen.empresa
            else:
                entidad = 'neutral'
        incial = self.request.user.pais.iniciales
        tipo = self.request.user.tipo_usuario.tipo_usuario
        descripcion = form.instance.descripcion
        descripcion_grupo = \
            incial + '_' + tipo + '_' + entidad + '_' + descripcion
        rol = Roles.objects.filter(id_rol=self.kwargs['pk']).first()
        grupo = Group.objects.filter(id=rol.grupo_id).first()
        grupo.name = descripcion_grupo
        try:
            grupo.save()
        except IntegrityError as e:
            return render(self.request,
                          'usr/roles_form.html',
                          {'mensaje': e.__cause__,
                           'form': form})
        form.instance.tipo_usuario = tipo_usuario
        form.instance.grupo = grupo
        form.instance.pais = self.request.user.pais
        form.instance.conf_general = self.request.user.config_gen
        form.instance.taller = self.request.user.taller
        form.instance.usuario_modifica = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('usr.add_roles',
                     login_url='bases:sin_permisos')
def RolesPermisos(request, rol_id=None):
    template_name = "usr/roles_permisos_form.html"

    rol = Roles.objects.filter(pk=rol_id).first()

    # if request.user.rol.id_rol == 1:
    #     permisos_admin = GruposPermisos.objects.all()
    if request.user.tipo_usuario.descripcion == 'USUARIO TALLER':
        grupo = Group.objects.\
            filter(name='NN_ADMINISTRADOR_ADMIN TALLER').first()
        permisos_admin = GruposPermisos.objects.filter(group=grupo)
    if request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
        grupo = Group.objects.\
            filter(name='NN_ADMINISTRADOR_ADMIN OPERACIONES').first()
        permisos_admin = GruposPermisos.objects.filter(group=grupo)
    contenidos = []
    modulos = []

    for permiso in permisos_admin:
        tmp = []
        tmp.append(permiso.permission.content_type.model)
        tmp.append(permiso.permission.content_type.app_label)
        contenidos.append(tmp)
        modulo_tmp = permiso.permission.content_type.app_label
        convertidor = {
            'cfg': 'Configuraciones',
            'ctg': 'Catálogo',
            'clt': 'Clientes',
            'prv': 'Proveedores',
            'trn': 'Transacciones',
            'ubc': 'Ubicaciones',
            'usr': 'usuarios',
            'est': 'Establecimientos'
        }
        modulo = convertidor.get(modulo_tmp, 'ninguno')
        modulos.append([modulo_tmp, modulo])
    contenidos = set(map(tuple, contenidos))
    contenidos = sorted(contenidos)
    modulos = set(map(tuple, modulos))
    modulos = sorted(modulos)
    form_class = RolForm
    contexto = {}

    if request.method == 'GET':
        permisos_rol = []

        if rol:
            permisos_asignados = GruposPermisos.objects.filter(group=rol.grupo)
            for permiso in permisos_asignados:
                permisos_rol.append(str(permiso.permission_id))

            permisos_asignados = json.dumps(permisos_rol)
            form_class = RolForm(instance=rol)

        else:
            permisos_asignados = None

        contexto = {'permisos_admin': permisos_admin,
                    'rol': rol,
                    'contenidos': contenidos,
                    'modulos': modulos,
                    'permisos_asignados': permisos_asignados,
                    'form': form_class
                    }

    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        zonal = request.POST.get('zonal', None)
        if zonal == 'true':
            zonal = True
        else:
            zonal = False
        pais_id = request.user.pais_id
        permisos = request.POST.getlist('permisos[]')
        permisos_lista = json.loads(permisos[0])

        if not rol:
            tipo_usuario = request.user.tipo_usuario
            if tipo_usuario.tipo_usuario == 'TALLER':
                entidad = request.user.taller().nombre
            else:
                if tipo_usuario.tipo_usuario == 'OPERACIONES':
                    entidad = request.user.grupo_empresarial().nombre
                else:
                    entidad = 'neutral'
            incial = request.user.pais.iniciales
            tipo = request.user.tipo_usuario.tipo_usuario
            descripcion_grupo = \
                incial + '_' + tipo + '_' + entidad + '_' + descripcion
            infoGrupo = Group(
                name=descripcion_grupo
            )
            if infoGrupo:
                try:
                    infoGrupo.save()
                except IntegrityError as e:
                    return JsonResponse(
                        {'mensaje': str(e.__cause__)},
                        status=500)
            infoRol = Roles(
                descripcion=descripcion,
                zonal=zonal,
                tipo_usuario=request.user.tipo_usuario,
                grupo=infoGrupo,
                usuario_crea=request.user.id
            )
            if infoRol:
                infoRol.save()
                for permiso in permisos_lista:
                    if permiso != 'on' and permiso != '0':
                        infoPermiso = GruposPermisos(
                            group_id=infoRol.grupo_id,
                            permission_id=permiso
                        )
                        infoPermiso.save()
                if infoRol.tipo_usuario.tipo_usuario == 'TALLER':
                    infoTipo = RolesTalleres(
                        rol=infoRol,
                        taller=request.user.taller()
                    )
                else:
                    infoTipo = RolesGruposEmpresariales(
                        rol=infoRol,
                        grupo_empresarial=request.user.grupo_empresarial()
                    )
                infoTipo.save()
        else:
            rol.descripcion = descripcion
            rol.zonal = zonal
            rol.usuario_modifica = request.user.id
            rol.save()
            permisos_grupo = GruposPermisos.objects.\
                filter(group_id=rol.grupo_id)
            if permisos_grupo:
                for permiso_grupo in permisos_grupo:
                    permiso_grupo.delete()

            for permiso in permisos_lista:
                if permiso != 'on' and permiso != '0':
                    infoPermiso = GruposPermisos(
                        group_id=rol.grupo_id,
                        permission_id=permiso
                    )
                    infoPermiso.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_roles',
                     login_url='bases:sin_permisos')
def ActualizarRolModal(request, pk):
    template_name = 'usr/actualizar_rol_modal.html'
    contexto = {}
    rol = Roles.objects.filter(id_rol=pk).first()

    if not rol:
        return HttpResponse('No existe el rol ' + str(pk))

    if request.method == 'GET':
        contexto = {'rol': rol}

    if request.method == 'POST':
        json_data = json.loads(request.body)
        estado = json_data['estado']
        if estado == 'ACTIVO':
            estado = Estados.objects.\
                filter(descripcion='INACTIVO').first()
        if estado == 'INACTIVO':
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
        rol.estado = estado
        rol.save()
        return HttpResponse('Rol actualizado')

    return render(request, template_name, contexto)


class UsuarioListaView(SinPermisos, generic.ListView):
    permission_required = "usr.view_usuarios"
    model = Usuarios
    template_name = "usr/usuarios_lista.html"
    context_object_name = "obj"
    login_url = "bases:login"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuarios.objects.\
                filter(rol_id=self.request.user.rol_id)
        else:
            if self.request.user.is_staff:

                return Usuarios.objects.\
                    filter(pais_id=self.request.user.pais_id).\
                    exclude(id=self.request.user.id)

            else:
                print(self.request.user.grupo_empresarial())
                if self.request.user.tipo_usuario.descripcion == 'USUARIO OPERACIONES':
                    id_usuarios = UsuariosGruposEmpresariales.objects.\
                        filter(
                            grupo_empresarial=self.request.user.grupo_empresarial()
                        ).values('usuario_id')
                    
                    return Usuarios.objects.\
                        filter(
                            id__in=id_usuarios
                            ).\
                        exclude(id=self.request.user.id)
                else:
                    id_usuarios = UsuariosTalleres.objects.\
                        filter(
                            taller_id=self.request.user.taller().id_taller
                        ).values('usuario_id')
                    return Usuarios.objects.\
                        filter(
                            id__in=id_usuarios
                            ).\
                        exclude(id=self.request.user.id)


class EditarPerfil(LoginRequiredMixin, generic.UpdateView):

    # permission_required = "usr.change_usuarios"
    model = Usuarios
    template_name = "usr/editar_perfil.html"
    context_object_name = "usuario"
    form_class = EditarPerfilForm
    success_url = reverse_lazy('bases:home')
    login_url = "bases:login"
    

    def form_valid(self, form):
        email = form.instance.email
        if Usuarios.objects.filter(email=email).\
                exclude(id=self.object.id).exists():
            return render(self.request,
                          'usr/editar_perfil.html',
                          {'mensaje': 'correo-duplicado',
                           'form': form})
        form.instance.usuario_modifica = self.request.user.id
        celular = form.instance.telefono
        form.instance.telefono = self.object.pais.prefijo_cel +\
            celular[-9:]
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EditarPerfil, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    # restringir la edicion de otros usuarios que no sea el logeado
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user




"""vista para obtener las tiendas segun la zona"""
@login_required()
def tiendas_jefezonal(request):

    if request.is_ajax and request.method == "GET":
        zona_id = request.GET.get('zona', None)
        usuario_zonal = request.GET.get("usuario", None)
        if zona_id: 
            try:
                user =Usuarios.objects.get(pk=usuario_zonal)
                if int(user.zona) == int(zona_id):
                    estado =2
                else:
                    estado =1
            except Usuarios.DoesNotExist:
                estado = 1
        else:
            estado = 0
        return JsonResponse({'estado': estado})
    return JsonResponse({}, status=400)




@login_required(login_url='/login/')
@permission_required('usr.add_usuarios',
                     login_url='bases:sin_permisos')
def UsuariosForm(request, pk=None):
    template_name = "usr/registro.html"
    form_registro = {}
    
    usuario = Usuarios.objects.filter(pk=pk).first()


    if request.method == 'GET':
        form_registro = UsuarioGrupoForm
        grupos_empresariales = None
        talleres = None
        zonas = None
        zona = ""
        paises = Paises.objects.all().exclude(nombre='NEUTRO')
        tiendas = Tiendas.objects.filter(
            estado__descripcion='ACTIVO',
            sociedad__grupo_empresarial= request.user.grupo_empresarial(),
            zona__grupo_empresarial=request.user.grupo_empresarial()
        )



        tiendas = TiendasSerializer(tiendas, many=True).data
        tiendas = json.dumps(tiendas)
        tiendas_asignadas = None
        
        if request.user.is_superuser:
            roles = Roles.objects.filter(descripcion='ADMINISTRADOR')
            grupos_empresariales = GruposEmpresariales.objects.\
                filter(estado__descripcion='ACTIVO')
        elif request.user.is_staff:
            roles = Roles.objects.filter(admin=True).\
                exclude(id_rol=request.user.rol.id_rol)
            grupos_empresariales = GruposEmpresariales.objects.\
                filter(
                    pais=request.user.pais,
                    estado__descripcion='ACTIVO'
                    )
            talleres = Talleres.objects.filter(
                pais=request.user.pais,
                estado__descripcion='ACTIVO'
            )

        else:

            tipo = request.user.tipo_usuario
            if tipo.tipo_usuario == 'OPERACIONES':
                roles_id = RolesGruposEmpresariales.objects.\
                    filter(
                        rol__estado__descripcion='ACTIVO',
                        grupo_empresarial=request.user.grupo_empresarial()
                    ).\
                    exclude(rol=request.user.rol).\
                    values('rol')
                roles = Roles.objects.filter(
                    id_rol__in=roles_id
                )

                
                zonas = Zonas.objects.filter(grupo_empresarial=request.user.grupo_empresarial())

            else:
                roles_id = RolesTalleres.objects.\
                    filter(
                        rol__estado__descripcion='ACTIVO',
                        taller=request.user.taller()
                    ).\
                    exclude(rol=request.user.rol).\
                    values('rol')
                roles = Roles.objects.filter(
                    id_rol__in=roles_id
                )
                talleres = Talleres.objects.filter(
                    pais=request.user.pais,
                    estado__descripcion='ACTIVO'
                )

                


        if usuario:
            form_registro = UsuarioGrupoForm(
                request=request,
                instance={'usuario': usuario}
            )
            tiendas_asignadas_id = UsuariosTiendas.objects.filter(
                usuario=usuario
            ).values('tienda')
            tiendas_asignadas = Tiendas.objects.filter(
                id_tienda__in=tiendas_asignadas_id
            )
            tiendas_asignadas = TiendasSerializer(
                tiendas_asignadas, many=True
                ).data
            tiendas_asignadas = json.dumps(tiendas_asignadas)
        contexto = {
            'usuario': usuario,
            'form': form_registro,
            'roles': roles,
            'grupos_empresariales': grupos_empresariales,
            'talleres': talleres,
            'tiendas': tiendas,
            'tiendas_asignadas': tiendas_asignadas,
            'paises': paises,
            'zonas': zonas,
            'zona':zona,
            }

    if request.method == 'POST':
        taller =""
        grupo_empresarial = ""
        if request.user.is_superuser:
            pais = request.POST['pais']
        username = request.POST['usuario-username']
        usuario_telegram = request.POST['usuario-usuario_telegram']
        print(usuario_telegram)
        print('*************')
        first_name = request.POST['usuario-first_name']
        last_name = request.POST['usuario-last_name']
        email = request.POST['usuario-email']
        telefono = request.POST['usuario-telefono']
        telefono = request.user.pais.prefijo_cel + telefono[-9:]
        taller_id =request.POST['taller']
        if taller_id != '0':
            taller = request.user.taller()

        tiendas_agregadas = request.POST.getlist('tiendas_agregadas[]')
        tiendas = json.loads(tiendas_agregadas[0])
        rol = request.POST.get('usuario-rol', None)
        rol_usuario = Usuarios.objects.filter(username__iexact=username).values('rol')
        usuario = Usuarios.objects.filter(username__iexact=username).first()

        if rol is None:
            rol = Roles.objects.filter(id_rol__in=rol_usuario).first()
            tipo_usuario = rol.tipo_usuario

        else:    
            rol = Roles.objects.filter(pk=rol).first()
            tipo_usuario = rol.tipo_usuario

        zona = request.POST['zona']
        
        grupo_emp = request.POST['grupo_empresarial']
        if grupo_emp == '0':
            grupo_neutro = GruposEmpresariales.objects.filter(nombre="NEUTRO").first()
            grupo_id = grupo_neutro.id_grupo_empresarial
        else:
            pass
        if rol.id_rol == 1:
            is_staff = True
        else:
            is_staff = False

        if rol.descripcion != 'ADMINISTRADOR':
            grupo_neutro = GruposEmpresariales.objects.filter(nombre="NEUTRO").first()

            if tipo_usuario.tipo_usuario == 'TALLER':
                taller = request.user.taller()
            else:
                grupo_empresarial = GruposEmpresariales.objects.\
                    filter(
                        id_grupo_empresarial=grupo_emp
                    ).first()
                # print(grupo_empresarial, 'grupo empresarial')
                if grupo_empresarial is None:
                    grupo_empresarial = request.user.grupo_empresarial()

        if not usuario:
            pais = request.user.pais.id_pais
            if Usuarios.objects.filter(email=email).exists():
                return JsonResponse(
                    {'mensaje': 'Correo ya se encuentra registrado'},
                    status=500
                    )
            longitud = 6
            valores = "0123456789" + \
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            tmp_pass = ""
            tmp_pass = tmp_pass.\
                join([choice(valores) for i in range(longitud)])
            tmp_pass.replace(" ", "")

            password = make_password(tmp_pass, salt=None, hasher='default')

            if zona == '':
                zona = 0


            infoUsuario = Usuarios(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                rol=rol,
                telefono=telefono,
                password=password,
                tipo_usuario=tipo_usuario,
                pais_id=pais,
                is_staff=is_staff,
                zona=zona,
                usuario_telegram=usuario_telegram
                # taller=taller,
            )

            if infoUsuario:
                try:
                    infoUsuario.save()
                except IntegrityError as e:
                    return JsonResponse(
                        {'mensaje': str(e.__cause__)}, status=500
                        )
                infoGrupo = UsuariosGrupos(
                    usuarios=infoUsuario,
                    group=rol.grupo
                )
                if infoGrupo:
                    infoGrupo.save()
                if infoUsuario.rol.descripcion != 'ADMINISTRADOR':
                    if infoUsuario.tipo_usuario.tipo_usuario == 'TALLER':
                        if taller_id == '0':
                            taller_id = request.user.taller().id_taller
                        infoTipo = UsuariosTalleres(
                            usuario=infoUsuario,
                            taller_id=taller_id
                        )

                    else:
                        infoTipo = UsuariosGruposEmpresariales(
                            usuario=infoUsuario,
                            grupo_empresarial=grupo_empresarial
                        )
                    infoTipo.save()
                if len(tiendas) > 0:
                    for tienda in tiendas:
                            
                        infoTienda = UsuariosTiendas(
                            usuario=infoUsuario,
                            tienda_id=tienda.get('id_tienda')
                        )

                        infoTienda.save()
                else:
                    pass
                if infoUsuario.rol.zonal == True:
                    zona_tienda = Zonas.objects.filter(id_zona=zona).first()
                    zona_id = zona_tienda.id_zona
                    tiendas = Tiendas.objects.filter(zona_id=zona_id)
                    for tienda in tiendas:
                        infoTienda = UsuariosTiendas(
                                usuario = infoUsuario,
                                tienda=tienda
                            )
                        infoTienda.save()
                else:
                    # return JsonResponse({'mensaje': 'No ah seleccionado ninguna zona'},status=500)
                    pass


                return JsonResponse({
                    'correo': infoUsuario.email,
                    'redireccion': 1
                    })
        else:
            if usuario.rol.zonal == True:
                zona_tienda = Zonas.objects.filter(id_zona=zona).first()
                zona_tienda = zona_tienda.id_zona
                tiendas = Tiendas.objects.filter(zona=zona_tienda)

            else:
                zona = usuario.zona


            if Usuarios.objects.filter(email=email).\
                    exclude(id=usuario.id).exists():
                return JsonResponse(
                    {'mensaje': 'Correo ya se encuentra registrado'},
                    status=500
                    )

            usuario.rol = rol
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.telefono = telefono
            usuario.usuario_modifica = request.user.id
            usuario.fecha_modificacion = datetime.datetime.now()
            usuario.zona = zona
            usuario.usuario_telegram = usuario_telegram
                        
            usuario.save()
            if grupo_empresarial:
                user_grupoempresarial = UsuariosGruposEmpresariales(
                    usuario = usuario,
                    grupo_empresarial = grupo_empresarial
                )
                user_grupoempresarial.save()
            if taller:
                user_t = UsuariosTalleres.objects.filter(taller_id=taller.id_taller, usuario_id=usuario.id)
                if user_t:
                    user_t.delete()
                
                user_taller = UsuariosTalleres(usuario_id=usuario.id, taller_id=taller.id_taller)
                user_taller.save()
                    
            grupoUsuario = UsuariosGrupos.objects.\
                filter(usuarios_id=usuario.id).first()
            grupoUsuario.group = rol.grupo
            grupoUsuario.save()

            tiendas_asignadas = UsuariosTiendas.objects.\
                filter(usuario=usuario)

            for t in tiendas_asignadas:
                t.delete()
                    
            if len(tiendas) > 0:

                if type(tiendas) is list:
                    for tienda in tiendas:
                        infoTienda = UsuariosTiendas(
                            usuario=usuario,
                            tienda_id=tienda.get('id_tienda')
                        )
                        infoTienda.save()
                else:
                    for tienda in tiendas:
                        infoTienda = UsuariosTiendas(
                                usuario = usuario,
                                tienda=tienda
                            )
                        infoTienda.save()

            
            return JsonResponse({
                    'correo': usuario.email,
                    'redireccion': 2
                    })

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_usuarios',
                     login_url='bases:sin_permisos')
def InactivarUsuarioModal(request, id_usuario):
    template_name = 'usr/inactivar_usuario_modal.html'
    contexto = {}
    usuario = Usuarios.objects.filter(pk=id_usuario).first()

    if not usuario:
        return HttpResponse('No existe el usuario ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'usuario': usuario}

    if request.method == 'POST':
        usuario.is_active = False
        usuario.save()
        return HttpResponse('Usuario inactivado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_usuarios',
                     login_url='bases:sin_permisos')
def ActivarUsuarioModal(request, id_usuario):
    template_name = 'usr/activar_usuario_modal.html'
    contexto = {}
    usuario = Usuarios.objects.filter(pk=id_usuario).first()

    if not usuario:
        return HttpResponse('No existe el usuario ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'usuario': usuario}

    if request.method == 'POST':
        usuario.is_active = True
        usuario.save()
        return HttpResponse('Usuario activado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('usr.change_usuarios',
                     login_url='bases:sin_permisos')
def ReestablecerContrasenaModal(request, id_usuario):
    template_name = 'usr/reestablecer_contrasena_modal.html'
    contexto = {}
    usuario = Usuarios.objects.filter(pk=id_usuario).first()

    if not usuario:
        return HttpResponse('No existe el usuario ' + str(id_usuario))

    if request.method == 'GET':
        contexto = {'usuario': usuario}

    if request.method == 'POST':
        longitud = 6
        valores = \
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        tmp_pass = ""
        tmp_pass = tmp_pass.join([choice(valores) for i in range(longitud)])
        tmp_pass.replace(" ", "")

        password = make_password(tmp_pass, salt=None, hasher='default')
        usuario.password = password
        # usuario.nueva_clave = True
        usuario.save()
        enviarCorreoContrasena.delay(usuario.id, tmp_pass, 2)
        return HttpResponse('Usuario activado')

    return render(request, template_name, contexto)


def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success = "Cambio de password listo."
            return redirect('bases:home')
        else:
            messages.error(request, 'Error al cambiar contraseña')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usr/cambiar_contrasena.html', {
        'form': form
    })


@login_required(login_url='/login/')
def cambiar_contrasena_modal(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            usuario = Usuarios.objects.\
                filter(username=request.user.username).first()
            # usuario.nueva_clave = False
            usuario.save()
            return redirect("bases:login")
        else:
            messages.error(request, 'Error al cambiar contraseña')
            return render(request, 'usr/cambiar_contrasena_inicial.html', {
                'form': form
            })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usr/cambiar_contrasena_inicial.html', {
        'form': form
    })


def contrasena_olvidada(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        correo = json_data['correo']
        usuario = Usuarios.objects.filter(email=correo).first()
        if usuario:
            longitud = 6
            valores = \
                "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            tmp_pass = ""
            tmp_pass = \
                tmp_pass.join([choice(valores) for i in range(longitud)])
            tmp_pass.replace(" ", "")

            password = make_password(tmp_pass, salt=None, hasher='default')
            usuario.password = password
            # usuario.nueva_clave = True
            usuario.save()
            enviarCorreoContrasena.delay(usuario.id, tmp_pass, 2)
            return JsonResponse({'content': {'message': 'enviada'}})
        else:
            return JsonResponse({'content': {'message': 'no enviada'}})
    return render(request, 'usr/contrasena_olvidada.html')


class VerificarCorreo(APIView):
    def post(self, request):
        datos = json.loads(request.body)
        email = (datos.get('correo'))
        usuario = Usuarios.objects.\
            filter(email=email).first()
        if usuario:
            respuesta = {'existe': True}
        else:
            respuesta = {'existe': False}
        return Response(respuesta)
