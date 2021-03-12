***********************
**Serializadores clt**
***********************

Dentro de la carpeta **clt** tenemos el archivo llamado ``serializers.py``. Donde se encuentran los serializadores de la aplicación clt

Serializador ClientesSerializer
==================================

Serializador que hereda de ``serializers.ModelSerializer`` de rest_framework, y que utiliza el :ref:`Modelo Clientes`. Este es el serializador utilizado para las consultas de los clientes registrados en el sistema, posee todos los campos del :ref:`Modelo Clientes`.
