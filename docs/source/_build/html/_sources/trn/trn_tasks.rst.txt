****************
**Tareas trn**
****************

Dentro de la carpeta **trn** tenemos el archivo llamado ``tasks.py``. Donde se encuentran las tareas en segundo plano de la aplicación trn

Tarea enviarReporte
=========================

Tarea que se encarga que enviar un correo electrónico a los usuarios configurados para la recepción del reporte mensual de órdenes de trabajo, esta tarea recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "correos", "Listado de correos electrónico a los que se les envía el reporte."
		"usuario", "Usuario administrador quien configura el envío de correos."

Tarea enviarCorreoCliente
==========================

Tarea que se encarga que enviar un correo electrónico al cliente con información de la órden de trabajo generada, esta tarea recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_orden", "Id de la órden de trabajo generada."

Tarea enviarCorreoZonal
==========================

Tarea que se encarga que enviar un correo electrónico al jefe zonal con información de una órden de trabajo, esta tarea recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id_orden", "Id de la órden de trabajo generada."
