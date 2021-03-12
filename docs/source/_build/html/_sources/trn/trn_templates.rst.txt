*******************
**Templates trn**
*******************

Dentro de la carpeta **trn** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación trn correspondiente a la gestión de transacciones y promociones.

Template agregar_adicional_modal
=====================================

Template del modal que aparecerá cuando el usuario desea agregar un adicional a una órden de trabajo, las funciones que posee este template son las siguientes:

Función calcularPrecioAdicional
--------------------------------

Realiza el cálculo del precio final del adicional según la cantidad ingresada por el usuario y agregándole la utilidad para la joyería.

Función agregar
--------------------------------

Agrega la información del adicional al arreglo de adicionales creado en el Localstorage.

Template agregar_piedra_modal
=====================================

Template del modal que aparecerá cuando el usuario desea agregar una piedra a una órden de trabajo, las funciones que posee este template son las siguientes:

Función buscarDetallePiedra
--------------------------------

Obtiene los datos del detalle de la piedra según la medida seleccionada, también realiza el cálculo del precio final de la piedra según la cantidad ingresada por el usuario y agregándole la utilidad para la joyería.

Función agregar
--------------------------------

Agrega la información de la piedra al arreglo de adicionales creado en el Localstorage.

Template aprobacion_pago_modal
==================================

Template del modal que aparecerá cuando el usuario desea aprobar el pago de una órden de trabajo, las funciones que posee este template son las siguientes:

Función aprobarPago
-------------------------

Realiza una petición de tipo POST a la :ref:`url orden_aprobacion_pago` enviando como parámetro el id de la órden para la cual se aprueba el pago.

Template comprobante_orden
==================================

Template del comprobante de una órden que se utiliza para generar un PDF que se podrá imprimir posteriormente.

Template correo_cliente
==================================

Template del correo que se envía al cliente una vez generada la órden de trabajo.

Template correo_producto_recibido
==================================

Template del correo que se envía al jefe zonal y al cliente una vez recibido el producto de la órden de trabajo por parte de la joyería.

Template detalle_orden_modal
==================================

Template del modal que aparecerá cuando el usuario desea consultar una órden para ver sus detalles, las funciones que posee este template son las siguientes:

Función mostrarFormulario
---------------------------

Oculta o muestra formularios y botones en el modal según los parámetros que reciba la función.

Función validarArchivo
---------------------------

Valida si el archivo que se está cargando tiene una extensión de las permitidas en el sistema y si no excede del peso máximo permitido.

Función envioMaterial
---------------------------

Realiza una petición de tipo POST a la :ref:`url envio_material` enviando un formulario que contiene el archivo de comprobante de envío de material.

Función recibeMaterial
---------------------------

Realiza una petición de tipo POST a la :ref:`url recibe_material` enviando un formulario que contiene los gramos de oro recibidos por el taller.

Función anularOrden
---------------------------

Realiza una petición de tipo POST a la :ref:`url anular_orden` enviando un formulario que contiene la observación para la anulación de la órden.

Función iniciarTrabajo
---------------------------

Realiza una petición de tipo POST a la :ref:`url ordenes_detalle` enviando como parámetro el id de la órden.

Función finalizarTrabajo
---------------------------

Realiza una petición de tipo POST a la :ref:`url ordenes_detalle` enviando un formulario que contiene el peso final del producto.

Función enviarProducto
---------------------------

Realiza una petición de tipo POST a la :ref:`url enviar_producto` enviando un formulario que contiene el archivo de comprobante de envío de producto y el costo del envío.

Función recibirProducto
---------------------------

Realiza una petición de tipo POST a la :ref:`url recibir_producto` enviando como parámetro el id de la órden y el estado al que debe ser actualizada.

Función cargarDocumentosTa
---------------------------

Realiza una petición de tipo POST a la :ref:`url cargar_doc_taller` enviando un formulario que contiene los archivos de los documentos pendientes por cargar por parte del taller.

Función cargarDocumentosOp
---------------------------

Realiza una petición de tipo POST a la :ref:`url cargar_doc_ope` enviando un formulario que contiene los archivos de los documentos pendientes por cargar por parte de la joyería.

Función devolverProducto
---------------------------

Realiza una petición de tipo POST a la :ref:`url devolver_producto` enviando como parámetro el id de la órden y el estado al que debe ser actualizada.

Función finalizarOrden
---------------------------

Realiza una petición de tipo POST a la :ref:`url finalizar_orden` enviando un formulario que contiene la factura de venta y una observación de ser el caso.

Función finalizarSinVenta
---------------------------

Realiza una petición de tipo POST a la :ref:`url finalizar_sin_venta` enviando un formulario que contiene una observación sobre la finalización de la órden.

