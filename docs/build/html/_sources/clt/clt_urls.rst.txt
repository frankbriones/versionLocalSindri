***************
**URLs clt**
***************

Dentro de la carpeta **clt** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación clt, se detalla a continuación cada ruta

url clientes_lista
====================

``/clientes/lista`` Ruta hacia la pantalla del listado de clientes registrados para un país determinado, hace un llamado a la :ref:`Vista ClientesListaView`.

url clientes_crear
===================

``/clientes/crear`` Ruta hacia la pantalla que permite crear un cliente para un país determinado, hace un llamado a la :ref:`Vista ClientesCrearView`.

url clientes_editar
====================

``/clientes/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un cliente para un país determinado, hace un llamado a la :ref:`Vista ClientesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del cliente a editar ``id_cliente``."

url clientes_actualizar
=========================

``/clientes/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un cliente para un país determinado, hace un llamado a la :ref:`Vista ActualizarClienteModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del cliente a editar ``id_cliente``."

url clientes_lista_api
=========================

``/clientes/buscar`` Ruta utilizada para la consulta de los clientes registrados en el sistema, hace un llamado a la :ref:`Vista ClientesListaAPIView`.

url clientes_buscar
=====================

``/clientes/buscar/<str:identificacion>`` Ruta utilizada para la consulta de un cliente específico, hace un llamado a la :ref:`Vista BusquedaCliente`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"identificacion","De tipo caracter, se refiere a la identificación del cliente a consultar ``identificacion``."

url clientes_modal
=====================

``/clientes/modal/<int:id_trn>/<int:tipo>`` Ruta utilizada para la creación de un cliente, hace un llamado a la :ref:`Vista ClientesCrearModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_trn","De tipo entero, se refiere al id de la transacción a registrar ``id_solicitud``."
	"tipo","De tipo entero, se refiere al tipo de transacción a registrar."
