*******************
**Views clt**
*******************

Dentro de la carpeta **clt** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación clt, se detalla a continuación cada vista.

Vista ClientesListaView
========================

Vista basada en clases, hace el llamado al :ref:`Template clientes_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``clt.view_clientes`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el ``Modelo Clientes`` obteniendo el listado de los clientes filtrando por país.

Vista ClientesCrearView
========================

Vista basada en clases que hace el llamado al :ref:`Template clientes_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``clt.add_clientes`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Clientes` mediante el uso del formulario :ref:`Formulario ClientesForm`. Esta vista crea un nuevo registro de cliente para un país determinado.

Vista ClientesEditarView
=========================

Vista basada en clases que hace el llamado al :ref:`Template clientes_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``clt.change_clientes`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Clientes` mediante el uso del formulario :ref:`Formulario ClientesForm`. Esta vista actualiza los valores de un cliente determinado.

Vista ActualizarClienteModal
==============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_cliente_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``clt.change_clientes`` respectivamente para acceder a la misma, reliza el proceso de activar o inactivar un cliente, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"cliente", "Objeto del cliente que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un cliente:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista ClientesModalView
=========================

Vista basada en clases que hace el llamado al :ref:`Template clientes_modal`. Esta vista hereda de la clase genérica de Django ``generic.TemplateView`` se trata de una vista para instanciar al modal de cliente.

Vista ClientesListaAPIView
===========================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar los clientes de un país determinado, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene todos los clientes registrados en el sistema. Para procesar los datos obtenidos se utiliza el :ref:`Serializador ClientesSerializer`, luego se envía la respuesta al template.

Vista BusquedaCliente
=======================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la informacion de un cliente determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"identificacion", "Número de identificación del cliente."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ClientesSerializer`, luego se envía la respuesta al template.

Vista ClientesCrearModal
==========================

Vista basada en funciones, hace el llamado al :ref:`Template clientes_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``clt.add_clientes`` respectivamente para acceder a la misma, realiza el proceso de registrar un cliente, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "form", "Instancia del :ref:`Formulario ClientesForm`."
        "id_trn", "Id de la transacción que se genera."
        "tipo", "Tipo de transacción que se realiza."

Método POST
------------
Recibe los siguientes datos en formato JSON para crear un cliente:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
        "identificacion", "Identificación del cliente, cédula o pasaporte."
        "nombres", "Nombres del cliente."
        "apellidos","Apellidos del cliente."
        "correo", "Dirección de correo electrónico del cliente."
        "telefono", "Número telefónico del cliente."
        "direccion", "Dirección del domicilio del cliente"
        "ciudad", "Id de la ciudad a la que pertenece el cliente."
