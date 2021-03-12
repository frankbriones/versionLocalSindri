*******************
**Views usr**
*******************

Dentro de la carpeta **usr** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación usr, se detalla a continuación cada vista.

Vista TipoUsuarioView
=======================

Vista basada en clases, hace el llamado al :ref:`Template tipo_usuarios_lista`. Esta vista hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo TipoUsuarios` obteniendo el listado de los tipo de usuarios registrados en el sistema.

Vista RolListaView
=======================

Vista basada en clases, hace el llamado al :ref:`Template roles_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.view_roles`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Roles` obteniendo el listado de los roles de usuario registrados en el sistema.

Vista UsuarioListaView
=======================

Vista basada en clases, hace el llamado al :ref:`Template usuarios_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.view_usuarios`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Usuarios` obteniendo el listado de los usuarios registrados en el sistema.

Vista Editar
=============

Vista basada en clases que hace el llamado al :ref:`Template editar_usuario`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_usuarios`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Usuarios` mediante el uso del formulario :ref:`Formulario EditarUsuarioForm`. Esta vista permite a un usuario administrador actualizar la información de un usuario determinado.

Vista EditarPerfil
===================

Vista basada en clases que hace el llamado al :ref:`Template editar_perfil`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_usuarios`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Usuarios` mediante el uso del formulario :ref:`Formulario EditarPerfilForm`. Esta vista permite a un usuario actualizar su propia información.

Vista RolesCrearView
=====================

Vista basada en clases que hace el llamado al :ref:`Template roles_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.add_roles`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Roles` mediante el uso del formulario :ref:`Formulario RolForm`. Esta vista permite a un usuario administrador crear un nuevo rol de usuario.

Vista RolesEditarView
======================

Vista basada en clases que hace el llamado al :ref:`Template roles_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.add_roles`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Roles` mediante el uso del formulario :ref:`Formulario RolForm`. Esta vista permite a un usuario administrador editar la información de un rol de usuario.

Vista RolesPermisos
=======================

Vista basada en funciones, hace el llamado al :ref:`Template roles_permisos_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.add_roles`` respectivamente para acceder a la misma, realiza el proceso de asignar los permisos a un rol de usuario, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template, en caso de existir alguna excepción al crear el usuario:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"permisos_admin", "Permisos disponibles para la asignación."
		"rol", "Objeto del rol al que se le van a asignar los permisos."
		"permisos_rol", "Permisos asignados actualmente al rol."
		"form_rol", "Instancia del :ref:`Formulario RolGrupoForm`."
		"contenidos", "Listado de aplicaciones a las que pertenecen los permisos."
		"modulos", "Listado de nombres de permisos."
		"permisos_asignados", "Permisos asignados actualmente al rol en formato JSON."

Método POST
------------
Recibe los siguientes datos en formato JSON para asignar permisos a un rol de usuario:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"permisos[]","Listado de permisos que se asignan al rol de usuario."

Vista ActualizarRolModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_rol_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_roles`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un rol de usuario, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rol", "Objeto del rol que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un rol:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista RegistroUsuario
=======================

Vista basada en funciones, hace el llamado al :ref:`Template registro`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.add_usuarios`` respectivamente para acceder a la misma, realiza el proceso crear un usuario, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template, en caso de existir alguna excepción al crear el usuario:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"usuario", "Objeto del usuario consultado."
		"form", "Instancia del :ref:`Formulario UsuarioGrupoForm`."
		"estandar_tallas", "Listado de estándar de tallas."

Método POST
------------
Recibe los siguientes datos en formato JSON para crear un usuario:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"usuario-rol", "Id del rol asignado al usuario."
		"usuario-username","Username del usuario nuevo."
		"usuario-first_name","Nombres del usuario nuevo."
		"usuario-last_name","Apellidos del usuario nuevo."
		"usuario-email","Correo del usuario nuevo."
		"usuario-direccion", "Dirección del usuario."
        "usuario-telefono", "Teléfono del usuario."
		"usuario-ciudad", "Id de la ciudad a la que pertenece el usuario."
		"usuario-sector", "Id del sector al que pertenece el usuario."
		"usuario-img_perfil","Url de la imagen de perfil del usuario nuevo."
		"usuario-observacion", "Observación sobre el usuario."
		"nombre_taller","Nombre del taller."
        "valor_fraccion", "Valor del gramo de fabricación para el taller."
		"tiempo_respuesta", "Tiempo límite para responder una solicitud."
		"escala_peso", "Escala de peso en la que puede ser fabricado un ítem."
		"estandar", "Estandar de tallas que maneja el taller."
		"costo_base_taller", "Valor de gramo de materia prima."
        "utilidad_taller", "Porcentaje de utilidad que se aplica sobre los costos de fabricación."
		"utilidad", "Porcentaje de utilidad que se aplicará sobre los costos del taller."
		"tmp_venta","Cantidad en días que representa el tiempo límite para finalizar una orden de trabajo."
		"externo", "Indica si tiene permitido generar directamente ordenes con un proveedor externo."
		"descuento", "Pocentaje máximo de descuento permitido para las órdenes de trabajo."
		"nombre_empresa","Nombre de la empresa."
		"costo_base_operaciones", "Costo del gramo base de la joyería."

Se genera una contraseña temporal aleatoria la cual se envía por correo electrónico al nuevo usuario.

Vista InactivarUsuarioModal
============================

Vista basada en funciones, hace el llamado al :ref:`Template inactivar_usuario_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_usuarios`` respectivamente para acceder a la misma, realiza el proceso de inactivar un usuario, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"usuario", "Objeto del usuario que se va a modificar de ser el caso."

Método POST
------------
Inactiva el usuario modificando el campo ``is_active`` dandole el valor **False**.

Vista ActivarUsuarioModal
==========================

Vista basada en funciones, hace el llamado al :ref:`Template activar_usuario_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_usuarios`` respectivamente para acceder a la misma, realiza el proceso de activar un usuario, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"usuario", "Objeto del usuario que se va a modificar de ser el caso."

Método POST
------------
Activa el usuario modificando el campo ``is_active`` dandole el valor **True**.

Vista ReestablecerContrasenaModal
==================================

Vista basada en funciones, hace el llamado al :ref:`Template reestablecer_contrasena_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_usuarios`` respectivamente para acceder a la misma, permite al usuario administrador reestablecer la contraseña de un usuario determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"usuario", "Objeto del usuario al que se va a reestablecer la contraseña."

Método POST
------------
Genera una contraseña aleatoria y envía la misma al usuario por correo electrónico.

Vista cambiar_contrasena
==========================

Vista basada en funciones, hace el llamado al :ref:`Template cambiar_contrasena`. Permite a un usuario modificar su contraseña actual, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"form", "Formulario de autenticación de Django ``PasswordChangeForm`` cuenta con todas las reglas de contraseñas para validar si la nueva contraseña a registrar es segura."

Método POST
------------
Valida si la contraseña ingresada por el usuario es segura y actualiza la misma.

Vista cambiar_contrasena_modal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template cambiar_contrasena_inicial`. Permite a un usuario modificar su contraseña actual al ingresar por primera vez al sistema después de ser registrado en el sistema o después del reestablecimiento de su contraseña, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"form", "Formulario de autenticación de Django ``PasswordChangeForm`` cuenta con todas las reglas de contraseñas para validar si la nueva contraseña a registrar es segura."

Método POST
------------
Valida si la contraseña ingresada por el usuario es segura y actualiza la misma.
