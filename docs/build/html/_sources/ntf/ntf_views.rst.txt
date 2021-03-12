*******************
**Views ntf**
*******************

Dentro de la carpeta **ntf** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación ntf, se detalla a continuación cada vista.

Vista ObtenerNotificacionesUsuarioView
=======================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las notificaciones de un usuario determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"id_usuario", "Id del usuario del cual se consultan las notificaciones."
		"limite", "Cantidad de registros que se van a devolver en la consulta."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador NotificacionesSerializer`, luego se envía la respuesta al template.

Vista ObtenerNotificacionesTallerView
=======================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las notificaciones de un taller determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"id_taller", "Id del taller del cual se consultan las notificaciones."
		"limite", "Cantidad de registros que se van a devolver en la consulta."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador NotificacionesSerializer`, luego se envía la respuesta al template.

Vista PrimeraNotificacionesUsuarioView
=======================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar la primera notificación que se encuentre en estado **PRODUCTO RECIBIDO** o **no vista** de un usuario determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"id_usuario", "Id del usuario del cual se consultan las notificaciones."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador NotificacionesSerializer`, luego se envía la respuesta al template.

Vista PrimeraNotificacionesTallerView
=======================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar la primera notificación que se encuentre en estado **ESPERA COTIZACION TALLER** o **no vista** de un taller determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"id_taller", "Id del taller del cual se consultan las notificaciones."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador NotificacionesSerializer`, luego se envía la respuesta al template.

Vista ActualizarNotificacionView
=================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para actualizar una notificación cambiando el valor del campo vista a True, cuenta con las siguientes acciones:

Método POST
------------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"pk","Id de la notificación que se va a actualizar."
