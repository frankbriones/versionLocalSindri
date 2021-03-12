*******************
**Views trn**
*******************

Dentro de la carpeta **trn** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación trn, se detalla a continuación cada vista.

Vista SolicitudesListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template solicitudes_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.view_solicitudtrabajo`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo SolicitudTrabajo` obteniendo el listado de las solicitudes de trabajo registradas filtrando por usuario o por taller.

Vista SolicitudesListaAPIView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las solicitudes registradas filtrando por usuario o por taller.

Vista SolicitudesListaFechaAPIView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las solicitudes registradas filtrando por usuario o por taller determinado en un rango de fechas, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"f_inicio", "Fecha de inicio del rango de fecha para la consulta."
		"f_fin", "Fecha fin del rango de fecha para la consulta."
		"opcion", "Tipo de consulta que realiza el usuario."

Las opciones de consulta son las siguientes:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"Opción 1", "Devuelve todas las solicitudes correspondientes al mes actual para un usuario o taller determinado."
		"Opción 2", "Devuelve todas las solicitudes correspondientes al mes anterior para un usuario o taller determinado."
		"Opción 3", "Devuelve las últimas 100 solicitudes registradas para un usuario o taller determinado."
		"Opción 4", "Devuelve las últimas 1000 solicitudes registradas para un usuario o taller determinado."
		"Opción 5", "Devuelve todas las solicitudes generadas entre la fecha inicio y la fecha fin para un usuario o taller determinado."
		"Opción 6", "Devuelve todas las solicitudes registradas para un usuario o taller determinado."

Vista TipoSolicitudView
============================

Vista basada en clases, hace el llamado al :ref:`Template tipo_solicitud_modal`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.view_solicitudtrabajo`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.TemplateView`` envía al template la información del ítem y del proveedor para generar la solicitud.

Vista SolicitudesCrearView
===========================

Vista basada en clases que hace el llamado al :ref:`Template solicitudes_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.add_solicitudtrabajo`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo SolicitudTrabajo` mediante el uso del formulario :ref:`Formulario SolicitudDetalleForm`. Esta vista crea un nuevo registro de solicitud de trabajo para un país determinado registrando también los detalles de la misma y los rubros asociados agregados por el usuario.

Vista SolicitudesEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template solicitudes_editar_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_solicitudtrabajo`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo SolicitudTrabajo` mediante el uso del formulario :ref:`Formulario SolicitudEditarForm`. Esta vista actualiza los valores de una solicitud determinada.

Vista SolicitudDetalleView
=============================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_solicitud_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_solicitudtrabajo`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una transacción recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"solicitud", "Objeto de la solicitud que se consulta."
		"item", "Id del ítem asociado a la solicitud"
		"utilidad_fab_op", "Porcentaje de utilidad sobre la fabricación configurado para la joyería."
		"configuracion_op", "Parámetros configurados para la joyería."
		"configuracion_ta", "Parámetros configurados para el taller o proveedor."
		"rubros", "Lista de rubros registrados en el sistema para el taller o proveedor."
		"rubros_asociados", "Rubros asociados a la solicitud de trabajo consultada."

Método POST
------------
Registra una respuesta para la solicitud de trabajo por parte del taller 1 para cotización, 2 para evaluación y 3 para rechazo. Recibe los siguientes datos en formato JSON:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"rubros_lista[]","Arreglo que contiene los rubros asignados a la solicitud."
		"peso_min","Peso mínimo de fabricación para el producto estipulado por el taller."
		"peso_max","Peso máximo de fabricación para el producto estipulado por el taller."
		"valor_gramo", "Costo por gramo de oro asignado a la solicitud."
		"valor_error", "Costo que se puede adicionar o restar del precio calculado para la fabricación, dependiendo del peso final del producto."
		"tiempo_ent_min", "Tiempo mínimo necesario para la entrega del producto."
		"tiempo_ent_max", "Tiempo máximo necesario para la entrega del producto."
		"total_rubros", "Costo total de los rubros asociados a la solicitud."
		"prct_util_sobre_fabrica_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
		"prct_impuestos_ta", "Porcentaje de impuestos cobrados por el taller."
		"tiempo_dias", "Cantidad de días necesarios para la evaluación."
		"tiempo_horas", "Cantidad de horas necesarias para la evaluación."
		"tiempo_minutos", "Cantidad de minutos necesarios para la evaluación."
		"observacion_ta", "Observación del por qué se rechaza la solicitud."

Vista GenerarOrdenSolicitudView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para actualizar los datos de una solicitud de trabajo de la cual se generará una orden basados en el peso de fabricación seleccionado por el usuario, cuenta con las siguientes acciones:

Método POST
------------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"pk", "Id de la solicitud de la cual se generará una órden de trabajo."

Vista SolicitarAExternoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para generar una solicitud externa a partir de una solicitud rechazada por el taller, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"pk", "Id de la solicitud de la cual se generará una solicitud externa."

Vista OrdenesListaView
============================

Vista basada en clases, hace el llamado al :ref:`Template ordenes_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.view_ordentrabajo`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo OrdenTrabajo` obteniendo el listado de las órdenes de trabajo registradas filtrando por un usuario o taller determinado.