Función finalizarSinVenta
---------------------------

Realiza una petición de tipo POST a la :ref:`url correo_cliente` enviando un formulario que contiene el archivo de factura de venta y la observación de ser el caso.

Template detalle_solicitud_modal
==================================

Template del modal que aparecerá cuando el usuario desea consultar una solicitud de trabajo para ver sus detalles, las funciones que posee este template son las siguientes:

Función calcularPrecio
-------------------------

Calcula todos los valores correspondientes a la solicitud según el peso que recibe por parámetro hasta mostrar al usuario el precio final de la solicitud.

Función calcularPrecioGramoFijo
--------------------------------

Calcula todos los valores correspondientes a la solicitud según el peso que recibe por parámetro hasta mostrar al usuario el precio final de la solicitud basado en un precio gramo final fijo.

Función CalcularDescuento
--------------------------

Calcula el nuevo precio de la solicitud luego de aplicar el descuento ingresado por el usuario, valida también que el descuento no exceda el máximo permitido.

Función mostrarRubros
-------------------------

Muestra el listado de rubros asociados a la solicitud.

Función ocultarRubros
-------------------------

Oculta el listado de rubros asociados a la solicitud.

Función evaluar
-------------------------

Muestra el formulario para evaluación de solicitud.

Función rechazar
-------------------------

Muestra el formulario para rechazo de solicitud.

Función aceptar
-------------------------

Muestra el formulario para cotización de solicitud.

Función responderSolicitud
---------------------------

Realiza una petición de tipo POST a la :ref:`url solicitudes_detalle` enviando como parámetro el id de la solicitud a responder, la data que se envía en la petición se describe a continuación:

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

Función generarOrden
---------------------------

Realiza una petición de tipo POST a la :ref:`url generar_orden_solicitud` enviando como parámetro el id de la solicitud para generar una órden a partir de esta, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"peso_solicitado", "Peso del producto solicitado por el cliente."
		"precio", "Precio de la solicitud."
		"costo_gr_base_op", "Costo del gramo de oro estipulado por la joyería."
		"costo_gr_base_ta", "Costo del gramo de oro estipulado por el taller."
		"prct_util_sobre_base_op", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por la joyería."
        "util_sobre_base_op", "Valor de utilidad obtenido sobre la materia prima suministrada por la joyería."
        "prct_util_sobre_base_ta", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por el taller."
        "util_sobre_base_ta", "Valor de utilidad obtenido sobre la materia prima suministrada por el taller."
		"servicio_fabricacion", "Costo total de la mano de obra para la fabricación."
		"costo_taller", "Suma de todos los costos cobrados por el taller para la fabricación."
		"prct_util_sobre_fabrica_op", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por la joyería."
        "util_sobre_fabrica_op", "Valor de utilidad obtenido sobre la fabricación para la joyería."
        "prct_util_sobre_fabrica_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
        "util_sobre_fabrica_ta", "Valor de utilidad obtenido sobre la fabricación para el taller."
		"prct_impuestos", "Porcentaje de impuestos aplicados sobre la órden de parte de la joyería."
        "impuestos", "Valor de impuestos aplicados sobre la órden de parte de la joyería."
        "prct_impuestos_ta", "Porcentaje de impuestos aplicados sobre la órden de parte del taller."
        "impuestos_ta", "Valor de impuestos aplicados sobre la órden de parte del taller."
		"precio_gramo_final", "Costo por gramo de oro en caso de manejarse un precio fijo."
		"precio_con_descuento", "Precio de la órden luego de aplicar descuento."
		"costo_total_rubros", "Costo total de los rubros asociados a la órden."
        "valor_error", "Costo que se puede adicionar o restar del precio calculado para la fabricación, dependiendo del peso final del producto."

Función SolicitarExterno
---------------------------

Realiza una petición de tipo POST a la :ref:`url solicitar_externo` enviando como parámetro el id de la solicitud para generar una solicitud a externo a partir de esta.

Función agregarRubro
---------------------------

Crea el elemento HTML para agregar un rubro a la solicitud de trabajo.

Función borrardiv
---------------------------

Elimina el elemento HTML enviado por parámetro.

Función nombrarElementos
---------------------------

Asigna un id a los elementos HTML creados.

Función obtenerRubros
---------------------------

Genera un arreglo con los rubros agregados a la solicitud de trabajo.

Función calcularValoresTaller
------------------------------

Calcula los costos a pagar al taller por el trabajo de fabricación.

Template ordenes_item_crear
==================================

Template de la pantalla que le permite al usuario generar una órden de trabajo a partir de un ítem de catálogo, las funciones que posee este template son las siguientes:

Función buscarDetalle
-------------------------

Realiza una petición de tipo GET a la :ref:`url detalle_buscar` enviando como parámetro el id del detalle de ítem y el id del ítem para obtener la información del detalle.

Función calcularPrecio
-------------------------

Calcula todos los valores correspondientes a la órden según el peso seleccionado por el usuario hasta mostrar al usuario el precio final de la órden.

Función calcularPrecioGramoFijo
--------------------------------

Calcula todos los valores correspondientes a la órden según el peso seleccionado por el usuario hasta mostrar al usuario el precio final de la órden basado en un precio gramo final fijo.

Función CalcularDescuento
--------------------------

Calcula el nuevo precio de la órden luego de aplicar el descuento ingresado por el usuario, valida también que el descuento no exceda el máximo permitido.

Función cargarAdicionales
--------------------------

Agrega a la órden los adicionales que se encuentran en un arreglo guardado en el LocalStorage, calcula el nuevo precio de la órden sumados los costos de estos adicionales.

Función borrarAdicional
--------------------------

Quita un adicional de la órden y recalcula el precio final.

Función buscarElemento
--------------------------

Identifica el elemento del adicional a eliminar.

Función borrarAdicionales
--------------------------

Elimina todos los adicionales guardados.

Función validarArchivo
---------------------------

Valida si el archivo que se está cargando tiene una extensión de las permitidas en el sistema y si no excede del peso máximo permitido.

Función guardarOrden
---------------------------

Realiza una petición de tipo POST a la :ref:`url ordenes_item_crear` enviando como parámetro el id del ítem y la identificación del cliente, la data que se envía en la petición se describe a continuación:

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

Template ordenes_lista
============================

Template de la pantalla para consultar las órdenes de un usuario o taller determinado. Las funciones que posee este template son las siguientes:

Función obtenerOrdenesfecha
---------------------------------

Realiza una petición de tipo GET a la :ref:`url ordenes_api_lista_fecha` enviando como parámetro una fecha de inicio y una de fin para obtener las órdenes que fueron generadas dentro de dicho rango de fechas, además un parámetro opcion para identificar el tipo de consulta que se realiza.

Función generarReporte
---------------------------------

Redirige hacia la :ref:`url rep_ordenes_admin_op` o :ref:`url rep_ordenes` dependiendo el tipo de usuario que realiza la consulta enviando como parámetro una fecha de inicio y una de fin para obtener las órdenes que fueron generadas dentro de dicho rango de fechas, además un parámetro opcion para identificar el tipo de consulta que se realiza, esto para obtener un reporte en una hoja de cálculo con la información de las órdenes correspondientes al rango de fechas dado.

Función verDetalles
--------------------

Redirige al :ref:`url ordenes_detalle` enviando como parámetro el id de la órden de la cual se requieren los detalles.

Función formato
----------------

Da formato a la Tabla que se genera con el listado de órdenes consultadas.

Template ordenes_pagos_lista
=============================

Template de la pantalla para consultar los pagos aprobados de las órdenes de un usuario o taller determinado. Las funciones que posee este template son las siguientes:

Función obtenerOrdenesfecha
---------------------------------

Realiza una petición de tipo GET a la :ref:`url ordenes_pagos_api_lista` enviando como parámetro una fecha de inicio y una de fin para obtener las órdenes que fueron generadas dentro de dicho rango de fechas, además un parámetro opcion para identificar el tipo de consulta que se realiza.

Función generarReporte
---------------------------------

Redirige hacia la :ref:`url rep_pagos_aprobados` enviando como parámetro una fecha de inicio y una de fin para obtener las órdenes que fueron generadas dentro de dicho rango de fechas, además un parámetro opcion para identificar el tipo de consulta que se realiza, esto para obtener un reporte en una hoja de cálculo con la información de las órdenes y su estado de pago correspondientes al rango de fechas dado.

Función verDetalles
--------------------

Redirige al :ref:`url orden_aprobacion_pago` enviando como parámetro el id de la órden de la cual se requieren los detalles.

Función formato
----------------

Da formato a la Tabla que se genera con el listado de órdenes consultadas.

Template ordenes_solicitud_crear
==================================

Template de la pantalla que le permite al usuario generar una órden de trabajo a partir de una solicitud, las funciones que posee este template son las siguientes:

Función validarArchivo
---------------------------

Valida si el archivo que se está cargando tiene una extensión de las permitidas en el sistema y si no excede del peso máximo permitido.

Función guardarOrden
---------------------------

Realiza una petición de tipo POST a la :ref:`url ordenes_solicitud_crear` enviando como parámetro el id de la solicitud y la identificación del cliente, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"env_material", "Indica si la joyería envía o no materia prima hacia el taller."

