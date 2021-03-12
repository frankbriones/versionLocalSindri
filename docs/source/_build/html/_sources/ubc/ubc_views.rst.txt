*******************
**Views ubc**
*******************

Dentro de la carpeta **ubc** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación ubc, se detalla a continuación cada vista.

Vista RegionesListaView
========================

Vista basada en clases, hace el llamado al :ref:`Template regiones_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_regiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Regiones` obteniendo el listado de las regiones registradas en el sistema.

Vista RegionesCrearView
========================

Vista basada en clases que hace el llamado al :ref:`Template regiones_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_regiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Regiones` mediante el uso del formulario :ref:`Formulario RegionForm`. Esta vista crea un nuevo registro de región.

Vista RegionesEditarView
=========================

Vista basada en clases que hace el llamado al :ref:`Template regiones_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_regiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Regiones` mediante el uso del formulario :ref:`Formulario RegionForm`. Esta vista actualiza los valores de una región determinada.

Vista PaisesListaView
======================

Vista basada en clases, hace el llamado al :ref:`Template paises_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_paises`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Paises` obteniendo el listado de los países registrados en el sistema.

Vista PaisesCrearView
========================

Vista basada en clases que hace el llamado al :ref:`Template paises_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_paises`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Paises` mediante el uso del formulario :ref:`Formulario PaisForm`. Esta vista crea un nuevo registro de país.

Vista PaisesEditarView
=========================

Vista basada en clases que hace el llamado al :ref:`Template paises_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_paises`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Paises` mediante el uso del formulario :ref:`Formulario PaisForm`. Esta vista actualiza los valores de un país determinado.

Vista LocalidadesListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template localidades_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_localidades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Localidades` obteniendo el listado de las localidades registradas filtrando por país.

Vista LocalidadesCrearView
============================

Vista basada en clases que hace el llamado al :ref:`Template localidades_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_localidades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Localidades` mediante el uso del formulario :ref:`Formulario LocalidadForm`. Esta vista crea un nuevo registro de localidad para un país determinado.

Vista LocalidadesEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template localidades_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_localidades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Localidades` mediante el uso del formulario :ref:`Formulario LocalidadForm`. Esta vista actualiza los valores de una localidad determinada.

Vista ActualizarLocalidadModal
================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_localidad_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_localidades`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una localidad, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"localidad", "Objeto de la localidad que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una localidad:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista ZonasListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template zonas_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_zonas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Zonas` obteniendo el listado de las zonas registradas filtrando por país.

Vista ZonasCrearView
============================

Vista basada en clases que hace el llamado al :ref:`Template zonas_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_zonas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Zonas` mediante el uso del formulario :ref:`Formulario ZonaForm`. Esta vista crea un nuevo registro de zona para un país determinado.

Vista ZonasEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template zonas_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_zonas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Zonas` mediante el uso del formulario :ref:`Formulario ZonaForm`. Esta vista actualiza los valores de una zona determinada.

Vista ActualizarZonaModal
================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_zona_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_zonas`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una zona, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"zona", "Objeto de la zona que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una zona:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista CiudadesListaView
=========================

Vista basada en clases, hace el llamado al :ref:`Template ciudades_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_ciudades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Ciudades` obteniendo el listado de las ciudades registradas filtrando por país.

Vista CiudadesCrearView
========================

Vista basada en clases que hace el llamado al :ref:`Template ciudades_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_ciudades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Ciudades` mediante el uso del formulario :ref:`Formulario CiudadForm`. Esta vista crea un nuevo registro de ciudad para un país determinado.

Vista CiudadEditarView
=========================

Vista basada en clases que hace el llamado al :ref:`Template ciudades_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_ciudades`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Ciudades` mediante el uso del formulario :ref:`Formulario CiudadForm`. Esta vista actualiza los valores de una ciudad determinada.

Vista ActualizarCiudadModal
============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_ciudad_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_ciudades`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una ciudad, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"ciudad", "Objeto de la ciudad que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una ciudad:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista SectoresListaView
=========================

Vista basada en clases, hace el llamado al :ref:`Template sectores_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.view_sectores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Sectores` obteniendo el listado de los sectores registrados filtrando por zona.

Vista SectoresCrearView
========================

Vista basada en clases que hace el llamado al :ref:`Template sectores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.add_sectores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Sectores` mediante el uso del formulario :ref:`Formulario SectorForm`. Esta vista crea un nuevo registro de sector para un país determinado.

Vista SectoresEditarView
=========================

Vista basada en clases que hace el llamado al :ref:`Template sectores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_sectores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Sectores` mediante el uso del formulario :ref:`Formulario SectorForm`. Esta vista actualiza los valores de un sector determinado.

Vista ActualizarSectorModal
============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_sector_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ubc.change_sectores`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un sector, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"sector", "Objeto del sector que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un sector:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."
