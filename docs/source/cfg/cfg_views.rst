*******************
**Views cfg**
*******************

Dentro de la carpeta **cfg** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación cfg, se detalla a continuación cada vista.

Vista CfgPaisEditarView
========================

Vista basada en clases que hace el llamado al :ref:`Template cfg_pais_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_paises`` para acceder a la misma, se trata de una vista de actualización ``generic.UpdateView`` la cual afecta el modelo ``Modelo Paises`` mediante el uso del formulario ``Formulario CfgPaisForm``. Esta vista actualiza los parámetros de configuración para un país determinado, estableciendo el comportamiento del sistema para todos los usuarios de dicho país.

Vista CfgOpEditarView
======================

Vista basada en clases que hace el llamado al :ref:`Template cfg_op_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_configgeneral`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo ``Modelo ConfigGeneral`` mediante el uso del formulario ``Formulario CfgOpeForm``. Esta vista actualiza los parámetros de configuración para una empresa determinada, estableciendo el comportamiento del sistema para todos los usuarios de dicha empresa.

Vista CalculadoraPorcentajesView
=================================

Vista basada en funciones, hace el llamado al :ref:`Template cal_porcentajes_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_configgeneral`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"configuracion","Objeto que contiene la configuración actual de la empresa a configurar."

Método POST
------------
Recibe los siguientes datos en formato JSON para editar la configuración:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
    
        "costo_gramo_base","Costo del gramo base que se establecerá para la empresa."
        "utilidad_sobre_base","Porcentaje de utilidad que se aplicará sobre el gramo base para todos los usuarios de la empresa."
        "utilidad_sobre_taller","Porcentaje de utilidad que se aplicará sobre el costo del taller para todos los usuarios de la empresa."
        "prct_impuestos","Porcentaje de impuestos que se aplicará a todas las transacciones que realizen los usuarios de la empresa."

Vista CfgTalEditarView
=========================

Vista basada en clases, hace el llamado al :ref:`Template cfg_ta_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``usr.change_taller`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo ``Modelo Taller`` mediante el uso del formulario ``Formulario CfgTalForm``. Esta vista actualiza los parámetros de configuración para un taller determinado, estableciendo el comportamiento del sistema para todos los usuarios de dicho taller.

Vista CfgOperacionesTaller
===========================

Vista basada en funciones, hace el llamado al :ref:`Template cfg_ope_tal_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_configutilidadtaller`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rel_usuarios","Registros de relaciones entre usuarios y talleres, se recuperan todos los usuarios de tipo operaciones pertenecientes a la empresa del usuario que realiza la configuración y todos los talleres del mismo país de quien realiza la configuración."
	"rel_zonas", "Registros de relaciones entre zonas y talleres, se obtienen las zonas y los talleres pertenecientes al país del usuario que realiza la configuración."
	"rel_sectores", "Registros de relaciones entre sectores y talleres, se obtienen los sectores y los talleres pertenecientes al país del usuario que realiza la configuración."
	"configuraciones", "Registros de configuraciones específicas realizadas previamente para los talleres registrados."

Método POST
------------
Recibe los siguientes datos en formato JSON para editar la configuración:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
    
        "id_item","Id del usuario, zona o sector al que se le va a configurar el porcentaje de utilidad para el taller especificado."
        "nombre","Nombre del usuario, zona o sector al que se le va a configurar el porcentaje de utilidad para el taller especificado."
        "id_taller","Id del taller al que se le va a establecer el porcentaje de utilidad."
        "taller","Nombre del taller al que se le va a establecer el porcentaje de utilidad."
		"tipo", "Tipo de configuración que se va a realizar. 1 para la relación usuario-taller, 2 para la relación zona-taller, 3 para la relación sector-taller."
		"utilidad", "Porcentaje de utilidad que se va a establecer."

Vista CfgOperacionesProveedor
==============================

Vista basada en funciones, hace el llamado al :ref:`Template cfg_ope_pro_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_configutilidadproveedor`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rel_usuarios","Registros de relaciones entre usuarios y proveedores, se recuperan todos los usuarios de tipo operaciones pertenecientes a la empresa del usuario que realiza la configuración y todos los proveedores del mismo país de quien realiza la configuración."
	"rel_zonas", "Registros de relaciones entre zonas y proveedores, se obtienen las zonas y los proveedores pertenecientes al país del usuario que realiza la configuración."
	"configuraciones", "Registros de configuraciones específicas realizadas previamente para los proveedores registrados."

Método POST
------------
Recibe los siguientes datos en formato JSON para editar la configuración:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
    
        "id_item","Id del usuario, zona o sector al que se le va a configurar el porcentaje de utilidad para el taller especificado."
        "nombre","Nombre del usuario, zona o sector al que se le va a configurar el porcentaje de utilidad para el taller especificado."
        "id_proveedor","Id del proveedor al que se le va a establecer el porcentaje de utilidad."
        "prv_nombres","Nombres del proveedor al que se le va a establecer el porcentaje de utilidad."
		"prv_apellidos", "Apellidos del proveedor al que se le va a establecer el porcentaje de utilidad."
		"tipo", "Tipo de configuración que se va a realizar. 1 para la relación usuario-proveedor, 2 para la relación zona-proveedor."
		"utilidad", "Porcentaje de utilidad que se va a establecer."

Vista CfgTiempoVenta
=====================

Vista basada en funciones, hace el llamado al :ref:`Template cfg_tmp_lim_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_usuarios`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rel_usuarios","Registros de todos los usuarios pertenecientes a la empresa del usuario que realiza la configuración."
	"rel_zonas", "Registros de las zonas pertenecientes al país del usuario que realiza la configuración."
	"rel_sectores", "Registros de los sectores pertenecientes al país del usuario que realiza la configuración."

Método POST
------------
Recibe los siguientes datos en formato JSON para editar la configuración:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"id_item","Id del usuario, zona o sector al que se le va a configurar el tiempo límite de venta."
	"tipo", "Tipo de configuración que se va a realizar. 1 para usuarios, 2 para zonas, 3 para sectores."
	"tmp_lim_vta", "Tiempo límite de venta que se va a establecer."

Vista CfgPermitirExterno
=========================

Vista basada en funciones, hace el llamado al :ref:`Template cfg_ext_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.change_usuarios`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rel_usuarios","Registros de todos los usuarios pertenecientes a la empresa del usuario que realiza la configuración."
	"rel_zonas", "Registros de las zonas pertenecientes al país del usuario que realiza la configuración."
	"rel_sectores", "Registros de los sectores pertenecientes al país del usuario que realiza la configuración."

Método POST
------------
Recibe los siguientes datos en formato JSON para editar la configuración:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"id_item","Id del usuario, zona o sector al que se le va a configurar si se permite solicitudes a externos o no."
	"tipo", "Tipo de configuración que se va a realizar. 1 para usuarios, 2 para zonas, 3 para sectores."
	"aut_externo", "Valor verdadero o falso para establecer si se permite o no solicitudes a externos."

Vista RubrosListaView
=======================

Vista basada en clases, hace el llamado al :ref:`Template rubros_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.view_rubrosasociados`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el modelo ``Modelo Taller`` obteniendo el listado de rubros filtrando por empresa o por taller dependiendo del tipo de usuario que realiza la consulta.

Vista RubrosFormView
=====================

Vista basada en funciones, hace el llamado al :ref:`Template rubro_form_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.add_rubrosasociados`` respectivamente para acceder a la misma, reliza el proceso de crear o modificar un rubro, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"form","Instancia del formulario ``RubrosForm``."
	"rubro", "Objeto del rubro que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para crear o editar un rubro:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"descripcion","Descripción para el rubro a crear o modificar."

