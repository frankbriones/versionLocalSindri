*****************
**Modelos prv**
*****************

Dentro de la carpeta **prv** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación prv

Modelo Proveedores
===================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los proveedores que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "identificacion","Identificación del proveedor registrado."
        "nombres", "Nombre del proveedor."
        "apellidos", "Apellidos del proveedor."
        "direccion", "Dirección del proveedor."
        "telefono", "Número de teléfono del proveedor."
        "correo", "Dirección de correo electrónico del proveedor."
        "zona", "Id de la zona a la que pertenece el proveedor."
        "ciudad", "Id de la ciudad a la pertene el proveedor."
        "estado", "Id del estado del país puede ser activo o inactivo."
        "tipo_usuario","Indica qué tipo de usuario creó el proveedor."
        "taller", "Id del taller al que pertenece el proveedor."
        "porcentaje_merma", "Porcentaje de merma asignado al proveedor."
        "escala_peso", "Escala de peso para fabricaciones del proveedor."
