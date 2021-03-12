*******************
**Views Bases**
*******************

Dentro de la carpeta **bases** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación bases, se detalla a continuación cada vista.

Vista Home
==========

Vista basada en clases que hace el llamado al :ref:`Template home`. Esta vista hace uso del ``LoginRequiredMixin`` propio de Django para validar si el usuario se encuentra autenticado, de no ser así el sistema lo redirige al LoginRequiredMixin.

Vista user_login
================

Vista basada en funciones, se encarga de validar las credenciales introducidas por el usuario desde la pantalla de login, hace uso del ``EmailBackend`` para la validación, de existir un usuario con las credenciales ingresadas pasa a validar si la clave del usuario es nueva ``if request.user.nueva_clave`` de ser ese el caso lo redirige hacia la pantalla de actualizar contraseña, caso contrario lo redirige a la pantalla home.

Vista Logout
============

Vista basada en clases, hace el llamado al :ref:`Template logout`, también hace uso del ``LoginRequiredMixin`` para validar si el usuario se encuentra autenticado.

Vista SinPermisosTemplate
=========================

Vista basada en clases, hace el llamado al :ref:`Template sin_premisos`, que indicará al usuario que no cuenta con los permisos para visualizar la pantalla a la que intenta acceder.

Vista error404Template
======================

Vista basada en clases, hace el llamado al :ref:`Template error404`, que indica al usuario que está intentando acceder a una ruta que no existe o no disponible por el momento.

Vista SinPermisos
=================

Vista basada en clases, se encarga de validar si el usuario cuenta con los permisos necesarios para acceder a una ruta determinada, para ello hace uso de dos Mixins propios de Django ``LoginRequiredMixin`` y  ``PermissionRequiredMixin``, el primero para validar si el usuario se encuentra autenticado y el segundo para consultar si el usuario cuenta con el permiso para ejecutar una vista determinada. Para la validación del permiso en cada vista que herede de la vista SinPermisos se debe especificar cuál es el permiso requerido, en caso de que el usuario no cuente con el permiso indicado será redirigido a la pantalla Sin permisos.
