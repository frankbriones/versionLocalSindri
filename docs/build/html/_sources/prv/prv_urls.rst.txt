***************
**URLs prv**
***************

Dentro de la carpeta **prv** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación prv, se detalla a continuación cada ruta

url proveedores_lista
======================

``/proveedores/lista`` Ruta hacia la pantalla del listado de proveedores registrados en el sistema, hace un llamado a la :ref:`Vista ProveedoresListaView`.

url proveedores_crear
======================

``/proveedores/crear`` Ruta hacia la pantalla que permite crear un proveedor en el sistema, hace un llamado a la :ref:`Vista ProveedoresCrearView`.

url proveedores_editar
=======================

``/proveedores/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un proveedor determinado, hace un llamado a la :ref:`Vista ProveedoresEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del proveedor a editar."

url proveedores_actualizar
===========================

``/proveedores/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un proveedor para un país determinado, hace un llamado a la :ref:`Vista ActualizarProveedorModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del proveedor a editar."
