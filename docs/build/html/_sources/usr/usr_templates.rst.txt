*******************
**Templates usr**
*******************

Dentro de la carpeta **usr** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación usr correspondiente a la creación, consulta y modificación de clientes en el sistema.

Template activar_usuario_modal
==================================

Template del modal que aparecerá cuando se requiere activar un usuario, las funciones que posee este template son las siguientes:

Función activarUsuario
--------------------------

Realiza una petición de tipo POST a la :ref:`url usuario_activar_modal` enviando como parámetro el id del usuario a activar.

Template actualizar_rol_modal
==================================

Template del modal que aparecerá cuando se requiere activar o inactivar un rol de usuario, las funciones que posee este template son las siguientes:

Función actualizarRol
--------------------------

Realiza una petición de tipo POST a la :ref:`url roles_actualizar` enviando como parámetro el id del rol a activar o inactivar.

Template cambiar_contrasena_inicial
=====================================

Template de la pantalla que aparecerá cuando el usuario ingresa por primera vez al sistema después de haber sido creado o después de un reestablecimiento de su contraseña, realiza una petición de tipo POST a la :ref:`url usuario_cambiar_contrasena_modal` para modificar la contraseña inicial que le asignó al usuario.

Template cambiar_contrasena
============================

Template de la pantalla que permite a un usuario cambiar su propia contraseña, realiza una petición de tipo POST a la :ref:`url usuario_cambiar_contrasena` para modificar la contraseña actual del usuario.

Template editar_perfil
=======================

Template de la pantalla que permite a un usuario modificar su propia información, realiza una petición de tipo POST a la :ref:`url usuario_editar_perfil` para modificar la información actual del usuario.

Template editar_usuario
========================

Template de la pantalla que permite a un usuario administrador modificar la información de otro usuario, realiza una petición de tipo POST a la :ref:`url usuario_editar` para modificar la información del usuario seleccionado.

Template inactivar_usuario_modal
==================================

Template del modal que aparecerá cuando se requiere inactivar un usuario, las funciones que posee este template son las siguientes:

Función inactivarUsuario
--------------------------

Realiza una petición de tipo POST a la :ref:`url usuario_inactivar_modal` enviando como parámetro el id del usuario a inactivar.

Template reestablecer_contrasena_modal
=======================================

Template del modal que aparecerá cuando se requiere reestablecer la contraseña de un usuario, las funciones que posee este template son las siguientes:

Función reiniciaContrasena
----------------------------

Realiza una petición de tipo POST a la :ref:`url usuario_reinicia_contrasena` enviando como parámetro el id del usuario a quien se le reestablece la contraseña.

Template registro
===================

Template de la pantalla que permite crear un usuario para un país determinado, realiza una petición de tipo POST a la :ref:`url usuario_registro` para registrar el nuevo usuario.

Template roles_form
=======================

Template de la pantalla que permite crear o editar un rol de usuario, realiza una petición de tipo POST a la :ref:`url roles_crear` en caso de creación de un rol, y una petición de tipo POST a la :ref:`url roles_editar` en caso de modificar los datos de un rol enviando como parámetro el id del rol a editar.

Template roles_lista
========================

Template de la pantalla para consultar los roles de usuario que pertenezcan a un taller o empresa determinados. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_rol_modal` y a la pantalla de creación o edición de roles :ref:`Template roles_form`. Para la consulta de los roles de usuarios se realiza una petición de tipo GET a la :ref:`url roles_lista`.

Template roles_permisos_form
=======================================

Template de la pantalla que permite al usuario asignar los permisos de acceso a un rol, las funciones que posee este template son las siguientes:

Función guardarRol
----------------------------

Realiza una petición de tipo POST a la :ref:`url roles_permisos` enviando como parámetro el id del rol al que se le asignan los permisos, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"permisos[]", "Listado de permisos que se le asignan al rol."

Template tipo_usuarios_lista
=============================

Template de la pantalla para consultar los tipos de usuarios registrados en el sistema.

Template usuarios_lista
========================

Template de la pantalla para consultar todos los usuarios que pertenezcan al mismo país. Desde esta pantalla se puede acceder a la pantalla de creación de usuarios :ref:`Template registro` y a la pantalla de edición de usuarios :ref:`Template editar_usuario`. Para la consulta de los usuarios se realiza una petición de tipo GET a la :ref:`url usuario_lista`.
