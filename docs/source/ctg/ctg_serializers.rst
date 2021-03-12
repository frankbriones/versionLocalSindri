***********************
**Serializadores ctg**
***********************

Dentro de la carpeta **ctg** tenemos el archivo llamado ``serializers.py``. Donde se encuentran los serializadores de la aplicación ctg

Serializador DetallesSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo DetalleItems`. Este es el serializador utilizado para las consultas de los detalles de ítems registrados en el sistema, posee todos los campos del :ref:`Modelo DetalleItems`.

Serializador DetallePiedraSerializer
=====================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo DetallePiedras`. Este es el serializador utilizado para las consultas de los detalles de piedras registrados en el sistema, posee todos los campos del :ref:`Modelo DetallePiedras`.

Serializador DivisionesSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Divisiones`. Este es el serializador utilizado para las consultas de las divisiones registradas en el sistema, posee todos los campos del :ref:`Modelo Divisiones`.

Serializador CategoriasSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Categorias`. Este es el serializador utilizado para las consultas de las categorías registradas en el sistema, posee todos los campos del :ref:`Modelo Categorias`.

Serializador ColoresSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Colores`. Este es el serializador utilizado para las consultas de los colores registrados en el sistema, posee todos los campos del :ref:`Modelo Colores`.

Serializador ItemsSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Items`. Este es el serializador utilizado para las consultas de los ítems registrados en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_item","Id del ítem registrado."
        "sku", "Identificador único del ítem."
        "descripcion", "Descripción del ítem."
        "imagen", "Url de la imagen asociada al ítem."
        "taller", "Id del taller al que pertenece el ítem."
        "taller_nombre", "Nombre del taller al que pertenece el ítem."
        "cantdetalles", "Cantidad de detalles asociados al ítem."
        "cantcolores", "Cantidad de colores asociados al ítem."
