*****************
**Modelos ctg**
*****************

Dentro de la carpeta **ctg** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación ctg

Modelo TiposCatalogo
=====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los tipos de catálogo registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_tipo_catalogo","Id del tipo de catálogo registrado."
        "descripcion", "Descripción del tipo de catálogo."
        "estado", "Id del estado del tipo de catálogo puede ser activo o inactivo."

Modelo UnidadesMedida
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las unidades de medida registradas en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_unidad","Id de la unidad de medida registrada."
        "descripcion", "Descripción de la unidad de medida."
        "simbolo", "Símbolo asignado a la unidad de medida."
        "estado", "Id del estado de la unidad de medida puede ser activo o inactivo."

Modelo Divisiones
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las divisiones registradas en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_unidad","Id de la unidad de medida registrada."
        "descripcion", "Descripción de la unidad de medida."
        "simbolo", "Símbolo asignado a la unidad de medida."
        "estado", "Id del estado de la unidad de medida puede ser activo o inactivo."

Modelo Categorias
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las categorías registradas en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_categoria","Id de la categoría registrada."
        "descripcion", "Descripción de la categoría."
        "tipo_catalogo", "Id del tipo de catálogo al que pertenece la categoría."
        "unidad_medida", "Id de la unidad de medida asociada a la categoría."
        "taller", "Id del taller al que pertenece la categoría."
        "division", "Id de la división a la que pertenece la categoría."
        "estado", "Id del estado de la categoría puede ser activo o inactivo."

Manager ManejadorItems
=======================

Manager utilizado en el :ref:`Modelo Items`. Este manager permite obtener datos calculados del modelo antes mencionado, consta de los siguientes métodos:

Método contar_detalles
-----------------------
Retorna la cantidad de detalles relacionados a un ítem, recibe como parámetro el id del ítem ``id_item``.

Método contar_colores
-----------------------
Retorna la cantidad de registros de colores relacionados a un ítem, recibe como parámetro el id del ítem ``id_item``.

Modelo Items
=====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para clientes que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_item","Id del ítem registrado."
                "sku", "Identificador único del ítem."
                "descripcion", "Descripción del ítem."
                "tipo_catalogo","Id del tipo de catálogo al que pertenece el ítem."
                "categoria", "Id de la categoría a la que pertenece el ítem."
                "pais", "Id del país al que pertenece el ítem."
                "taller", "Id del taller al que pertenece el ítem."
                "imagen", "Url de la imagen asociada al ítem."
                "valor_fraccion", "Valor del gramo de oro asignado al ítem."
                "valor_gramo_dif", "Valor de gramo de oro diferenciado asignado al ítem."
                "peso_max_dif","Peso máximo para valor de gramo diferenciado, a los pesos por encima de este valor se le aplica el valor gramo normal."
                "escala_peso", "Escala de peso en la que puede ser fabricado un ítem."
                "parte_interna", "Descripción de la parte interna del ítem."
                "acabado","Descripción del acabado del ítem."
                "tiempo_entrega_min", "Tiempo mínimo en que se puede entregar el ítem fabricado."
                "tiempo_entrega_max", "Tiempo máximo en que se puede entregar el ítem fabricado."
                "costo", "Costo total de fabricación del ítem."
                "costo_piedras", "Costo total de las piedras del ítem."
                "cantidad_piedras", "Cantidad de piedras que posee el ítem."
                "estado", "Id del estado del ítem puede ser activo o inactivo."

Este modelo cuenta con los siguientes métodos:

Método comprimirImagen
-----------------------
Permite reducir el peso de una imagen reduciendo su calidad, recibe como parámetro la imagen asociada al ítem ``imagen``.

Método num_detalles
-----------------------
Obtiene la cantidad de detalles relacionados a un ítem, utiliza el :ref:`Manager ManejadorItems`.

Método num_colores
-----------------------
Obtiene la cantidad de registros de colores relacionados a un ítem, utiliza el :ref:`Manager ManejadorItems`.

Modelo Colores
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los colores registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_color","Id del color registrado."
        "descripcion", "Descripción del color."
        "pais", "Id del país al que pertenece el color."
        "taller", "Id del taller al que pertenece el color."
        "costo_adicional", "Costo que se agrega por gramo al valor fracción del ítem."
        "estado", "Id del estado del color puede ser activo o inactivo."

