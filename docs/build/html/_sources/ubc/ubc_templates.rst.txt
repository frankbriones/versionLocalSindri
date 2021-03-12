*******************
**Templates ubc**
*******************

Dentro de la carpeta **ubc** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación ubc correspondiente a la creación, consulta y modificación de clientes en el sistema.

Template actualizar_ciudad_modal
==================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una ciudad, las funciones que posee este template son las siguientes:

Función actualizarCiudad
--------------------------

Realiza una petición de tipo POST a la :ref:`url ciudades_actualizar` enviando como parámetro el id de la ciudad a actualizar.

Template actualizar_localidad_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una localidad, las funciones que posee este template son las siguientes:

Función actualizarLocalidad
----------------------------

Realiza una petición de tipo POST a la :ref:`url localidades_actualizar` enviando como parámetro el id de la localidad a actualizar.

Template actualizar_sector_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un sector, las funciones que posee este template son las siguientes:

Función actualizarSector
----------------------------

Realiza una petición de tipo POST a la :ref:`url sectores_actualizar` enviando como parámetro el id del sector a actualizar.

Template actualizar_zona_modal
==================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una zona, las funciones que posee este template son las siguientes:

Función actualizarZona
--------------------------

Realiza una petición de tipo POST a la :ref:`url zonas_actualizar` enviando como parámetro el id de la zona a actualizar.

Template ciudades_form
=======================

Template de la pantalla que permite crear o editar una ciudad para un país determinado, realiza una petición de tipo POST a la :ref:`url ciudades_crear` en caso de creación de una ciudad, y una petición de tipo POST a la :ref:`url ciudades_editar` en caso de modificar los datos de una ciudad enviando como parámetro el id de la ciudad a editar.

Template ciudades_lista
========================

Template de la pantalla para consultar todas las ciudades que pertenezcan al mismo país. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_ciudad_modal` y a la pantalla de creación o edición de ciudades :ref:`Template ciudades_form`. Para la consulta de las ciudades se realiza una petición de tipo GET a la :ref:`url ciudades_lista`.

Template localidades_form
===========================

Template de la pantalla que permite crear o editar una localidad para un país determinado, realiza una petición de tipo POST a la :ref:`url localidades_crear` en caso de creación de una localidad, y una petición de tipo POST a la :ref:`url localidades_editar` en caso de modificar los datos de una localidad enviando como parámetro el id de la localidad a editar.

Template localidades_lista
===========================

Template de la pantalla para consultar todas las localidades que pertenezcan al mismo país. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_localidad_modal` y a la pantalla de creación o edición de localidades :ref:`Template localidades_form`. Para la consulta de las localidades se realiza una petición de tipo GET a la :ref:`url localidades_lista`.

Template paises_form
=======================

Template de la pantalla que permite crear o editar un país, realiza una petición de tipo POST a la :ref:`url paises_crear` en caso de creación de un país, y una petición de tipo POST a la :ref:`url paises_editar` en caso de modificar los datos de un país enviando como parámetro el id del país a editar.

Template paises_lista
========================

Template de la pantalla para consultar todos los países. Desde esta pantalla se puede acceder a la pantalla de creación o edición de países :ref:`Template paises_form`. Para la consulta de los países se realiza una petición de tipo GET a la :ref:`url paises_lista`.

Template regiones_form
=======================

Template de la pantalla que permite crear o editar una región determinada, realiza una petición de tipo POST a la :ref:`url regiones_crear` en caso de creación de una región, y una petición de tipo POST a la :ref:`url regiones_editar` en caso de modificar los datos de una región enviando como parámetro el id de la región a editar.

Template regiones_lista
========================

Template de la pantalla para consultar todas las regiones registradas en el sistema. Desde esta pantalla se puede acceder a la pantalla de creación o edición de regiones :ref:`Template regiones_form`. Para la consulta de las regiones se realiza una petición de tipo GET a la :ref:`url regiones_lista`.

Template sectores_form
=======================

Template de la pantalla que permite crear o editar un sector para un país determinado, realiza una petición de tipo POST a la :ref:`url sectores_crear` en caso de creación de un sector, y una petición de tipo POST a la :ref:`url sectores_editar` en caso de modificar los datos de un sector enviando como parámetro el id del sector a editar.

Template sectores_lista
========================

Template de la pantalla para consultar todas los sectores que pertenezcan a la misma zona. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_sector_modal` y a la pantalla de creación o edición de sectores :ref:`Template sectores_form`. Para la consulta de los sectores se realiza una petición de tipo GET a la :ref:`url sectores_lista`.

Template zonas_form
=======================

Template de la pantalla que permite crear o editar una zona para un país determinado, realiza una petición de tipo POST a la :ref:`url zonas_crear` en caso de creación de una zona, y una petición de tipo POST a la :ref:`url zonas_editar` en caso de modificar los datos de una zona enviando como parámetro el id de la zona a editar.

Template zonas_lista
========================

Template de la pantalla para consultar todas las zonas que pertenezcan al mismo país. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_zona_modal` y a la pantalla de creación o edición de zonas :ref:`Template zonas_form`. Para la consulta de las zonas se realiza una petición de tipo GET a la :ref:`url zonas_lista`.
