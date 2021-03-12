from django.urls import path
from django.contrib.auth import views as auth_views

from .views import TipoUsuarioView, TipoUsuarioFormView, RolListaView,\
     UsuarioListaView, RolesPermisos, UsuariosForm,\
     InactivarUsuarioModal, ActivarUsuarioModal, ReestablecerContrasenaModal,\
     cambiar_contrasena, EditarPerfil, RolesCrearView, RolesEditarView, \
     cambiar_contrasena_modal, ActualizarRolModal, contrasena_olvidada,\
     VerificarCorreo, tiendas_jefezonal

urlpatterns = [
     path('tipos/lista',
          TipoUsuarioView.as_view(),
          name='tipo_usuarios_lista'
          ),
     path('tipos/crear',
          TipoUsuarioFormView.as_view(),
          name='tipo_usuario_nuevo'
          ),
     path('rol/lista',
          RolListaView.as_view(),
          name='roles_lista'
          ),
     path('rol/actualizar/<int:pk>',
          ActualizarRolModal,
          name='roles_actualizar'
          ),
     path('rol/crear/<int:rol_id>',
          RolesPermisos,
          # RolesCrearView.as_view(),
          name='roles_crear'
          ),
     path('rol/editar/<int:pk>',
          RolesEditarView.as_view(),
          name='roles_editar'
          ),
     # path('rol/permisos/<int:rol_id>',
     #      RolesPermisos,
     #      name='roles_permisos'
     #      ),
     path('usuario/lista/',
          UsuarioListaView.as_view(),
          name='usuario_lista'
          ),
     path('usuario/registro/<int:pk>',
          UsuariosForm,
          name='usuarios_form'
          ),
     path('contrasena_nuevo_usuario/',
          auth_views.PasswordResetView.as_view(
               template_name='usr/contrasena_olvidada.html',
               email_template_name='usr/correo_nuevo_usuario.html',
               subject_template_name='usr/asunto_correo_usuario_nuevo.txt'
          ),
          name='contrasena_nuevo_usuario'
          ),
     path('usuario/editar/perfil/<int:pk>',
          EditarPerfil.as_view(),
          name='usuario_editar_perfil'
          ),
     path('usuario/inactivar_modal/<int:id_usuario>',
          InactivarUsuarioModal,
          name='usuario_inactivar_modal'
          ),
     path('usuario/activar_modal/<int:id_usuario>',
          ActivarUsuarioModal,
          name='usuario_activar_modal'
          ),
     path('usuario/res_contrasena/<int:id_usuario>',
          ReestablecerContrasenaModal,
          name='usuario_reinicia_contrasena'
          ),
     path('usuario/contrasena/cambiar/',
          cambiar_contrasena,
          name='usuario_cambiar_contrasena'
          ),
     path('usuario/contrasena/cambiar/inicial/',
          cambiar_contrasena_modal,
          name='usuario_cambiar_contrasena_modal'
          ),
     path('usuario/contrasena_olvidada/',
          contrasena_olvidada,
          name='usuario_contrasena_olvidada'
          ),
     path('usuario/verificar-correo/',
          VerificarCorreo.as_view(),
          name='verificar_correo'
          ),
     path('usuario/ajax/tiendaszonal/', tiendas_jefezonal, name="tiendas_jefezonal"),

]