Vista OrdenesListaAPIView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las órdenes registradas filtrando por usuario o por taller.

Vista OrdenesListaFechaAPIView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar las órdenes registradas filtrando por usuario o por taller determinado en un rango de fechas, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"f_inicio", "Fecha de inicio del rango de fecha para la consulta."
		"f_fin", "Fecha fin del rango de fecha para la consulta."
		"opcion", "Tipo de consulta que realiza el usuario."

Las opciones de consulta son las siguientes:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"Opción 1", "Devuelve todas las órdenes correspondientes al mes actual para un usuario o taller determinado."
		"Opción 2", "Devuelve todas las órdenes correspondientes al mes anterior para un usuario o taller determinado."
		"Opción 3", "Devuelve las últimas 100 órdenes registradas para un usuario o taller determinado."
		"Opción 4", "Devuelve las últimas 1000 órdenes registradas para un usuario o taller determinado."
		"Opción 5", "Devuelve todas las órdenes generadas entre la fecha inicio y la fecha fin para un usuario o taller determinado."
		"Opción 6", "Devuelve todas las órdenes registradas para un usuario o taller determinado."

Vista OrdenesPagosListaView
============================

Vista basada en clases, hace el llamado al :ref:`Template ordenes_pagos_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.view_ordentrabajo`` para acceder a la misma.

Vista OrdenesPagosListaAPIView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para consultar los pagos de órdenes registrados filtrando por usuario o por taller determinado en un rango de fechas, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"f_inicio", "Fecha de inicio del rango de fecha para la consulta."
		"f_fin", "Fecha fin del rango de fecha para la consulta."
		"opcion", "Tipo de consulta que realiza el usuario."

Las opciones de consulta son las siguientes:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"Opción 1", "Devuelve todos los pagos correspondientes al mes actual para un usuario o taller determinado."
		"Opción 2", "Devuelve todos los pagos correspondientes al mes anterior para un usuario o taller determinado."
		"Opción 3", "Devuelve todos los pagos generados entre la fecha inicio y la fecha fin para un usuario o taller determinado."
		"Opción 4", "Devuelve todos los pagos registrados para un usuario o taller determinado."

Vista TipoOrdenView
============================

Esta vista hereda de la clase genérica de Django ``generic.TemplateView``, se utiliza para deplegar el modal de los tipos de órdenes.

Vista CrearOrdenSolicitudView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template ordenes_solicitud_crear`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.add_ordentrabajo`` respectivamente para acceder a la misma. Esta vista es utilizada para generar una órden de trabajo a partir de una solicitud, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una transacción recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"solicitud", "Objeto de la solicitud de la cual se generará la orden de trabajo."
		"cliente", "Objeto del cliente por el cual se realiza la órden de trabajo."

Método POST
------------
Registra una órden de trabajo con los datos de la solicitud y del cliente. Recibe los siguientes datos en formato JSON:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"env_material","Indica si la joyería envía o no materia prima hacia el taller."

