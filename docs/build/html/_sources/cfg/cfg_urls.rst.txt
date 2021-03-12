***************
**URLs cfg**
***************

Dentro de la carpeta **cfg** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación cfg, se detalla a continuación cada ruta

url cfg_pais_editar
====================

``/configuracion/pais/<int:pk>`` Ruta a la página para editar los parámetros generales a nivel de país en el sistema, hace un llamado a la :ref:`Vista CfgPaisEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del pais a configurar ``pais_id``."

url cfg_ope_editar
===================

``/configuracion/operaciones/<int:pk>`` Ruta hacia la página de configuración de los parámetros generales para una empresa determinada, hace un llamado a la :ref:`Vista CfgOpEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la configuración general del usuario ``config_gen_id``."

url calcular_porcentajes
=========================

``/configuracion/porcentajes/modal/<int:pk>`` Ruta que abre el modal para calcular los porcentajes de utilidades que se deben aplicar a los costos para llegar a un precio por gramo determinado, hace un llamado a la :ref:`Vista CalculadoraPorcentajesView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la configuración general del usuario ``config_gen_id``."

url cfg_tal_editar
===================

``/configuracion/taller/<int:pk>`` Ruta hacia la página de configuración de los parámetros generales para un taller determinado, hace un llamado a la :ref:`Vista CfgTalEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del taller a configurar ``taller_id``."

url cfg_ope_tal
================

``/configuracion/ope-taller/`` Ruta hacia la pantalla de configuración de porcentajes de utilidad sobre talleres aplicados de forma individual, hace un llamado a la :ref:`Vista CfgOperacionesTaller`.

url cfg_ope_prv
================

``/configuracion/ope-proveedor/`` Ruta hacia la pantalla de configuración de porcentajes de utilidad sobre proveedores aplicados de forma individual, hace un llamado a la :ref:`Vista CfgOperacionesProveedor`.

url cfg_tmp_vta
================

``/configuracion/tiempo-venta/`` Ruta hacia la pantalla de configuración de tiempo límite de venta aplicados de forma individual a los usuarios, hace un llamado a la :ref:`Vista CfgTiempoVenta`.

url cfg_aut_ext
================

``/configuracion/aut-externo/`` Ruta hacia la pantalla de configuración de autorización a externos aplicados de forma individual a los usuarios, hace un llamado a la :ref:`Vista CfgPermitirExterno`.

url cfg_rubros_lista
=====================

``/configuracion/rubros/lista/`` Ruta hacia la pantalla del listado de rubros registrados para un taller determinado, hace un llamado a la :ref:`Vista RubrosListaView`.

url cfg_rubros_form
=====================

``/configuracion/rubros/form/<int:pk>`` Ruta que abre el modal para crear o editar un rubro para un taller determinado, hace un llamado a la :ref:`Vista RubrosFormView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del rubro a editar ``id_rubro``."

url cfg_rubros_actualizar
==========================

``/configuracion/rubros/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un rubro para un taller determinado, hace un llamado a la :ref:`Vista ActualizarRubroModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del rubro a editar ``id_rubro``."

url cfg_envio_reportes
=======================

``/reportes/envio/<int:id_usuario>`` Ruta hacia la pantalla de configuración para el envío de reportes mensual para una empresa determinada, hace un llamado a la :ref:`Vista EnvioReportesView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_usuario","De tipo entero, se refiere al id del usuario que realiza la configuración ``id``."
