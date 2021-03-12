***************
**URLs ubc**
***************

Dentro de la carpeta **ubc** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación ubc, se detalla a continuación cada ruta

url regiones_lista
====================

``/regiones/lista`` Ruta hacia la pantalla del listado de regiones registradas en el sistema, hace un llamado a la :ref:`Vista RegionesListaView`.

url regiones_crear
===================

``/regiones/crear`` Ruta hacia la pantalla que permite crear una región en el sistema, hace un llamado a la :ref:`Vista RegionesCrearView`.

url regiones_editar
====================

``/regiones/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una región determinado, hace un llamado a la :ref:`Vista RegionesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la región a editar ``id_region``."

url paises_lista
====================

``/paises/lista`` Ruta hacia la pantalla del listado de países registrados en el sistema, hace un llamado a la :ref:`Vista PaisesListaView`.

url paises_crear
===================

``/paises/crear`` Ruta hacia la pantalla que permite crear un país en el sistema, hace un llamado a la :ref:`Vista PaisesCrearView`.

url paises_editar
====================

``/paises/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un país determinado, hace un llamado a la :ref:`Vista PaisesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del país a editar ``id_pais``."

url localidades_lista
======================

``/localidades/lista`` Ruta hacia la pantalla del listado de localidades de un país determinado, hace un llamado a la :ref:`Vista LocalidadesListaView`.

url localidades_crear
======================

``/localidades/crear`` Ruta hacia la pantalla que permite crear una localidad para un país determinado, hace un llamado a la :ref:`Vista LocalidadesCrearView`.

url localidades_editar
=======================

``/localidades/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una localidad de país determinado, hace un llamado a la :ref:`Vista LocalidadesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la localidad a editar ``id_localidad``."

url localidades_actualizar
===========================

``/localidades/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una localidad para un país determinado, hace un llamado a la :ref:`Vista ActualizarLocalidadModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la localidad a editar ``id_localidad``."

url zonas_lista
======================

``/zonas/lista`` Ruta hacia la pantalla del listado de zonas de un país determinado, hace un llamado a la :ref:`Vista ZonasListaView`.

url zonas_crear
======================

``/zonas/crear`` Ruta hacia la pantalla que permite crear una zona para un país determinado, hace un llamado a la :ref:`Vista ZonasCrearView`.

url zonas_editar
=======================

``/zonas/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una zona de país determinado, hace un llamado a la :ref:`Vista ZonasEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la zona a editar ``id_zona``."

url zonas_actualizar
===========================

``/zonas/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una zona para un país determinado, hace un llamado a la :ref:`Vista ActualizarZonaModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la zona a editar ``id_zona``."

url ciudades_lista
====================

``/ciudades/lista`` Ruta hacia la pantalla del listado de ciudades de un país determinado, hace un llamado a la :ref:`Vista CiudadesListaView`.

url ciudades_crear
===================

``/ciudades/crear`` Ruta hacia la pantalla que permite crear una ciudad para un país determinado, hace un llamado a la :ref:`Vista CiudadesCrearView`.

url ciudades_editar
====================

``/ciudades/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una ciudad de país determinado, hace un llamado a la :ref:`Vista CiudadEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la ciudad a editar ``id_ciudad``."

url ciudades_actualizar
=========================

``/ciudades/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una ciudad para un país determinado, hace un llamado a la :ref:`Vista ActualizarCiudadModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la ciudad a editar ``id_ciudad``."

url sectores_lista
====================

``/sectores/lista`` Ruta hacia la pantalla del listado de sectores de un país determinado, hace un llamado a la :ref:`Vista SectoresListaView`.

url sectores_crear
===================

``/sectores/crear`` Ruta hacia la pantalla que permite crear un sector para un país determinado, hace un llamado a la :ref:`Vista SectoresCrearView`.

url sectores_editar
====================

``/sectores/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un sector de país determinado, hace un llamado a la :ref:`Vista SectoresEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del sector a editar ``id_sector``."

url sectores_actualizar
=========================

``/sectores/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un sector para un país determinado, hace un llamado a la :ref:`Vista ActualizarSectorModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del sector a editar ``id_sector``."
