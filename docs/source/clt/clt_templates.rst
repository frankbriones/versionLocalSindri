*******************
**Templates clt**
*******************

Dentro de la carpeta **clt** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación clt correspondiente a la creación, consulta y modificación de clientes en el sistema.

Template actualizar_cliente_modal
==================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un cliente, las funciones que posee este template son las siguientes:

Función actualizarCliente
--------------------------

Realiza una petición de tipo POST a la :ref:`url clientes_actualizar` enviando como parámetro el id del cliente a actualizar

Template clientes_form
=======================

Template de la pantalla que permite crear o editar un cliente para un país determinado, realiza una petición de tipo POST a la :ref:`url clientes_crear` en caso de creación de un cliente, y una petición de tipo POST a la :ref:`url clientes_editar` en caso de modificar los datos de un cliente enviando como parámetro el id del cliente a editar.

Template clientes_lista
========================

Template de la pantalla para consultar todos los clientes que pertenezcan a la misma empresa. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_cliente_modal` y a la pantalla de creación o edición de clientes :ref:`Template clientes_form`, esta pantalla es solo para los usuarios de tipo operaciones y que posean el permiso para ver clientes. Para la consulta de los clientes se realiza una petición de tipo GET a la :ref:`url clientes_lista`.

Template clientes_modal
==================================

Template del modal que aparecerá cuando el usuario desea consultar un cliente en específico, las funciones que posee este template son las siguientes:

Función buscarCliente
-----------------------

Realiza una petición de tipo GET a la :ref:`url clientes_buscar` enviando como parámetro el número de identificación del cliente. De existir un cliente con la identificación ingresada carga los datos del mismo, caso contrario le consulta al usuario si desea crearlo.

Función habilitarGuardado
--------------------------

Habilita los elementos del formulario para la creación del cliente.

Función borrarDatos
---------------------

Borra los valores ingresados en los elementos del formulario para la creación del cliente.

Función guardarCliente
-----------------------

Función para crear un nuevo cliente validando que la identificación no esté registrada previamente. Realiza una petición de tipo POST a la :ref:`url clientes_modal`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"identificacion","Identificación del cliente nuevo."
	"nombres","Nombres del cliente a registrar."
	"apellidos","Apellidos del cliente a registrar."
	"ciudad","Ciudad a la que pertenece el cliente."
	"direccion","Dirección del cliente."
	"telefono","Teléfono del cliente."
	"correo","Correo del cliente."

Función generarOrden
-----------------------

Realiza un redireccionamiento a la :ref:`url ordenes_solicitud_crear` enviando como parámetros el número de identificación del cliente y el número de transacción esto aplica para solicitudes internas y externas.