Modelo ItemsColores
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo que describe una relación de muchos a muchos, aquí están registrados los ítems con los colores en los que está disponible su fabricación, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_item_color","Id de la relación ítem-color."
        "item", "Id del ítem."
        "color", "Id del color."

Modelo EstandarTallas
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los estándar de tallas registradas en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_estandar","Id del estándar registrado."
        "descripcion", "Descripción del estándar."

Modelo Tallas
===============

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los colores registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_talla","Id de la talla registrada."
        "diametro", "Diámetro que mide la joya."
        "talla", "Número de talla."
        "estandar", "Id del estándar asociado a la talla."
        "taller", "Id del taller al que pertenece la talla."
        "estado", "Id del estado del color puede ser activo o inactivo."

Modelo DetalleItems
=====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los detalles de un ítem registrado en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_detalle_item","Id del detalle de ítem registrado."
                "id_item", "Id del ítem al que pertenece el detalle."
                "medida", "Medida del detalle."
                "estandar", "Descripción del estándar de medida asignada al detalle."
                "unidad_medida","Id de la unidad de medida asignada al detalle."
                "peso_minimo", "Peso mínimo en que se puede fabricar el ítem."
                "peso_maximo", "Peso máximo en que se puede fabricar el ítem."
                "costo_piedras", "Costo total de las piedras del ítem."
                "cantidad_piedras", "Cantidad de piedras que posee el ítem."
                "estado", "Id del estado del ítem puede ser activo o inactivo."

Modelo Adicionales
=====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los adicionales registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_adicional","Id del adicional registrado."
                "sku", "Identificador único del adicional."
                "taller", "Id del taller al que pertenece el adicional."
                "descripcion", "Descripción del adicional."
                "imagen","Url de la imagen asociada al adicional."
                "costo", "Costo del adicional."
                "utilidad_sobre_adicionales", "Porcentaje de utilidad aplicado sobre el costo del adicional."
                "precio", "Precio del adicional (costo + utilidad)."
                "pais", "Id del país al que pertenece el adicional."
                "estado", "Id del estado del adicional puede ser activo o inactivo."

Modelo CategoriaAdicionales
============================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo que describe una relación de muchos a muchos, aquí están registrados los adicionales con las categorías en las que están disponibles, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_categoria_adicional","Id de la relación adicional-categoría."
        "adicional", "Id del adicional."
        "categoria", "Id de la categoría."
        "taller", "Id del taller al que pertenecen."
        "pais", "Id del país al que pertenecen."

Modelo Piedras
=====================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las piedras finas registradas en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_piedra","Id de la piedra registrada."
                "sku", "Identificador único de la piedra."
                "taller", "Id del taller al que pertenece la piedra."
                "descripcion", "Descripción de la piedra."
                "imagen","Url de la imagen asociada a la piedra."
                "utilidad_sobre_piedras", "Porcentaje de utilidad aplicado sobre el costo de la piedra."
                "pais", "Id del país al que pertenece la piedra."
                "estado", "Id del estado de la piedra puede ser activo o inactivo."

Modelo DetallePiedras
======================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los detalles asociados a una piedra registrada en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_detalle_piedra","Id del detalle registrado."
                "piedra", "Id de la piedra a la que pertenece el detalle."
                "taller", "Id del taller al que pertenece el detalle."
                "medida", "Medida del detalle."
                "costo","Costo de la piedra para la medida dada."
                "precio", "Precio de la piedra para la medida dada (costo + utilidad)."
                "pais", "Id del país al que pertenece el detalle."
                "estado", "Id del estado del detalle puede ser activo o inactivo."

Modelo CategoriaPiedras
============================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo que describe una relación de muchos a muchos, aquí están registrados las piedras con las categorías en las que están disponibles, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_categoria_piedra","Id de la relación piedra-categoría."
        "piedra", "Id de la piedra."
        "categoria", "Id de la categoría."
        "taller", "Id del taller al que pertenecen."
        "pais", "Id del país al que pertenecen."

Modelo ConteoCotizaciones
==========================

Modelo que hereda de ``models.Model`` de Django. Este es el modelo para contabilizar las veces que un ítem es cotizado, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
                "id_cotizacion","Id de la cotización."
                "fecha_creacion", "Fecha en que se genera la cotización."
                "usuario", "Id del usuario que genera la cotización."
                "item", "Id del ítem cotizado."
                "tipo","Tipo de cotización que se realiza (1 para cliente, 2 para usuario interno)."
