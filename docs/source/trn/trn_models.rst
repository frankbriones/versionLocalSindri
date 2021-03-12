*****************
**Modelos trn**
*****************

Dentro de la carpeta **trn** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación trn

Modelo OrigenMaterial
==========================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para registrar los deiferentes origenes de material en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_origen","Id del origen de material registrado."
        "descripcion", "Descripción del origen de material."

Modelo SolicitudTrabajo
========================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las solicitudes de trabajo que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_solicitud","Id de la solicitud registrada."
        "secuencia", "Identificador de la solicitud generada."
        "usuario", "Id del usuario que genera la solicitud."
        "taller", "Id del taller a quien va dirigida la solicitud."
        "proveedor", "Id del proveedor a quien va dirigida la solicitud."
        "imagen", "Url de la imagen relacionada a la solicitud."
        "peso_min", "Peso mínimo de fabricación asignado a la solicitud."
        "peso_max", "Peso máximo de fabricación asignado a la solicitud."
        "talla", "Id de la talla solicitada para la fabricación."
        "color", "Id del colo solicitado para la fabricación."
        "longitud", "Medida solicitada para la fabricación."
        "valor_gramo", "Costo por gramo de oro asignado a la solicitud."
        "valor_error", "Costo que se puede adicionar o restar del precio calculado para la fabricación, dependiendo del peso final del producto."
        "total_rubros", "Costo total de los rubros asociados a la solicitud."
        "precio", "Precio calculado de la fabricación."
        "externa", "Indica si la fabricación la realiza un taller interno o un proveedor externo."
        "acabado", "Describe el acabado del producto solicitado por el cliente."
        "parte_interna", "Describe la parte interna del producto solicitado por el cliente."
        "cantidad_piedras", "Cantidad de piedras que posee el producto."
        "origen_material", "Origen de la materia prima para la fabricación."
        "costo_gramo_base_op", "Costo del gramo de oro estipulado por la joyería."
        "costo_gramo_base_ta", "Costo del gramo de oro estipulado por el taller."
        "prct_util_sobre_base_op", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por la joyería."
        "util_sobre_base_op", "Valor de utilidad obtenido sobre la materia prima suministrada por la joyería."
        "prct_util_sobre_base_ta", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por el taller."
        "util_sobre_base_ta", "Valor de utilidad obtenido sobre la materia prima suministrada por el taller."
        "prct_util_sobre_fabrica_op", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por la joyería."
        "util_sobre_fabrica_op", "Valor de utilidad obtenido sobre la fabricación para la joyería."
        "prct_util_sobre_fabrica_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
        "util_sobre_fabrica_ta", "Valor de utilidad obtenido sobre la fabricación para el taller."
        "sku_relacionado", "SKU del producto de catálogo relacionado a la fabricación solicitada."
        "tiempo_ent_min", "Tiempo mínimo necesario para la entrega del producto."
        "tiempo_ent_max", "Tiempo máximo necesario para la entrega del producto."
        "tiempo_respuesta", "Fecha en que el taller responderá a una solicitud en evaluación."
        "detalle", "Descripción de lo solicitado por el cliente."
        "observacion_op", "Observación sobre la solicitud de parte de operaciones."
        "observacion_ta", "Observación sobre la solicitud de parte del taller."
        "pais", "Id del país al que pertenece la promoción."
        "estado", "Id del estado de la promoción."
        "generado_con_ext", "Indica si la solicitud es generada a partir de una solicitud rechazada por el taller."
        "solicitud_relacionada", "Id de la solicitud rechazada por la cual se generó la nueva solicitud."
        "peso_solicitado", "Peso del producto solicitado por el cliente."
        "prct_impuestos", "Porcentaje de impuestos cobrados por la joyería."
        "impuestos", "Valor de impuestos cobrado por la joyería."
        "prct_impuestos_ta", "Porcentaje de impuestos cobrados por el taller."
        "impuestos_ta", "Valor de impuestos cobrado por el taller."
        "costo_taller", "Suma de todos los costos cobrados por el taller para la fabricación."
        "servicio_fabricacion", "Costo total de la mano de obra para la fabricación."
        "precio_con_descuento", "Precio de la solicitud luego de aplicar descuento."
        "fecha_cotizacion", "Fecha en que la solicitud fue cotizada."
        "tiempo_cotizacion", "Tiempo en que el taller tardó en cotizar una solicitud."
        "precio_gramo_final", "Costo por gramo de oro en caso de manejarse un precio fijo."

