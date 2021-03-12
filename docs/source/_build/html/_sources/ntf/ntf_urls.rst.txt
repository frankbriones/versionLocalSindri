***************
**URLs cfg**
***************

Dentro de la carpeta **cfg** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación cfg, se detalla a continuación cada ruta

url notificaciones_usuario_lista
=================================

``/usuario/lista/<int:id_usuario>/<int:limite>`` Ruta para obtener las notificaciones de un usuario determinado, hace un llamado a la :ref:`Vista ObtenerNotificacionesUsuarioView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"id_usuario","De tipo entero, se refiere al id del usuario a consultar ``id``."
		"limite","De tipo entero, se refiere a la cantidad de registros que va a devolver la consulta."

url notificaciones_taller_lista
=================================

``/taller/lista/<int:id_taller>/<int:limite>`` Ruta para obtener las notificaciones de un taller determinado, hace un llamado a la :ref:`Vista ObtenerNotificacionesTallerView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"id_taller","De tipo entero, se refiere al id del taller a consultar ``id_taller``."
		"limite","De tipo entero, se refiere a la cantidad de registros que va a devolver la consulta."

url notificaciones_usuario_primera
===================================

``/usuario/primera/<int:id_usuario>`` Ruta para obtener la primera notificación no contestada de un usuario determinado, hace un llamado a la :ref:`Vista PrimeraNotificacionesUsuarioView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"id_usuario","De tipo entero, se refiere al id del usuario a consultar ``id``."

url notificaciones_taller_primera
===================================

``/taller/primera/<int:id_taller>`` Ruta para obtener la primera notificación no contestada de un taller determinado, hace un llamado a la :ref:`Vista PrimeraNotificacionesTallerView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"id_taller","De tipo entero, se refiere al id del taller a consultar ``id_taller``."

url notificacion_actualizar
============================

``/actualizar/<int:pk>`` Ruta para actualizar una notificación de un país determinado, hace un llamado a la :ref:`Vista ActualizarNotificacionView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la notificación a actualizar ``id_notificacion``."