Vista CrearOrdenItemView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template ordenes_item_crear`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.add_ordentrabajo`` respectivamente para acceder a la misma. Esta vista es utilizada para generar una órden de trabajo a partir de un ítem de catálogo, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una transacción recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"item", "Objeto del ítem del cual se generará la orden de trabajo."
		"cliente", "Objeto del cliente por el cual se realiza la órden de trabajo."
		"detalles", "Listado de los detalles que pertenecen al ítem."
		"colores", "Listado de colores en los que está disponible el ítem para su fabricación."
		"utilidad_fab_op", "Porcentaje de utilidad sobre la fabricación configurado para la joyería."
		"configuracion_op", "Parámetros configurados para la joyería."
		"configuracion_ta", "Parámetros configurados para el taller."
		"origen_material", "Listado de los orígenes de material disponibles."
		"origen_pre", "Id del orígen de material preestablecido en el sistema."

Método POST
------------
Registra una órden de trabajo con los datos del ítem y del cliente. Recibe los siguientes datos en formato JSON:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"adicionales_lista[]","Arreglo que contiene los id's de los adicionales agregados a la órden."
		"tipo_transaccion", "Tipo de transacción a realizar."
		"id_detalle_item", "Id del detalle de ítem seleccionado."
		"id_color", "Id del color seleccionado."
		"env_material", "Indica si la joyería envía o no materia prima hacia el taller."
		"costo", "Costo total del taller."
		"precio", "Precio de la órden."
		"precio_sistema", "Precio de la órden calculado por el sistema."
		"adicional_color_gramo", "Costo adicional por gramo de fabricación debido al color de la joya."
		"peso_solicitado", "Peso del producto solicitado por el cliente."
		"util_sobre_base_op", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por la joyería."
		"util_base_op", "Valor de utilidad obtenido sobre la materia prima suministrada por la joyería."
		"util_sobre_base_ta", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por el taller."
		"util_base_ta", "Valor de utilidad obtenido sobre la materia prima suministrada por el taller."
		"servicio_fab", "Costo total de la mano de obra para la fabricación."
		"utilidad_fab_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
		"util_fab_ta", "Valor de utilidad obtenido sobre la fabricación para el taller."
		"utilidad_fab_op", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por la joyería."
		"util_fab_op", "Valor de utilidad obtenido sobre la fabricación para la joyería."
		"costo_gr_base_op", "Costo del gramo de oro estipulado por la joyería."
		"costo_gr_base_ta", "Costo del gramo de oro estipulado por el taller."
		"costo_gramo_fabricado", "Costo de gramo de fabricación."
		"costo_adicionales", "Costo de los adicionales agregados a la órden de trabajo."
		"precio_adicionales", "Precio total de adicionales sumada la utilidad para el taller."
		"precio_adicionales_op", "Precio total de adicionales sumada la utilidad para la joyería."
		"costo_piedras", "Costo de piedras agregadas a la órden."
		"precio_piedras", "Precio total de piedras sumada la utilidad para el taller."
		"precio_piedras_op", "Precio total de piedras sumada la utilidad para la joyería."
		"util_sobre_piedras", "Utilidad sobre las piedras obtenida por el taller."
		"util_sobre_piedras_op", "Utilidad sobre las piedras obtenida por la joyería."
		"util_sobre_adicionales", "Utilidad sobre los adicionales obtenida por el taller."
		"util_sobre_adicionales_op", "Utilidad sobre los adicionales obtenida por la joyería."
		"origen_material", "Origen de la materia prima para la fabricación."
		"prct_impuesto", "Porcentaje de impuestos cobrados por la joyería."
		"impuestos_orden", "Valor de impuestos cobrado por la joyería."
		"prct_impuestos_ta", "Porcentaje de impuestos cobrados por el taller."
		"impuestos_ta", "Valor de impuestos cobrado por el taller."
		"precio_total_adicionales", "Precio total de adicionales agregados a la órden."
		"precio_gramo_final", "Costo por gramo de oro en caso de manejarse un precio fijo."
		"costo_piedras_basicas", "Costo de piedras registrado para el ítem de la órden de trabajo."
		"datos_extra", "Datos adicionales sobre la fabricación."

Vista OrdenDetalleView
=============================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_orden_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_ordentrabajo`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una transacción recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"orden", "Objeto de la órden que se consulta."
		"item", "Id del ítem asociado a la órden."
		"detalle", "Detalle del ítem asociado a la órden."
		"detalleSolicitud", "Detalle de la solicitud asociada a la órden."
		"sintalla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"adicionales_lista", "Lista de los adicionales agregados a la órden."
		"peso_max_arc", "Peso máximo para un archivo cargado por el usuario."
		"ext_perm_arc", "Extensiones permitidas para los archivos cargados por el usuario."

Método POST
------------
Registra un cambio de estado para la órden que se consulta. Recibe los siguientes datos en formato JSON:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"estado","Estado al que debe pasar la órden de trabajo."

Vista CorreoTemplateView
=============================

