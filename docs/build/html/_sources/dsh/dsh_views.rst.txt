*******************
**Views dsh**
*******************

Dentro de la carpeta **dsh** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación dsh, se detalla a continuación cada vista.

Vista DashboardAdminOpeAPIView
================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener todos los datos que se presentan en el panel de estadísticas para el administrador de operaciones, los datos corresponden a las órdenes generadas por todas las joyerías del país al que pertenece el administrador, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"totales_por_estado", "Arreglo que contiene las cantidades de órdenes generadas con su estado."
		"producto_mas_cotizado", "Objeto del ítem que ha sido más cotizado en un periodo de tiempo."
		"totales_int_ext", "Arreglo que contiene las cantidades de órdenes generadas identificando si son internas o externas."
		"gramos_fabricados", "Cantidad total de gramos fabricados en un periodo de tiempo."
		"producto_mas_fabricado", "Objeto del ítem que ha sido más fabricado en un periodo de tiempo."
		"fabricaciones_por_mes", "Arreglo que contiene las cantidades de órdenes fabricadas por mes."
		"categoria_mas_fabricada", "Objeto de la categoría que ha sido más fabricada en un periodo de tiempo."
		"color_mas_fabricado", "Objeto del color de fabricación más solicitado en un periodo de tiempo."
		"gramos_por_joyeria", "Arreglo que contiene la cantidad de gramos fabricados por joyería."
		"fecha_inicio", "Fecha de inicio del rango de tiempo de la consulta."
		"fecha_fin", "Fecha fin del rango de tiempo de la consulta."

Vista DashboardAdminTalAPIView
================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener todos los datos que se presentan en el panel de estadísticas para el administrador de taller, los datos corresponden a las órdenes fabricadas por el taller al que pertenece el administrador, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"totales_por_estado", "Arreglo que contiene las cantidades de órdenes generadas con su estado."
		"producto_mas_cotizado", "Objeto del ítem que ha sido más cotizado en un periodo de tiempo."
		"solicitudes_por_estado", "Arreglo que contiene las cantidades de solicitudes generadas con su estado."
		"gramos_fabricados", "Cantidad total de gramos fabricados en un periodo de tiempo."
		"producto_mas_fabricado", "Objeto del ítem que ha sido más fabricado en un periodo de tiempo."
		"fabricaciones_por_mes", "Arreglo que contiene las cantidades de órdenes fabricadas por mes."
		"categoria_mas_fabricada", "Objeto de la categoría que ha sido más fabricada en un periodo de tiempo."
		"color_mas_fabricado", "Objeto del color de fabricación más solicitado en un periodo de tiempo."
		"gramos_por_joyeria", "Arreglo que contiene la cantidad de gramos fabricados por joyería."
		"fecha_inicio", "Fecha de inicio del rango de tiempo de la consulta."
		"fecha_fin", "Fecha fin del rango de tiempo de la consulta."

Vista DashboardAdminOpeView
============================

Vista basada en clases, hace el llamado al :ref:`Template dashboard_operaciones`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.estadisticas_admin`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.TemplateView``, esta vista es utilizada para mostrar el panel de estadísticas para el administrador de operaciones.

Vista DashboardAdminTalView
============================

Vista basada en clases, hace el llamado al :ref:`Template dashboard_taller`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.estadisticas_admin`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.TemplateView``, esta vista es utilizada para mostrar el panel de estadísticas para el administrador del taller.
