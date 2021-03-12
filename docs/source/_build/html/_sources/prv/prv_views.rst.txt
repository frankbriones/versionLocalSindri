*******************
**Views prv**
*******************

Dentro de la carpeta **prv** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación prv, se detalla a continuación cada vista.

Vista ProveedoresListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template proveedores_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``prv.view_proveedores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Proveedores` obteniendo el listado de los proveedores registrados en el sistema.

Vista ProveedoresCrearView
===========================

Vista basada en clases que hace el llamado al :ref:`Template proveedores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``prv.add_proveedores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Proveedores` mediante el uso del formulario :ref:`Formulario ProveedorForm`. Esta vista crea un nuevo registro de proveedor para un país determinado.

Vista ProveedoresEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template proveedores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``prv.change_proveedores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Proveedores` mediante el uso del formulario :ref:`Formulario ProveedorForm`. Esta vista actualiza los valores de un proveedor determinado.

Vista ActualizarProveedorModal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_proveedor_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``prv.change_proveedores`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un proveedor, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"proveedor", "Objeto del proveedor que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un proveedor:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."
