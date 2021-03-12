***************
**URLs usr**
***************

Dentro de la carpeta **usr** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación usr, se detalla a continuación cada ruta

url tipo_usuarios_lista
========================

``/tipos/lista`` Ruta hacia la pantalla del listado de tipos de usuarios registrados en el sistema, hace un llamado a la :ref:`Vista TipoUsuarioView`.

url roles_lista
====================

``/rol/lista`` Ruta hacia la pantalla del listado de roles de usuarios registrados en el sistema, hace un llamado a la :ref:`Vista RolListaView`.

url roles_actualizar
=====================

``/rol/actualizar/<int:pk>`` Ruta hacia el modal que permite activar o inactivar un rol de usuario determinado, hace un llamado a la :ref:`Vista ActualizarRolModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del rol a editar."

url roles_crear
=====================

``/rol/crear`` Ruta hacia la pantalla que permite crear un rol de usuario en el sistema, hace un llamado a la :ref:`Vista RolesCrearView`.

url roles_editar
=====================

``/rol/editar/<int:pk>`` Ruta hacia el modal que permite editar un rol de usuario determinado, hace un llamado a la :ref:`Vista RolesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del rol a editar."

url roles_permisos
=====================

``/rol/permisos/<int:rol_id>`` Ruta hacia la pantalla que permite asignar permisos a un rol de usuario determinado, hace un llamado a la :ref:`Vista RolesPermisos`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del rol al que se le asignan los permisos."

url usuario_lista
====================

``/usuario/lista`` Ruta hacia la pantalla del listado de usuarios registrados en el sistema, hace un llamado a la :ref:`Vista UsuarioListaView`.

url usuario_registro
=====================

``/usuario/registro`` Ruta hacia la pantalla que permite crear un usuario en el sistema, hace un llamado a la :ref:`Vista RegistroUsuario`.

url usuario_editar
====================

``/usuario/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un usuario determinado, hace un llamado a la :ref:`Vista Editar`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del usuario a editar ``id``."

url usuario_editar_perfil
==========================

``/usuario/editar/perfil/<int:pk>`` Ruta hacia la pantalla que permite a un usuario editar su información, hace un llamado a la :ref:`Vista EditarPerfil`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del usuario a editar ``id``."

url usuario_inactivar_modal
============================

``/usuario/inactivar_modal/<int:id_usuario>`` Ruta que abre el modal para inactivar un usuario de un país determinado, hace un llamado a la :ref:`Vista InactivarUsuarioModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_usuario","De tipo entero, se refiere al id del usuario a inactivar ``id``."

url usuario_activar_modal
============================

``/usuario/activar_modal/<int:id_usuario>`` Ruta que abre el modal para activar un usuario de un país determinado, hace un llamado a la :ref:`Vista ActivarUsuarioModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_usuario","De tipo entero, se refiere al id del usuario a activar ``id``."

url usuario_cambiar_contrasena
===============================

``/usuario/contrasena/cambiar`` Ruta hacia la pantalla que permite a un usuario cambiar su contraseña actual, hace un llamado a la :ref:`Vista cambiar_contrasena`.

url usuario_cambiar_contrasena_modal
=====================================

``/usuario/contrasena/cambiar/inicial`` Ruta hacia la pantalla que permite a un usuario cambiar su contraseña actual al ingresar por primera vez al sistema después de ser registrado o después del reestablecimiento de su contraseña, hace un llamado a la :ref:`Vista cambiar_contrasena_modal`.

url usuario_reinicia_contrasena
================================

``/usuario/res_contrasena/<int:id_usuario>`` Ruta hacia la pantalla que permite a un usuario administrador reestablecer la contraseña de un usuario determinado, hace un llamado a la :ref:`Vista ReestablecerContrasenaModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_usuario","De tipo entero, se refiere al id del usuario al que se reestablece la contraseña ``id``."