Vista ActualizarRubroModal
===========================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_rubro_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``trn.change_rubrosasociados`` respectivamente para acceder a la misma, reliza el proceso de activar o inactivar un rubro, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"rubro", "Objeto del rubro que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un rubro:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista EnvioReportesView
========================

Vista basada en funciones, hace el llamado al :ref:`Template cfg_envio_reportes`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``cfg.env_reportes`` respectivamente para acceder a la misma, reliza el proceso de crear o editar una tarea periódica para el envío mensual de reportes de órdenes de trabajo, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"usuarios", "Queryset de objetos de los usuarios pertenecientes a la misma empresa o al mismo taller del usuario que realiza la configuración."
	"usuarios_registrados", "Usuarios que se encuentran registrados para el envío del reporte mensual, esto en caso de que se edite una tarea periódica creada anteriormente."
	"dia", "Día del mes registrado para el envío del reporte de órdenes de trabajo."
	"hora", "Hora del día registrada para el envío del reporte de órdenes de trabajo."

Método POST
------------
Recibe los siguientes datos en formato JSON para Crear o editar una tarea periódica para el envío del reporte:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"usuarios[]","Arreglo que contiene los Id's de los usuarios a los que se les enviará el reporte."
	"dia", "Día del mes a configurar para el envío del reporte de órdenes de trabajo."
	"hora", "Hora del día a configurar para el envío del reporte de órdenes de trabajo."