Modelo DetalleSolicitud
==========================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los detalles que pertenecen a una solicitud, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_detalle_solicitud","Id del detalle registrado."
        "solicitud", "Id de la solicitud a la que pertenece el detalle."
        "item", "Id del ítem registrado en el detalle."
        "pais", "Id del país al que pertenece el detalle."

Modelo OrdenTrabajo
====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las órdenes de trabajo que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_orden","Id de la órden de trabajo registrada."
        "secuencia", "Identificador de la órden generada."
        "cliente", "Id del cliente de la órden de trabajo."
        "usuario", "Id del usuario que genera la órden."
        "taller", "Id del taller a quien va dirigida la órden."
        "proveedor", "Id del proveedor a quien va dirigida la órden."
        "color", "Id del colo solicitado para la fabricación."
        "categoria", "Id de la categoría a la pertenece el ítem de la órden de trabajo."
        "peso_solicitado", "Peso del producto solicitado por el cliente."
        "peso_final", "Peso final del producto fabricado."
        "costo_taller", "Suma de todos los costos cobrados por el taller para la fabricación."
        "servicio_fabricacion", "Costo total de la mano de obra para la fabricación."
        "precio_sistema", "Precio total de la órden calculado por el sistema."
        "precio_con_descuento", "Precio de la órden luego de aplicar descuento."
        "precio_min", "Precio total mínimo calculado para la órden."
        "precio_max", "Precio total máximo calculado para la órden."
        "externa", "Indica si la fabricación la realiza un taller interno o un proveedor externo."
        "env_material", "Indica si la joyería envía materia prima hacia el taller."
        "gramos_enviados", "Cantidad de gramos de oro que envía la joyería hacia el taller."
        "gramos_recibidos", "Cantidad de gramos de oro que recibe el taller enviados desde la joyería."
        "comp_envio_ta", "Url del archivo que corresponde al comprobante de envío del producto desde el taller hacia la joyería."
        "comp_envio_op", "Url del archivo que corresponde al comprobante de envío del material desde la joyería hacia el taller."
        "factura_vta", "Url del archivo que corresponde a la factura de venta."
        "obs_recepcion_prod", "Observación de la joyería al recibir el producto."
        "obs_venta", "Observación de la joyería al vender el producto."
        "obs_recepcion_mat", "Observación del taller al recibir el material."
        "fecha_recibe_mat", "Fecha en que el taller recibe la materia prima enviada por la joyería."
        "fecha_envio_mat", "Fecha en que la joyería envía la materia prima hacia el taller."
        "fecha_anulacion", "Fecha en que el taller anula la órden de trabajo."
        "fecha_fin_trabajo", "Fecha en que el taller finaliza el trabajo de fabricación."
        "fecha_envio_prod", "Fecha en que el taller envía el producto hacia la joyería."
        "fecha_recibe_prod", "Fecha en que la joyería recibe el producto."
        "fecha_venta", "Fecha en que la joyería vende el producto."
        "tiempo_duracion_orden", "Tiempo total de duración de una orden desde que se genera hasta que es finalizada."
        "origen_material", "Origen de la materia prima para la fabricación."
        "costo_gramo_base_op", "Costo del gramo de oro estipulado por la joyería."
        "costo_gramo_base_ta", "Costo del gramo de oro estipulado por el taller."
        "prct_util_sobre_base_op", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por la joyería."
        "util_sobre_base_op", "Valor de utilidad obtenido sobre la materia prima suministrada por la joyería."
        "prct_util_sobre_base_ta", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por el taller."
        "util_sobre_base_ta", "Valor de utilidad obtenido sobre la materia prima suministrada por el taller."
        "prct_util_sobre_fabrica_op", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por la joyería."
        "util_sobre_fabrica_op", "Valor de utilidad obtenido sobre la fabricación para la joyería."
        "prct_util_sobre_fabrica_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
        "util_sobre_fabrica_ta", "Valor de utilidad obtenido sobre la fabricación para el taller."
        "costo_gramo_fabricado", "Costo de gramo de fabricación."
        "adicional_color_gramo", "Costo adicional por gramo de fabricación debido al color de la joya."
        "precio_piedras", "Precio de las piedras finas agregadas a la órden de trabajo."
        "costo_adicionales", "Costo de los adicionales agregados a la órden de trabajo."
        "util_sobre_adicionales", "Utilidad aplicada sobre el costo de adicionales."
        "precio_adicionales", "Precio total de adicionales sumada la utilidad."
        "precio_venta_final", "Precio final de la órden."
        "pais", "Id del país al que pertenece la órden."
        "estado", "Id del estado de la órden."
        "prct_impuestos", "Porcentaje de impuestos aplicados sobre la órden de parte de la joyería."
        "impuestos", "Valor de impuestos aplicados sobre la órden de parte de la joyería."
        "prct_impuestos_ta", "Porcentaje de impuestos aplicados sobre la órden de parte del taller."
        "impuestos_ta", "Valor de impuestos aplicados sobre la órden de parte del taller."
        "pago_aprobado", "Indica si el pago por la fabricación de la órden fue aprobado."
        "fecha_aprueba_pago", "Fecha en que se aprueba el pago de la fabricación."
        "precio_piedras_op", "Precio final de las piedras finas agregadas a la órden de parte de la joyería."
        "precio_adicionales_op", "Precio final de los adicionales agregados a la órden de parte de la joyería."
        "util_sobre_adicionales_op", "Utilidad sobre los adicionales obtenida por la joyería."
        "util_sobre_piedras_op", "Utilidad sobre las piedras obtenida por la joyería."
        "orden_vendida", "Indica si la órden fué vendida o no."
        "costo_envio", "Costo de envío del producto desde el taller hacia la joyería."
        "anticipo_fabricacion", "Url del archivo que corresponde al comprobante de anticipo para la fabricación."
        "factura_taller", "Url del archivo que corresponde a la factura del taller."
        "cta_por_pagar", "Url del archivo que corresponde a la cuenta por pagar generada."
        "orden_compra", "Url del archivo que corresponde a la órden de compra generada."
        "precio_gramo_final", "Costo por gramo de oro en caso de manejarse un precio fijo."
        "costo_piedras_basicas", "Costo de piedras registrado para el ítem de la órden de trabajo."
        "costo_total_rubros", "Costo total de los rubros asociados a la órden."
        "valor_error", "Costo que se puede adicionar o restar del precio calculado para la fabricación, dependiendo del peso final del producto."
        "datos_extra", "Datos adicionales sobre la fabricación."
        "usuario_aprueba_pago", "Id del usuario que aprueba el pago de la fabricación."

