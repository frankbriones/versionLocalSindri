*****************
**Modelos clt**
*****************

Dentro de la carpeta **clt** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación clt

Modelo Clientes
================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para clientes que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_cliente","Id del cliente registrado."
        "identificacion", "Identificación del cliente, cédula o pasaporte."
        "nombres", "Nombres del cliente."
        "apellidos","Apellidos del cliente."
        "correo", "Dirección de correo electrónico del cliente."
        "telefono", "Número telefónico del cliente."
        "direccion", "Dirección del domicilio del cliente"
        "ciudad", "Id de la ciudad a la que pertenece el cliente."
        "pais", "Id del país al que pertenece el cliente."
        "estado", "Id del estado del cliente puede ser activo o inactivo."
