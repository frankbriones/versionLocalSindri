*******************
**Templates cfg**
*******************

Dentro de la carpeta **cfg** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación cfg correspondiente a las configuraciones que puede realizar el usuario para definir el comportamiento del sistema.

Template actualizar_rubro_modal
===============================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un rubro, las funciones que posee este template son las siguientes:

Función actualizarRubro
------------------------

Realiza una petición de tipo POST a la :ref:`url cfg_rubros_actualizar` enviando como parámetro el id del rubro a actualizar

Template cal_porcentajes_modal
==============================

Template del modal que permite calcular los porcentajes de utilidad que se deben aplicar tanto sobre el costo de gramo base como sobre el costo de fabricación de modo que el precio final del gramo sea igual al deseado por quien realiza la configuración, las funciones que posee este template son las siguientes:

Función CalcularPorcentajePromedio
-----------------------------------

Toma los valores ingresados por el usuario correspondientes a costo gramo base, costo gramo taller, porcentaje de impuestos y precio final de gramo fabricado, valida que el usuario ingresó todos los valores y que no existan valores negativos, luego calcula los porcentajes de utilidad promedio tanto para el costo gramo base como para el costo gramo taller

Función CalcularPorcentajeBase
-----------------------------------

Toma los valores ingresados por el usuario correspondientes a costo gramo base, costo gramo taller, porcentaje de impuestos, precio final de gramo fabricado y porcentaje de utilidad sobre costo gramo taller, valida que el usuario ingresó todos los valores y que no existan valores negativos, luego calcula el porcentaje de utilidad que se debe aplicar sobre el costo gramo base para que el precio gramo final corresponda al ingresado por el usuario.

Función CalcularPorcentajeTaller
-----------------------------------

Toma los valores ingresados por el usuario correspondientes a costo gramo base, costo gramo taller, porcentaje de impuestos, precio final de gramo fabricado y porcentaje de utilidad sobre costo gramo base, valida que el usuario ingresó todos los valores y que no existan valores negativos, luego calcula el porcentaje de utilidad que se debe aplicar sobre el costo gramo taller para que el precio gramo final corresponda al ingresado por el usuario.

Función guardar
----------------

Realiza una petición de tipo POST a la :ref:`url calcular_porcentajes` como parámetro se coloca el id de configuración del usuario que realiza la petición, la data que se envía en la petición corresponde a los datos ingresados por el usuario y los porcentajes calculados.

Template cfg_envio_reportes
===========================

Template de la pantalla para configurar el horario y los usuarios a los que el sistema enviará de forma automática un reporte mensual con la información de las transacciones del mes anterior a la fecha de envío, las funciones que posee este template son las siguientes:

Función guardarConfiguracion
-----------------------------

Realiza una petición de tipo POST a la url :ref:`url cfg_envio_reportes` como parámetro se coloca el id del usuario que realiza la petición, la data que se envía en la petición corresponde al día del mes y la hora seleccionada por el usuario para el envío además de un array que contiene los id's de los usuarios a los que se le enviará el reporte.

Template cfg_ext_form
======================

Template de la pantalla para configurar los usuarios a quienes se le permitirá realizar solicitudes directamente con los proveedores externos, en esta pantalla el usuario podrá configurar los permisos por usuario, por zona o por sector al que pertenecen los usuarios a configurar, las funciones que posee este template son las siguientes:

Función agregarConfiguracion
-----------------------------

Realiza una petición de tipo POST a la :ref:`url cfg_aut_ext`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"id_item","Corresponde al id sea del usuario, la zona o el sector."
	"tipo","1 para usuario, 2 para zona, 3 para sector."
	"aut_externo","Verdadero o falso para autorización de externo."


Template cfg_op_form
=====================

Template de la pantalla para realizar las configuraciones generales de los usuarios de tipo operaciones para una empresa en específico, realiza una petición de tipo POST a la :ref:`url cfg_ope_editar` enviando como parámetro el id de la configuración general del usuario, esta pantalla es solo para los usuarios de tipo operaciones y con rol de administrador.

Template cfg_ope_pro_form
==========================

Template de la pantalla que permite establecer los porcentajes de utilidad sobre la fabricación para los usuarios de tipo operaciones, en ella se puede configurar dicho porcentaje para cada usuario por proveedor de forma independiente, la configuración la puede hacer por usuario o por zona, las funciones que posee este template son las siguientes:

Función agregarConfiguracion
------------------------------

Realiza una petición de tipo POST a la :ref:`url cfg_ope_prv`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"id_item","Corresponde al id sea del usuario o la zona."
	"nombre","Username o nombre de la zona a configurar."
	"id_proveedor","Id del proveedor a configurar el porcentaje de utilidad."
	"prv_nombres","Nombres del proveedor."
	"prv_apellidos","Apellidos del proveedor."
	"tipo","1 para usuario, 2 para zona."
	"utilidad","Porcentaje de utilidad que se le asignará al proveedor para el usuario indicado."

Template cfg_ope_tal_form
==========================

Template de la pantalla que permite establecer el porcentaje de utilidad sobre los talleres de forma independiente, la configuración se puede realizar por usuario, por zona o por sector, las funciones que posee este template son las siguientes:

Función agregarConfiguracion
------------------------------

Realiza una petición de tipo POST a la :ref:`url cfg_ope_tal`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"id_item","Corresponde al id sea del usuario, la zona o el sector."
	"nombre","Username o nombre de la zona o sector a configurar."
	"id_taller","Id del taller a configurar el porcentaje de utilidad."
	"taller","Nombres del taller."
	"tipo","1 para usuario, 2 para zona, 3 para sector."
	"utilidad","Porcentaje de utilidad que se le asignará al taller para el usuario indicado."

Template cfg_pais_form
=======================

Template de la pantalla para realizar configuraciones generales que establecen el comportamiento del sistema para usuarios que pertenecen al mismo país, realiza una petición de tipo POST a la url ``cfg_pais_editar`` enviando como parámetro el id del país a configurar.

Template cfg_ta_form
=====================

Template de la pantalla para realizar las configuraciones generales de los usuarios de tipo taller para un taller en específico, realiza una petición de tipo POST a la :ref:`url cfg_tal_editar` enviando como parámetro el id del taller a configurar, esta pantalla es solo para los usuarios de tipo taller y con rol de administrador.

Template cfg_tmp_lim_form
==========================

Template de la pantalla para configurar el tiempo límite de venta que tendrán los usuarios de tipo operaciones que generen órdenes de trabajo, en esta pantalla el usuario administrador podrá configurar el tiempo límite por usuario, por zona o por sector al que pertenecen los usuarios a configurar, las funciones que posee este template son las siguientes:

Función agregarConfiguracion
-----------------------------

Realiza una petición de tipo POST a la :ref:`url cfg_tmp_vta`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"id_item","Corresponde al id sea del usuario, la zona o el sector."
	"tipo","1 para usuario, 2 para zona, 3 para sector."
	"tmp_lim_vta","Tiempo límite en días para que el usuario de por terminada la órden que generó."

Template rubro_form_modal
==========================

Template del modal que permite crear o editar un rubro para un taller determinado, realiza una petición de tipo POST a la :ref:`url cfg_rubros_form` en caso de edición de un rubro envia como parámetro el id del rubro a editar, esta pantalla es solo para los usuarios de tipo taller y con rol de administrador.

Template rubros_lista
======================

Template de la pantalla que permite visualizar los rubros registrados en un taller determinado, desde esta pantalla el usuario puede agregar, editar, activar o inactivar rubros para su taller. Para la consulta de los rubros se realiza una petición de tipo GET a la :ref:`url cfg_rubros_lista`.
