****************
**Tareas ntf**
****************

Dentro de la carpeta **ntf** tenemos el archivo llamado ``tasks.py``. Donde se encuentran las tareas en segundo plano de la aplicación ntf

Tarea crearNotificacionTaller
==============================

Tarea que genera una nueva notificación afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_usuario_genera", "Id del usuario que genera la notificación."
        "id_taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "producto", "Descripción del producto por el cual se genera la notificación."
        "principal", "Indica si la notificación debe ser mostrada en la pantalla principal de la aplicación."
        "id_usuario_recibe", "Id del usuario que recibe la notificación."
        "postergada", "Indica si la notificación se generó después de postergar una notificación anterior."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "id_estado", "Id del estado en que se encuentra la transacción."

Tarea NotificacionSolicitudCreada
==================================

Tarea que genera una nueva notificación de solicitud creada afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_usuario_genera", "Id del usuario que genera la notificación."
        "id_taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "producto", "Descripción del producto por el cual se genera la notificación."
        "principal", "Indica si la notificación debe ser mostrada en la pantalla principal de la aplicación."
        "id_usuario_recibe", "Id del usuario que recibe la notificación."
        "postergada", "Indica si la notificación se generó después de postergar una notificación anterior."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "id_estado", "Id del estado en que se encuentra la transacción."

Tarea NotificacionSolicitudCotizada
====================================

Tarea que genera una nueva notificación de solicitud cotizada afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_usuario_genera", "Id del usuario que genera la notificación."
        "id_taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "producto", "Descripción del producto por el cual se genera la notificación."
        "principal", "Indica si la notificación debe ser mostrada en la pantalla principal de la aplicación."
        "id_usuario_recibe", "Id del usuario que recibe la notificación."
        "postergada", "Indica si la notificación se generó después de postergar una notificación anterior."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "id_estado", "Id del estado en que se encuentra la transacción."

Tarea NotificacionOrdenes
==================================

Tarea que genera una nueva notificación de órden generada afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_usuario_genera", "Id del usuario que genera la notificación."
        "id_taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "producto", "Descripción del producto por el cual se genera la notificación."
        "principal", "Indica si la notificación debe ser mostrada en la pantalla principal de la aplicación."
        "id_usuario_recibe", "Id del usuario que recibe la notificación."
        "postergada", "Indica si la notificación se generó después de postergar una notificación anterior."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "id_estado", "Id del estado en que se encuentra la transacción."

Tarea NotificacionEvaluarSolicitud
===================================

Tarea que genera una nueva notificación de solicitud en evaluación afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."

Tarea NotificacionLimiteVenta
===================================

Tarea que genera una nueva notificación que indica al usuario que se ha cumplido el plazo para finalizar una órden de trabajo, afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."

Tarea NotificacionOrdenesActualizar
====================================

Tarea que actualiza el estado de una notificación afectando al :ref:`Modelo Notificaciones`, para la generación de la notificación recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_usuario_genera", "Id del usuario que genera la notificación."
        "id_taller", "Id del taller al que pertenece el usuario que recibe la notificación."
        "id_usuario_recibe", "Id del usuario que recibe la notificación."
        "id_transaccion", "Id de la transacción por la cual se generó la notificación."
        "tipo_transaccion", "Indica el tipo de transacción por la que se generó la notificación."
        "id_estado", "Id del estado en que se encuentra la transacción."