Vista basada en funciones, hace el llamado al :ref:`Template correo_cliente`. Esta vista envía información de una órden de trabajo a un template para luego ser enviado mediante correo electrónico al cliente, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una órden recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"orden", "Objeto de la órden que se consulta."
		"item", "Id del ítem asociado a la órden."
		"detalle", "Detalle del ítem asociado a la órden."
		"detalleSolicitud", "Detalle de la solicitud asociada a la órden."
		"sintalla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"costo_adicionales", "Costo total de los adicionales agregados a la órden de trabajo."
		"adicionales_lista", "Lista de los adicionales agregados a la órden."
		"sUrl", "Path del directorio raíz de los archivos del proyecto."
		"precio_final", "Precio final de la órden de trabajo."
		"usuario", "Usuario que realiza la petición."

Vista CorreoZonalTemplateView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template correo_producto_recibido`. Esta vista envía información de una órden de trabajo a un template para luego ser enviado mediante correo electrónico al jefe zonal, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una órden recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"orden", "Objeto de la órden que se consulta."
		"item", "Id del ítem asociado a la órden."
		"detalle", "Detalle del ítem asociado a la órden."
		"detalleSolicitud", "Detalle de la solicitud asociada a la órden."
		"sintalla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"costo_adicionales", "Costo total de los adicionales agregados a la órden de trabajo."
		"adicionales_lista", "Lista de los adicionales agregados a la órden."
		"sUrl", "Path del directorio raíz de los archivos del proyecto."
		"precio_final", "Precio final de la órden de trabajo."
		"usuario", "Usuario que realiza la petición."

Vista ComprobanteTemplateView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template comprobante_orden`. Esta vista envía información de una órden de trabajo a un template para luego ser impresa a modo de comprobante, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene los detalles de una órden recibiendo su id como parámetro. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"orden", "Objeto de la órden que se consulta."
		"item", "Id del ítem asociado a la órden."
		"detalle", "Detalle del ítem asociado a la órden."
		"detalleSolicitud", "Detalle de la solicitud asociada a la órden."
		"sintalla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"costo_adicionales", "Costo total de los adicionales agregados a la órden de trabajo."
		"adicionales_lista", "Lista de los adicionales agregados a la órden."
		"sUrl", "Path del directorio raíz de los archivos del proyecto."
		"usuario", "Usuario que realiza la petición."

