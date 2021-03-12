***************
**URLs trn**
***************

Dentro de la carpeta **trn** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación trn, se detalla a continuación cada ruta

url solicitudes_lista
======================

``/solicitudes/lista`` Ruta hacia la pantalla del listado de solicitudes de trabajo registradas para un usuario o taller determinado, hace un llamado a la :ref:`Vista SolicitudesListaView`.

url solicitudes_api_lista
==========================

``/solicitudes/lista`` Ruta hacia la pantalla del listado de solicitudes de trabajo registradas para un usuario o taller determinado, hace un llamado a la :ref:`Vista SolicitudesListaAPIView`.

url solicitudes_api_lista_fecha
=================================

``/solicitudes/list/fecha/api/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite consultar las solicitudes correspondientes a un rango de fecha para un usuario o taller determinado, hace un llamado a la :ref:`Vista SolicitudesListaFechaAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."

url solicitudes_crear
======================

``/solicitudes/crear/<int:tipo>/<int:pk>`` Ruta hacia la pantalla que permite crear una solicitud de trabajo, hace un llamado a la :ref:`Vista SolicitudesCrearView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"tipo","De tipo entero, se refiere al tipo de solicitud a crear."
		"pk", "De tipo entero, se refiere al id del ítem asociado a la solicitud."

url solicitudes_tipo
======================

``/solicitudes/tipo/<int:id_item>`` Ruta hacia el modal que permite al usuario escoger el tipo de solicitud a realizar, hace un llamado a la :ref:`Vista TipoSolicitudView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"id_item", "De tipo entero, se refiere al id del ítem asociado a la solicitud."

url solicitudes_editar
=======================

``/solicitudes/editar/<int:pk>`` Ruta hacia la pantalla que permite al usuario editar los valores de una solicitud, hace un llamado a la :ref:`Vista SolicitudesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"pk", "De tipo entero, se refiere al id de la solicitud a editar."

url solicitudes_detalle
========================

``/solicitudes/detalle/modal/<int:id_solicitud>/<int:accion>`` Ruta que abre el modal que contiene la información detallada de una solicitud determinada, hace un llamado a la :ref:`Vista SolicitudDetalleView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_solicitud","De tipo entero, se refiere al id de la solicitud a consultar."
	"accion", "De tipo entero, se refiere a la acción a realizar sobre la solicitud."

url solicitar_externo
========================

``/solicitudes/solicitarexterno/<int:pk>`` Ruta hacia la pantalla que permite al usuario realizar una solicitud externa, hace un llamado a la :ref:`Vista SolicitarAExternoView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la solicitud de la cual se generará la solicitud externa."

url generar_orden_solicitud
============================

``/solicitudes/generarordensolicitud/<int:pk>`` Ruta que actualiza los datos de una solicitud de la cual se generará una órden de trabajo, hace un llamado a la :ref:`Vista GenerarOrdenSolicitudView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la solicitud a la cual se actualizará los datos."

url ordenes_lista
==========================

``/ordenes/lista`` Ruta hacia la pantalla del listado de órdenes de trabajo registradas para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenesListaView`.

url ordenes_api_lista
======================

``/ordenes/lista/api/<int:limite>`` Ruta hacia la pantalla del listado de órdenes de trabajo registradas para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenesListaAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"limite","De tipo entero, se refiere a la cantidad de registros obtenidos en la consulta."

url ordenes_api_lista_fecha
=================================

``/ordenes/lista/fecha/api/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite consultar las órdenes correspondientes a un rango de fecha para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenesListaFechaAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."

url ordenes_pagos_lista
==========================

``/ordenes/pagos/lista`` Ruta hacia la pantalla del listado de pagos de órdenes de trabajo registradas para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenesPagosListaView`.

url ordenes_pagos_api_lista
=================================

``/ordenes/lista/pagos/api/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite consultar los pagos de las órdenes correspondientes a un rango de fecha para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenesPagosListaAPIView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."

url ordenes_tipo
======================

``/ordenes/tipo`` Ruta hacia el modal que permite al usuario escoger el tipo de órden a realizar, hace un llamado a la :ref:`Vista TipoOrdenView`.

url ordenes_solicitud_crear
============================

``/ordenes/solicitudcrear/<int:id_trn>/<str:identificacion>`` Ruta hacia la pantalla que permite al usuario crear una órden a partir de una solicitud, hace un llamado a la :ref:`Vista CrearOrdenSolicitudView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_trn","De tipo entero, se refiere al id de la solicitud de la cual se realizará la órden."
	"identificacion", "Identificación del cliente."

url ordenes_item_crear
============================

``/ordenes/itemcrear/<int:id_trn>/<str:identificacion>`` Ruta hacia la pantalla que permite al usuario crear una órden a partir de un ítem de catálogo, hace un llamado a la :ref:`Vista CrearOrdenItemView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_trn","De tipo entero, se refiere al id del ítem del cual se realizará la órden."
	"identificacion", "Identificación del cliente."

url ordenes_detalle
========================

``/ordenes/detalles/modal/<int:id_orden>`` Ruta que abre el modal que contiene la información detallada de una órden para un usuario o taller determinado, hace un llamado a la :ref:`Vista OrdenDetalleView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden a consultar."

url ordenes_agregar_piedra
============================