Modelo DetalleOrden
==========================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los detalles que pertenecen a una órden, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_detalle_orden","Id del detalle registrado."
        "orden", "Id de la órden a la que pertenece el detalle."
        "id_solicitud", "Id de la solicitud registrada en el detalle."
        "id_item", "Id del ítem registrado en el detalle."
        "id_detalle_item", "Id del detalle de ítem registrado en el detalle de órden."
        "id_adicional", "Id del adicional registrado en el detalle."
        "costo_unitario_adicional", "Costo unitario de adicional registrado en la órden."
        "prct_util_sobre_adicional", "Porcentaje de utilidad aplicado sobre el adicional."
        "utilidad_sobre_adicional", "Valor de la utilidad obtenida del adicional."
        "precio_adicionales", "Precio de los adicionales."
        "id_piedra", "Id de la piedra registrada en el detalle."
        "id_detalle_piedra", "Id del detalle de piedra registrado en el detalle."
        "costo_unitario_piedra", "Costo unitario de la piedras registrada en el detalle."
        "prct_util_sobre_piedra", "Porcentaje de utilidad aplicado sobre la piedra."
        "utilidad_sobre_piedra", "Valor de la utilidad obtenida sobre la piedra."
        "precio_piedras", "Precio de las piedras."
        "cantidad", "Cantidad de elementos agregados por detalle."
        "precio_piedras_op", "Total a cobra por la joyería por concepto de piedras finas."
        "precio_adicionales_op", "Total a cobrar por la joyería por concepto de adicionales."
        "util_sobre_adicionales_op", "Valor de utilidad sobre adicionales obtenido por la joyería."
        "util_sobre_piedras_op", "Valor de utilidad sobre piedras finas obtenido por la joyería."
        "pais", "Id del país al que pertenece el detalle."


Modelo RubrosAsociados
=======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los rubros asociados registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_rubro","Id del rubro registrado."
        "descripcion", "Descripción del rubro."
        "estado", "Id del estado del rubro en el sistema."

Modelo SolicitudRubros
=======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los rubros asociados a una solicitud de trabajo, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_solicitud_rubro","Id de la relación rubro-solicitud registrada."
        "solicitud", "Id de la solicitud a la que pertenece el rubro."
        "rubro", "Id del rubro asociado a la solicitud."
        "valor", "Valor asignado al rubro."
