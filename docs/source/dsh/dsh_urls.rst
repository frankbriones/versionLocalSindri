***************
**URLs dsh**
***************

Dentro de la carpeta **dsh** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación dsh, se detalla a continuación cada ruta

url dashboard_operaciones
==========================

``/adminop/`` Ruta hacia la pantalla del panel de estadísticas para el administrador de operaciones, hace un llamado a la :ref:`Vista DashboardAdminOpeView`.

url dashboard_taller
==========================

``/adminta/`` Ruta hacia la pantalla del panel de estadísticas para el administrador de taller, hace un llamado a la :ref:`Vista DashboardAdminTalView`.

url dashboard_usuario_api
===========================

``/adminop/api/<int:opcion>/<str:f_inicio>/<str:f_fin>`` Ruta para obtener los datos para el panel de estadísticas para el administrador de operaciones, hace un llamado a la :ref:`Vista DashboardAdminOpeAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"opcion","De tipo entero, se refiere al tipo de consulta que realiza el usuario."
		"f_inicio", "De tipo string, se refiere a la fecha de inicio del periodo a consultar."
		"f_fin", "De tipo string, se refiere a la fecha fin del periodo a consultar."

url dashboard_taller_api
===========================

``/adminta/api/<int:opcion>/<str:f_inicio>/<str:f_fin>`` Ruta para obtener los datos para el panel de estadísticas para el administrador de taller, hace un llamado a la :ref:`Vista DashboardAdminTalAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"opcion","De tipo entero, se refiere al tipo de consulta que realiza el usuario."
		"f_inicio", "De tipo string, se refiere a la fecha de inicio del periodo a consultar."
		"f_fin", "De tipo string, se refiere a la fecha fin del periodo a consultar."