``/ordenes/piedras/agregar/<int:id_orden>/<int:id_piedra>`` Ruta que abre el modal que permite al usuario agregar una piedra a una órden determinada, hace un llamado a la :ref:`Vista AgregarPiedraView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden a la cual se le agregará la piedra."
	"id_piedra","De tipo entero, se refiere al id de la piedra a agregar."

url ordenes_agregar_adicional
===============================

``/ordenes/adicionales/agregar/<int:id_orden>/<int:id_adicional>`` Ruta que abre el modal que permite al usuario agregar un adicional a una órden determinada, hace un llamado a la :ref:`Vista AgregarAdicionalView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden a la cual se le agregará el adicional."
	"id_adicional","De tipo entero, se refiere al id del adicional a agregar."

url envio_material
===============================

``/ordenes/enviomaterial/<int:pk>`` Ruta que permite al usuario registrar el envío de material de una órden determinada, hace un llamado a la :ref:`Vista EnvioMaterialView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url recibe_material
===============================

``/ordenes/recibematerial/<int:pk>`` Ruta que permite al usuario registrar la recepción de material de una órden determinada, hace un llamado a la :ref:`Vista RecibirMaterialView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url anular_orden
===============================

``/ordenes/anularorden/<int:pk>`` Ruta que permite al usuario registrar la anulación de una órden determinada, hace un llamado a la :ref:`Vista AnularOrdenView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url finalizar_trabajo
===============================

``/ordenes/finalizartrabajo/<int:pk>`` Ruta que permite al usuario registrar la finalización del trabajo de fabricación de una órden determinada, hace un llamado a la :ref:`Vista FinalizarTrabajoView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url enviar_producto
===============================

``/ordenes/enviarproducto/<int:pk>`` Ruta que permite al usuario registrar el envío del producto de una órden determinada, hace un llamado a la :ref:`Vista EnviarProductoView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url recibir_producto
===============================

``/ordenes/recibirproducto/<int:pk>`` Ruta que permite al usuario registrar la recepción del producto de una órden determinada, hace un llamado a la :ref:`Vista RecibirProductoView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url cargar_doc_taller
===============================

``/ordenes/cargardoctaller/<int:pk>`` Ruta que permite al usuario registrar la carga de documentos por pate del taller de una órden determinada, hace un llamado a la :ref:`Vista CargarDocumentosTaller`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url cargar_doc_ope
===============================

``/ordenes/cargardocope/<int:pk>`` Ruta que permite al usuario registrar la carga de documentos por pate de la joyería de una órden determinada, hace un llamado a la :ref:`Vista CargarDocumentosOperaciones`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url devolver_producto
===============================

``/ordenes/devolverproducto/<int:pk>`` Ruta que permite al usuario registrar la devolución del producto de una órden determinada, hace un llamado a la :ref:`Vista DevolverProductoView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url finalizar_orden
===============================

``/ordenes/finalizarorden/<int:pk>`` Ruta que permite al usuario registrar la finalización de una órden con venta, hace un llamado a la :ref:`Vista FinalizarOrdenView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url finalizar_sin_venta
===============================

``/ordenes/finalizarsinventa/<int:pk>`` Ruta que permite al usuario registrar la finalización de una órden sin venta, hace un llamado a la :ref:`Vista FinalizarSinVentaView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la órden de trabajo."

url orden_aprobacion_pago
===============================

``/ordenes/aprobacion/pago/modal/<int:id_orden>`` Ruta hacia el modal que permite al usuario aprobar el pago de una órden determinada, hace un llamado a la :ref:`Vista AprobacionPagoModalView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden de trabajo."

url correo_cliente
===============================

``/ordenes/enviarcorreocliente`` Ruta que permite al usuario el envío de correo al cliente, hace un llamado a la :ref:`Vista EnviarCorreoView`.

url correo_cliente_tmp
===============================

``/correo/correocliente/<int:id_orden>`` Ruta que permite al usuario el envío de correo al cliente, hace un llamado a la :ref:`Vista CorreoTemplateView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden de trabajo de la cual se enviará la información."

url comprobante_tmp
===============================

``/comprobante/<int:id_orden>`` Ruta que permite al usuario generar el comprobante de una órden determinada, hace un llamado a la :ref:`Vista ComprobanteTemplateView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_orden","De tipo entero, se refiere al id de la órden de trabajo de la cual se generará el comprobante."

url rep_ordenes
===============================

``/reporte/ordenes/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite al usuario generar un repórte de órdenes generadas dentro de un rango de fechas para un usuario o taller determinado, hace un llamado a la :ref:`Vista ReporteOrdenesListaView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."

url rep_ordenes_admin_op
===============================

``/reporte/ordenes/adminop/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite al usuario generar un repórte de órdenes generadas dentro de un rango de fechas para el usuario administrador de operaciones, hace un llamado a la :ref:`Vista ReporteOrdenesAdminOpView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."

url rep_pagos_aprobados
===============================

``/reporte/aprobacion/pagos/<str:f_inicio>/<str:f_fin>/<int:opcion>`` Ruta que permite al usuario generar un repórte de pago de órdenes generadas dentro de un rango de fechas determinado, hace un llamado a la :ref:`Vista ReporteOrdenesPagos`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

		"f_inicio","De tipo string, se refiere a la fecha inicial del rango de la consulta."
		"f_fin","De tipo string, se refiere a la fecha final del rango de la consulta."
		"opcion", "De tipo entero, se refiere al tipo de consulta que se realiza."