Vista ReporteOrdenesListaView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template reporte_lista_ordenes`. Esta vista envía información a un template para luego generar un reporte con el listado de órdenes de trabajo consultadas y sus detalles para una joyería o taller determinado, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene la información de las órdens recibiendo como parámetros la fecha inicio y fin de la consulta y la Opción de consulta. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"ordenes", "Listado de órdenes de trabajo consultadas."
		"taller", "Taller que realiza la consulta."
		"usuario", "Usuario que realiza la consulta."
		"fecha_inicio", "Fecha de inicio del rango de la consulta."
		"fecha_fin", "Fecha de fin del rango de la consulta."
		"opcion", "Opción de consulta de usuario."
		"solicitudes", "Listado de solicitudes que no han recibido respuesta al momento de generar el reporte."
		"sUrl", "Path del directorio raíz de los archivos del proyecto."

Las opciones de consulta son las siguientes:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"Opción 1", "Devuelve todas las órdenes correspondientes al mes actual para un usuario o taller determinado."
		"Opción 2", "Devuelve todas las órdenes correspondientes al mes anterior para un usuario o taller determinado."
		"Opción 3", "Devuelve las últimas 100 órdenes registradas para un usuario o taller determinado."
		"Opción 4", "Devuelve las últimas 1000 órdenes registradas para un usuario o taller determinado."
		"Opción 5", "Devuelve todas las órdenes generadas entre la fecha inicio y la fecha fin para un usuario o taller determinado."
		"Opción 6", "Devuelve todas las órdenes registradas para un usuario o taller determinado."

Vista ReporteOrdenesAdminOpView
================================

Vista basada en funciones, hace el llamado al :ref:`Template reporte_lista_ordenes`. Esta vista envía información a un template para luego generar un reporte con el listado de órdenes de trabajo consultadas y sus detalles para el administrador de operaciones, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene la información de las órdens recibiendo como parámetros la fecha inicio y fin de la consulta y la Opción de consulta. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"ordenes", "Listado de órdenes de trabajo consultadas."
		"taller", "Taller que realiza la consulta."
		"usuario", "Usuario que realiza la consulta."
		"fecha_inicio", "Fecha de inicio del rango de la consulta."
		"fecha_fin", "Fecha de fin del rango de la consulta."
		"opcion", "Opción de consulta de usuario."
		"solicitudes", "Listado de solicitudes que no han recibido respuesta al momento de generar el reporte."
		"sUrl", "Path del directorio raíz de los archivos del proyecto."

Las opciones de consulta son las siguientes:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"Opción 1", "Devuelve todas las órdenes correspondientes al mes actual para un usuario o taller determinado."
		"Opción 2", "Devuelve todas las órdenes correspondientes al mes anterior para un usuario o taller determinado."
		"Opción 3", "Devuelve las últimas 100 órdenes registradas para un usuario o taller determinado."
		"Opción 4", "Devuelve las últimas 1000 órdenes registradas para un usuario o taller determinado."
		"Opción 5", "Devuelve todas las órdenes generadas entre la fecha inicio y la fecha fin para un usuario o taller determinado."
		"Opción 6", "Devuelve todas las órdenes registradas para un usuario o taller determinado."

Vista AgregarPiedraView
=============================

Vista basada en funciones, hace el llamado al :ref:`Template agregar_piedra_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_ordentrabajo`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene la información de una piedra para que el usuario pueda agregarla a la órden de trabajo. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"piedra", "Objeto de la piedra que se consulta."
		"detalles_piedra", "Listado de detalles que pertenecen a la piedra."
		"id_orden", "Id de la órden que se está generando."
		"utilidad_fab_op", "Porcentaje de utilidad sobre la piedra configurado para la joyería."

Vista AgregarAdicionalView
=============================

Vista basada en funciones, hace el llamado al :ref:`Template agregar_adicional_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_ordentrabajo`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene la información de un adicional para que el usuario pueda agregarlo a la órden de trabajo. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"adicional", "Objeto del adicional que se consulta."
		"id_orden", "Id de la órden que se está generando."
		"utilidad_fab_op", "Porcentaje de utilidad sobre el adicional configurado para la joyería."

Vista AprobacionPagoModalView
==============================

Vista basada en funciones, hace el llamado al :ref:`Template aprobacion_pago_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_ordentrabajo`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Obtiene la información de una órden de trabajo para la aprobación de su pago. Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"orden", "Objeto de la órden que se consulta."
		"item", "Id del ítem asociado a la órden."
		"detalle", "Detalle del ítem asociado a la órden."
		"detalleSolicitud", "Detalle de la solicitud asociada a la órden."
		"sintalla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"total_costos_asociados", "Total de los costos asociados a la órden."
		"costos_lista", "Lista de los costos asociados a la órden."
		"valor_error", "Valor error estipulado por el taller."
		"usuario_aprueba", "Usuario que aprueba el pago de la órden de trabajo."

Método POST
------------
Registra la aprobación del pago de la órden consultada con su respectiva fecha de aprobación.

Vista EnvioMaterialView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar el envío de materia prima desde la joyería hacia el taller, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador EnvioMaterialSerializer`.

Vista RecibirMaterialView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la recepción de materia prima por parte del taller, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador RecibirMaterialSerializer`.

Vista AnularOrdenView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la anulación de una órden de trabajo por parte del taller, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador AnularOrdenSerializer`.

Vista FinalizarTrabajoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la finalización del trabajo de fabricación por parte del taller, también modifica los valores de la órden de ser necesario, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador FinalizarTrabajoSerializer`.

Vista EnviarProductoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar el envío del producto desde el taller hacia la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador EnviarProductoSerializer`.

Vista RecibirProductoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la recepción del producto por parte de la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador RecibirProductoSerializer`.

Vista CargarDocumentosTaller
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la carga de documentos pendientes por parte del taller, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador CargarDocTallerSerializer`.

Vista CargarDocumentosOperaciones
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la carga de documentos pendientes por parte de la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador CargarDocOpSerializer`.

Vista DevolverProductoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la devolución del producto por parte de la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador EnviarProductoSerializer`. Además genera una nueva órden de trabajo con los mismos datos de la órden consultada para la devolución.

Vista FinalizarOrdenView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la finalización de la órden con venta por parte de la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador FinalizarOrdenSerializer`.

Vista FinalizarSinVentaView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para registrar la finalización de la órden sin venta por parte de la joyería, cuenta con las siguientes acciones:

Método POST
------------
Registra un cambio de estado en la órden de trabajo hace uso del :ref:`Serializador FinalizarSinVentaSerializer`.

Vista EnviarCorreoView
====================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para realizar un envío de correo al cliente.

Vista ReporteOrdenesPagos
==============================

Vista basada en funciones, permite la generación de un reporte que contiene la información de los pagos aprobados para las órdenes de trabajo generadas en un rango de fechas determinado.