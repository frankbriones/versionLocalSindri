***********************
**Serializadores trn**
***********************

Dentro de la carpeta **trn** tenemos el archivo llamado ``serializers.py``. Donde se encuentran los serializadores de la aplicación trn.

Serializador OrdenesSerializer
=======================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para las consultas de las órdenes de trabajo que se generan en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "fecha_creacion","Fecha en que se generó la órden de trabajo."
        "usuario_crea", "Id del  usuario que generó la orden de trabajo."
        "secuencia", "Identificador de la órden generada."
        "colorestado", "Código hexadecimal del color asignado a la órden dependiendo del estado."
        "id_orden", "Id de la órden de trabajo."
        "estado", "Id del estado de la órden."
        "estado_nombre", "Descripción del estado de la órden."
        "solicita", "Username del usuario que solicita la órden."
        "pago_aprobado", "Indica si el pago de la órden ha sido aprobado."
        "fecha_recibe_prod", "Fecha en que la joyería recibe el producto."
        "fecha_aprueba_pago", "Fecha en que se aprueba el pago de la fabricación."
        "usuario_aprueba_pago", "Username del usuario que aprueba el pago de la fabricación."

Serializador SolicitudesSerializer
=======================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo SolicitudTrabajo`. Este es el serializador utilizado para las consultas de las solicitudes de trabajo que se generan en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "fecha_creacion","Fecha en que se generó la solicitud de trabajo."
        "usuario_crea", "Id del  usuario que generó la solicitud de trabajo."
        "secuencia", "Identificador de la solicitud generada."
        "colorestado", "Código hexadecimal del color asignado a la solicitud dependiendo del estado."
        "id_solicitud", "Id de la solicitud de trabajo."
        "estado", "Id del estado de la solicitud."
        "estado_nombre", "Descripción del estado de la solicitud."
        "solicita", "Username del usuario que realizó la solicitud."
        "detalle", "Detalle de la solicitud de trabajo."

Serializador SolicitarAExternoSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo SolicitudTrabajo`. Este es el serializador utilizado para generar una solicitud a externo, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "detalle", "Detalle de la solicitud de trabajo."

Serializador EnvioMaterialSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar el envío de material, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "comp_envio_op", "Comprobante de envío de material."
        "gramos_enviados", "Cantidad de gramos enviados."

Serializador RecibirMaterialSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la recepción de material, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "gramos_recibidos", "Cantidad de gramos recibidos."

Serializador AnularOrdenSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la anulación de una órden de trabajo, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "obs_recepcion_mat", "Observación sobre la anulación de la orden."

Serializador FinalizarTrabajoSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la finalización de una fabricación, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "peso_final", "Peso final del producto de la órden."

Serializador EnviarProductoSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar el envío del producto, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "comp_envio_ta", "Comprobante de envío de producto."
        "costo_envio", "Costo del envío."

Serializador RecibirProductoSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la recepción de un producto, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "estado", "Estado de la órden."

Serializador CargarDocTallerSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la carga de la factura del taller, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "factura_taller", "Archivo de factura del taller."

Serializador CargarDocOpSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la carga de los documentos generados para la órden de trabajo por parte de la joyería, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "cta_por_pagar", "Archivo de cuenta por pagar."
        "orden_compra", "Archivo de órden de compra."

Serializador DevolverProductoSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la devolución de un producto, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "obs_recepcion_prod", "Observación sobre la devolución del producto."

Serializador FinalizarOrdenSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la finalización de una órden de trabajo, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "obs_venta", "Observación sobre la finalización de la órden."
        "factura_vta", "Archivo de factura de venta."

Serializador FinalizarSinVentaSerializer
=========================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo OrdenTrabajo`. Este es el serializador utilizado para registrar la finalización de una órden de trabajo sin venta, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "obs_venta", "Observación sobre la finalización de la órden."

Serializador GenerarOrdenSerializer
=======================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo SolicitudTrabajo`. Este es el serializador utilizado para generar una órden de trabajo con los datos de una solicitud, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "peso_solicitado", "Peso del producto solicitado por el cliente."
        "costo_gramo_base_op", "Costo del gramo de oro estipulado por la joyería."
        "costo_gramo_base_ta", "Costo del gramo de oro estipulado por el taller."
        "prct_util_sobre_base_op", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por la joyería."
        "prct_util_sobre_base_ta", "Porcentaje de utilidad aplicado sobre la materia prima impuesto por el taller."
        "util_sobre_base_ta", "Valor de utilidad obtenido sobre la materia prima suministrada por el taller."
        "servicio_fabricacion", "Costo total de la mano de obra para la fabricación."
        "costo_taller", "Suma de todos los costos cobrados por el taller para la fabricación."
        "prct_util_sobre_fabrica_ta", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por el taller."
        "util_sobre_fabrica_ta", "Valor de utilidad obtenido sobre la fabricación para el taller."
        "prct_util_sobre_fabrica_op", "Porcentaje de utilidad aplicado sobre la fabricación impuesto por la joyería."
        "prct_impuestos", "Porcentaje de impuestos cobrados por la joyería."
