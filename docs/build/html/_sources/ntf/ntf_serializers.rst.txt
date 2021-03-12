***********************
**Serializadores ntf**
***********************

Dentro de la carpeta **ntf** tenemos el archivo llamado ``serializers.py``. Donde se encuentran los serializadores de la aplicación ntf

Serializador NotificacionesSerializer
=======================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Notificaciones`. Este es el serializador utilizado para las consultas de las notificaciones que se generan en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_notificacion","Id de la notificación que se genera."
        "usuario_genera", "Id del usuario que genera la notificación."
        "usuario_nombre", "Username del usuario que genera la notificación."
        "usuario_recibe", "Id del usuario que recibe la notificación."
        "taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "taller_nombre", "Nombre del taller al que se le genera la notificación."
        "nombre_producto", "Descripción del producto por el cual se generó la notificación."
        "vista", "Indica si la notificación ha sido vista o no."
        "principal", "Indica si la notificación debe ser mostrada en la pantalla principal de la aplicación."
        "postergada", "Indica si la notificación se generó después de postergar una notificación anterior."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "estado", "Id del estado en que se encuentra la transacción."
        "estado_nombre", "Descripción del estado de la transacción."
        "fecha_creacion", "Fecha en que se generó la notificación."
        "fecha_modificacion", "Fecha de modificación de la notificación."