Template reporte_lista_ordenes
==================================

Template utilizado para generar el reporte de órdenes con su respectiva información detallada.

Template solicitudes_editar_form
==================================

Template de la pantalla que permite al usuario modificar los valores de una solicitud generada con anterioridad, las funciones que posee este template son las siguientes:

Función validarImagen
---------------------------

Valida si la imagen que se está cargando tiene una extensión de las permitidas en el sistema y si no excede del peso máximo permitido.

Función seleccionarImagen
---------------------------

Crea una vista previa de la imagen cargada en caso de que la imágen cargada sea válida.

Función guardar
---------------------------

Realiza una petición de tipo POST a la :ref:`url solicitudes_editar` enviando como parámetro el id de la solicitud para guardar los valores asignados a la transacción, la data que se envía en la petición se describe a continuación:

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
		"id_proveedor", "Id del proveedor a quien va dirigida la solicitud."

Template solicitudes_form
==================================

Template de la pantalla que permite al crear una solicitud de trabajo, las funciones que posee este template son las siguientes:

Función validarImagen
---------------------------

Valida si la imagen que se está cargando tiene una extensión de las permitidas en el sistema y si no excede del peso máximo permitido.

Función seleccionarImagen
---------------------------

Crea una vista previa de la imagen cargada en caso de que la imágen cargada sea válida.

Función guardar
---------------------------

Realiza una petición de tipo POST a la :ref:`url solicitudes_crear` enviando como parámetro el id del ítem asociado a la solicitud y el tipo de transacción si es interna o externa, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
		"rubros_lista[]","Arreglo que contiene los rubros asignados a la solicitud."
		"id_solicitud-peso_min","Peso mínimo de fabricación para el producto estipulado por el taller."
		"id_solicitud-peso_max","Peso máximo de fabricación para el producto estipulado por el taller."
		"id_solicitud-valor_gramo", "Costo por gramo de oro asignado a la solicitud."
		"id_solicitud-valor_error", "Costo que se puede adicionar o restar del precio calculado para la fabricación, dependiendo del peso final del producto."
		"id_solicitud-tiempo_ent_min", "Tiempo mínimo necesario para la entrega del producto."
		"id_solicitud-tiempo_ent_max", "Tiempo máximo necesario para la entrega del producto."
		"total_rubros", "Costo total de los rubros asociados a la solicitud."
		"id_solicitud-proveedor", "Id del proveedor a quien va dirigida la solicitud."
		"id_solicitud-talla", "Id de la talla seleccionada en la solicitud."
		"id_solicitud-color", "Id del color seleccionado en la solicitud."
		"id_solicitud-acabado", "Acabado de la joya."
		"id_solicitud-parte_interna", "Descripción de la parte interna de la joya."
		"id_solicitud-cantidad_piedras", "Cantidad de piedras de la joya."

Función agregarRubro
---------------------------

Crea el elemento HTML para agregar un rubro a la solicitud de trabajo.

Función borrardiv
---------------------------

Elimina el elemento HTML enviado por parámetro.

Función nombrarElementos
---------------------------

Asigna un id a los elementos HTML creados.

Función obtenerRubros
---------------------------

Genera un arreglo con los rubros agregados a la solicitud de trabajo.

Template solicitudes_lista
============================

Template de la pantalla para consultar las solicitudes de un usuario o taller determinado. Las funciones que posee este template son las siguientes:

Función obtenerSolicitudesfecha
---------------------------------

Realiza una petición de tipo GET a la :ref:`url solicitudes_api_lista_fecha` enviando como parámetro una fecha de inicio y una de fin para obtener las solicitudes que fueron generadas dentro de dicho rango de fechas, además un parámetro opcion para identificar el tipo de consulta que se realiza.

Función verDetalles
--------------------

Redirige al :ref:`url solicitudes_detalle` enviando como parámetro el id de la solicitud de la cual se requieren los detalles.

Función formato
----------------

Da formato a la Tabla que se genera con el listado de órdenes consultadas.

Template tipo_solicitud_modal
==================================

Template del modal que permite al usuario elegir el tipo de solicitud a realizar, las funciones que posee este template son las siguientes:

Función solicitarExterno
-------------------------

Redirige a la :ref:`url solicitudes_crear` enviando como parámetro el id del ítem asociado a la solicitud y como tipo de solicitud el 2 que corresponde a solicitudes externas.

Para solicitudes internas se redirige al usuario a la :ref:`url solicitudes_crear` enviando como parámetro el id del ítem asociado a la solicitud y como tipo de solicitud el 1 que corresponde a solicitudes internas.
