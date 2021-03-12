*****************
**Modelos ubc**
*****************

Dentro de la carpeta **ubc** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación ubc

Modelo Regiones
================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las regiones que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_region","Id de la región registrada."
        "nombre", "Nombre de la región."
        "estado", "Id del estado de la región puede ser activo o inactivo."

Modelo Paises
==============

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los países que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_pais","Id del país registrado."
        "nombre", "Nombre del país."
        "iniciales", "Iniciales del país (2 caracteres)."
        "region", "Id de la región a la que pertenece el pais."
        "aut_externo", "Indica si los usuarios de el país tienen permitido realizar solicitudes con proveedores externos."
        "estado", "Id del estado del país puede ser activo o inactivo."
        "bandera","Url de la imagen de bandera del país."
        "simbolo_moneda", "Símbolo de la moneda del país."
        "decimales", "Indica si los valores monetarios del país utilizan o no decimales."
        "zona_horaria", "Zona horaria en la que se encuentra el país."
        "documentos_obligatorios", "Indica si los usuarios del país deben cargar documentos de manera obligatoria."
        
Modelo Localidades
===================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las localidades que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_localidad","Id de la localidad registrada."
        "nombre", "Nombre de la localidad."
        "pais", "Id del país al que pertenece la localidad."
        "estado", "Id del estado de la localidad puede ser activo o inactivo."

Modelo Zonas
===================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las zonas que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_zona","Id de la zona registrada."
        "nombre", "Nombre de la zona."
        "pais", "Id del país al que pertenece la zona."
        "estado", "Id del estado de la zona puede ser activo o inactivo."

Modelo Ciudades
================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para las ciudades que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_ciudad","Id de la ciudad registrada."
        "nombre", "Nombre de la ciudad."
        "localidad", "Id de la localidad a la que pertenece la ciudad."
        "pais", "Id del país al que pertenece la ciudad."
        "estado", "Id del estado de la ciudad puede ser activo o inactivo."

Modelo Sectores
================

Modelo que hereda de :ref:`ClaseModelo`. Este es el modelo para los sectores que se registrarán en el sistema, consta de los siguientes campos:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_sector","Id del sector registrado."
        "nombre", "Nombre del sector."
        "zona", "Id de la zona a la que pertenece el sector."
        "pais", "Id del país al que pertenece el sector."
        "estado", "Id del estado del sector puede ser activo o inactivo."
