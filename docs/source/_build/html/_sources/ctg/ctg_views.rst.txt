*******************
**Views ctg**
*******************

Dentro de la carpeta **ctg** tenemos el archivo llamado ``views.py``. Donde se encuentran las vistas de la aplicación ctg, se detalla a continuación cada vista.

Vista DivisionesListaView
==========================

Vista basada en clases, hace el llamado al :ref:`Template divisiones_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_divisiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Divisiones` obteniendo el listado de las divisiones filtrando por taller.

Vista DivisionesCrearView
==========================

Vista basada en clases que hace el llamado al :ref:`Template divisiones_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_divisiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Divisiones` mediante el uso del formulario :ref:`Formulario DivisionForm`. Esta vista crea un nuevo registro de división para un taller determinado.

Vista DivisionesEditarView
===========================

Vista basada en clases que hace el llamado al :ref:`Template divisiones_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_divisiones`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Divisiones` mediante el uso del formulario :ref:`Formulario DivisionForm`. Esta vista actualiza los valores de una división determinada.

Vista ActualizarDivisionModal
==============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_division_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_divisiones`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una división, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"division", "Objeto de la división que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una división:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista BusquedaDivisionesApiView
================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de las divisiones de un taller determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"taller", "Id del taller del cual se requieren las divisiones."
		"tipo", "El tipo de catálogo al que pertenecen las divisiones que se requieren."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador DivisionesSerializer`, luego se envía la respuesta al template.

Vista CategoriasListaView
==========================

Vista basada en clases, hace el llamado al :ref:`Template categorias_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_categorias`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Categorias` obteniendo el listado de las categorías filtrando por taller.

Vista CategoriasCrearView
==========================

Vista basada en clases que hace el llamado al :ref:`Template categorias_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_categorias`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Categorias` mediante el uso del formulario :ref:`Formulario CategoriaForm`. Esta vista crea un nuevo registro de categoría para un taller determinado.

Vista CategoriasEditarView
===========================

Vista basada en clases que hace el llamado al :ref:`Template categorias_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_categorias`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Categorias` mediante el uso del formulario :ref:`Formulario CategoriaForm`. Esta vista actualiza los valores de una categoría determinada.

Vista ActualizarCategoriaModal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_categoria_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_categorias`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una categoría, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"categoria", "Objeto de la categoría que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una categoría:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista BusquedaCategoriasApiView
================================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de las categorías de un taller determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"division", "Id de la división de la cual se requieren las categorías."
		"tipo", "El tipo de catálogo al que pertenecen las categorías que se requieren."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador CategoriasSerializer`, luego se envía la respuesta al template.

Vista TallasListaView
==========================

Vista basada en clases, hace el llamado al :ref:`Template tallas_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_tallas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Tallas` obteniendo el listado de las tallas filtrando por taller.

Vista TallasCrearView
==========================

Vista basada en clases que hace el llamado al :ref:`Template tallas_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_tallas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Tallas` mediante el uso del formulario :ref:`Formulario TallasForm`. Esta vista crea un nuevo registro de talla para un taller determinado.

Vista TallasEditarView
===========================

Vista basada en clases que hace el llamado al :ref:`Template tallas_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_tallas`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Tallas` mediante el uso del formulario :ref:`Formulario TallasForm`. Esta vista actualiza los valores de una talla determinada.

Vista ActualizarTallaModal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_talla_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_tallas`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una talla, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"talla", "Objeto de la talla que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una talla:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista ColoresListaView
==========================

Vista basada en clases, hace el llamado al :ref:`Template colores_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_colores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Colores` obteniendo el listado de los colores filtrando por taller.

Vista ColoresCrearView
==========================

Vista basada en clases que hace el llamado al :ref:`Template colores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_colores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Colores` mediante el uso del formulario :ref:`Formulario ColoresForm`. Esta vista crea un nuevo registro de color para un taller determinado.

Vista ColoresEditarView
===========================

Vista basada en clases que hace el llamado al :ref:`Template colores_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_colores`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Colores` mediante el uso del formulario :ref:`Formulario ColoresForm`. Esta vista actualiza los valores de un color determinado.

Vista ActualizarColorModal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_color_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_colores`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un color, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"color", "Objeto del color que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un color:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista AdicionalesListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template adicionales_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_adicionales`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Adicionales` obteniendo el listado de los adicionales filtrando por taller.

Vista AdicionalesModalListaView
================================

Vista basada en clases, hace el llamado al :ref:`Template adicional_agregar_modal`. Esta vista hereda de :ref:`Vista AdicionalesListaView`, con esta vista se obteniene el listado de los adicionales pertenecientes a una categoría y un taller específico.

Vista AdicionalesCrearView
===========================

Vista basada en clases que hace el llamado al :ref:`Template adicionales_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_adicionales`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Adicionales` mediante el uso del formulario :ref:`Formulario AdicionalesForm`. Esta vista crea un nuevo registro de adicional para un taller determinado.

Vista DetalleAdicionalCrearView
================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_adicional_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_adicionales`` respectivamente para acceder a la misma, realiza el proceso de registrar las categorías en que estará disponible un adicional determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "categorias_lista", "Listado de categorías que pertenecen a un taller determinado."
		"form", "Instancia del :ref:`Formulario AdicionalesForm`."
        "adicional", "Objeto del adicional al cual se le resgistran las categorías en que estará disponible."
        "categorias_adicional_lista", "Arreglo que contiene los id's de las categorías registradas para el adicional."

Método POST
------------
Recibe los siguientes datos en formato JSON para registrar las categorías en que estará disponible un adicional:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
        "categorias[]", "Arreglo que contiene los id's de las categorías que se registran para el adicional."

Vista AdicionalesEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template adicionales_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_adicionales`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Adicionales` mediante el uso del formulario :ref:`Formulario AdicionalesForm`. Esta vista actualiza los valores de un adicional determinado.

Vista ActualizarAdicionalModal
===============================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_adicional_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_adicionales`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un adicional, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"adicional", "Objeto del adicional que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un adicional:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista adicionalDetalleView
===============================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_adicional_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_adicionales`` respectivamente para acceder a la misma, obtiene la informaciónde un adicional en específico, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"adicional", "Objeto del adicional que se va a modificar de ser el caso."
	"categorias", "Listado de categorías en la que está disponible el adicional."

Vista PiedrasListaView
===========================

Vista basada en clases, hace el llamado al :ref:`Template piedras_lista`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_piedras`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.ListView`` la cual afecta el :ref:`Modelo Piedras` obteniendo el listado de las piedras filtrando por taller.

Vista PiedrasModalListaView
================================

Vista basada en clases, hace el llamado al :ref:`Template piedra_agregar_modal`. Esta vista hereda de :ref:`Vista PiedrasListaView`, con esta vista se obteniene el listado de las piedras pertenecientes a una categoría y un taller específico.

Vista PiedrasCrearView
===========================

Vista basada en clases que hace el llamado al :ref:`Template piedras_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_piedras`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Piedras` mediante el uso del formulario :ref:`Formulario PiedrasForm`. Esta vista crea un nuevo registro de piedra para un taller determinado.

Vista PiedrasEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template piedras_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Piedras` mediante el uso del formulario :ref:`Formulario PiedrasForm`. Esta vista actualiza los valores de una piedra determinada.

Vista DetallePiedraCrearView
================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_piedra_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_piedras`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "categorias_lista", "Listado de categorías que pertenecen a un taller determinado."
		"form", "Instancia del :ref:`Formulario PiedrasForm`."
		"detalles", "Listado de detalles que pertenecen a la piedra."
        "piedra", "Objeto de la piedra que se está consultando."
        "num_detalles", "Cantidad de detalles que posee la piedra."

Vista DetallePiedraCategoriasView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_categorias_piedra_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` respectivamente para acceder a la misma, realiza el proceso de registrar las categorías en que estará disponible una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "categorias_lista", "Listado de categorías que pertenecen a un taller determinado."
		"form", "Instancia del :ref:`Formulario PiedrasForm`."
		"detalles", "Listado de detalles que pertenecen a la piedra."
        "piedra", "Objeto de la piedra a la cual se le resgistran las categorías en que estará disponible."
		"num_detalles", "Cantidad de detalles que posee la piedra."
        "categorias_piedra_lista", "Arreglo que contiene los id's de las categorías registradas para la piedra."

Método POST
------------
Recibe los siguientes datos en formato JSON para registrar las categorías en que estará disponible un adicional:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
        "categorias[]", "Arreglo que contiene los id's de las categorías que se registran para la piedra."

Vista DetallePiedraAgregarView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_piedra_agregar_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_piedras`` respectivamente para acceder a la misma, realiza el proceso de registrar un detalle para una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"form", "Instancia del :ref:`Formulario DetallesPiedraForm`."
        "piedra", "Objeto de la piedra a la cual se le registrarán los detalles."

Método POST
------------
Recibe los siguientes datos en formato JSON para registrar un nuevo detalle para una piedra determinada:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
        "medida", "Medida del detalle para la piedra."
		"costo", "Costo del detalle."

Vista DetallePiedraEditarView
==============================

Vista basada en clases que hace el llamado al :ref:`Template detalle_piedra_editar_modal`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo DetallePiedras` mediante el uso del formulario :ref:`Formulario DetallesPiedraForm`. Esta vista actualiza los valores de un detalle perteneciente a una piedra determinada.

Vista PiedraDetalleView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_piedra_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_piedras`` respectivamente para acceder a la misma, obtiene la información y detalles de una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "piedra", "Objeto de la piedra que se consulta."
		"detalles", "Listado de detalles que pertenecen a la piedra."
		"categorias", "Listado de categorías en que está disponible la piedra."

Vista ActualizarDetallePiedraModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_detalle_piedra_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un detalle de una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"detalle", "Objeto del detalle que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un detalle de piedra:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista DetallePiedraEliminarView
=================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_piedra_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método POST
------------
Elimina de la base de datos un detalle perteneciente a una piedra en específico, recibe como parámetro el id del detalle a eliminar.

Vista ActualizarPiedraModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_piedra_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_piedras`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"piedra", "Objeto de la piedra que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar una piedra:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista ProductosListaView
===================================

Vista basada en funciones, hace el llamado al :ref:`Template productos_lista`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, obtiene un listado de ítems de tipo productos con precio fijo y productos con precio gramo, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"precio_fijo", "Listado de ítems de tipo producto con precio fijo."
	"precio_gramo", "Listado de ítems de tipo producto con precio gramo."

Vista ServiciosListaView
===================================

Vista basada en funciones, hace el llamado al :ref:`Template servicios_lista`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, obtiene un listado de ítems de tipo servicio con precio fijo y servicio con precio gramo, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"precio_fijo", "Listado de ítems de tipo servicio con precio fijo."
	"precio_gramo", "Listado de ítems de tipo servicio con precio gramo."

Vista GramoListaView
===================================

Vista basada en funciones, hace el llamado al :ref:`Template catalogo_gramo`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, obtiene un listado de ítems de tipo producto con precio gramo y servicio con precio gramo, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"productos", "Listado de ítems de tipo producto con precio gramo."
	"servicios", "Listado de ítems de tipo servicio con precio gramo."
	"talleres", "Listado de talleres pertenecientes al país del usuario que consulta."

Vista BusquedaItemsApiView
============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la informacion de un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"clave", "Texto de búsqueda ingresado por el usuario que debe coincidir con la descripción del ítem."
		"tipo", "El tipo de catálogo al que pertenece el ítem."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ItemsSerializer`, luego se envía la respuesta al template.

Vista ItemsTodosApiView
============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de todos los ítems pertenecientes a un tipo de catálogo específico, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"tipo", "El tipo de catálogo al que pertenece los ítems."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ItemsSerializer`, luego se envía la respuesta al template.

Vista ItemsPorTallerApiView
============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de todos los ítems pertenecientes a un taller específico, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"tipo", "El tipo de catálogo al que pertenece los ítems."
		"taller", "Id del taller al que pertenecen los ítems."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ItemsSerializer`, luego se envía la respuesta al template.

Vista ItemsPorDivisionApiView
==============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de todos los ítems pertenecientes a una división específica, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"tipo", "El tipo de catálogo al que pertenece los ítems."
		"division", "Id de la división a la que pertenecen los ítems."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ItemsSerializer`, luego se envía la respuesta al template.

Vista ItemsPorCategoriaApiView
===============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la información de todos los ítems pertenecientes a una categoría específica, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"tipo", "El tipo de catálogo al que pertenece los ítems."
		"categoria", "Id de la categoría a la que pertenecen los ítems."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador ItemsSerializer`, luego se envía la respuesta al template.

Vista FijoListaView
===================================

Vista basada en funciones, hace el llamado al :ref:`Template catalogo_fijo`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, obtiene un listado de ítems de tipo producto con precio fijo y servicio con precio fijo, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"productos", "Listado de ítems de tipo producto con precio fijo."
	"servicios", "Listado de ítems de tipo servicio con precio fijo."
	"talleres", "Listado de talleres pertenecientes al país del usuario que consulta."

Vista ItemsCrearView
===========================

Vista basada en clases que hace el llamado al :ref:`Template items_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_items`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.CreateView`` la cual afecta el modelo :ref:`Modelo Items` mediante el uso del formulario :ref:`Formulario ItemsForm`. Esta vista crea un nuevo registro de ítem para un taller determinado.

Vista ItemsEditarView
============================

Vista basada en clases que hace el llamado al :ref:`Template items_form`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_items`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo Items` mediante el uso del formulario :ref:`Formulario ItemsForm`. Esta vista actualiza los valores de un ítem determinado.

Vista DetalleCrearView
================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_items`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "colores_lista", "Listado de colores que pertenecen a un taller determinado."
		"form", "Instancia del :ref:`Formulario ItemsForm`."
		"detalles", "Listado de detalles que pertenecen al ítem."
        "item", "Objeto del ítem que se está consultando."
        "num_detalles", "Cantidad de detalles que posee el ítem."

Vista DetalleEditarView
==============================

Vista basada en clases que hace el llamado al :ref:`Template detalle_editar_modal`. Esta vista hereda de :ref:`Vista SinPermisos` para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_items`` para acceder a la misma, también hereda de la clase genérica de Django ``generic.UpdateView`` la cual afecta el modelo :ref:`Modelo DetalleItems` mediante el uso del formulario :ref:`Formulario DetallesForm`. Esta vista actualiza los valores de un detalle perteneciente a un ítem determinado.

Vista DetalleEliminarView
=================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_items`` respectivamente para acceder a la misma, cuenta con las siguientes acciones:

Método POST
------------
Elimina de la base de datos un detalle perteneciente a un ítem en específico, recibe como parámetro el id del detalle a eliminar.

Vista ActualizarDetalleItemModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template actualizar_detalle_item_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_items`` respectivamente para acceder a la misma, realiza el proceso de activar o inactivar un detalle de un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"detalle", "Objeto del detalle que se va a modificar de ser el caso."

Método POST
------------
Recibe los siguientes datos en formato JSON para activar o inactivar un detalle de ítem:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"estado","Su valor puede ser ACTIVO o INACTIVO según sea el caso."

Vista DetalleColoresAgregarView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalles_colores_form`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_items`` respectivamente para acceder a la misma, realiza el proceso de registrar los colores en que estará disponible un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "colores_lista", "Listado de colores que pertenecen a un taller determinado."
		"form", "Instancia del :ref:`Formulario ItemsForm`."
		"detalles", "Listado de detalles que pertenecen al ítem."
        "item", "Objeto del ítem al cual se le resgistran los colores en que estará disponible."
		"num_detalles", "Cantidad de detalles que posee el ítem."
        "colores_item_lista", "Arreglo que contiene los id's de los colores registrados para el ítem."

Método POST
------------
Recibe los siguientes datos en formato JSON para registrar los colores en que estará disponible un ítem:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
        "colores[]", "Arreglo que contiene los id's de los colores que se registran para el ítem."

Vista DetalleAgregarView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_agregar_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.add_items`` respectivamente para acceder a la misma, realiza el proceso de registrar un detalle para un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"form", "Instancia del :ref:`Formulario DetallesForm`."
        "item", "Objeto del ítem al cual se le registrarán los detalles."
		"sin_talla", "Objeto que corresponde a la talla denominada SIN TALLA."
		"tallas", "Listado de tallas que pertenecen a un taller determinado."

Método POST
------------
Recibe los siguientes datos en formato JSON para registrar un nuevo detalle para un ítem determinado:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80
        
	"talla_min","Talla mínima de fabricación del ítem (si tipo = 1)."
	"talla_max","Talla máxima de fabricación del ítem (si tipo = 1)."
	"medida","Medida de fabricación del ítem (si tipo = 2)."
	"peso_minimo","Peso mínimo de fabricación del ítem."
	"peso_maximo","Peso máximo de fabricación del ítem."
	"cantidad_piedras","Cantidad de piedras que posee el ítem."
	"costo_piedras","Costo de las piedras que posee el ítem."
	"unidad_medida_id","Id de la unidad de medida asignada al ítem."
	"tipo", "Identificador del tipo de guardado 1 para talla 2 para longitud."

Vista ItemDetalleView
==================================

Vista basada en funciones, hace el llamado al :ref:`Template detalle_item_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, obtiene la información y detalles de un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

        "item", "Objeto del ítem que se consulta."
		"detalles", "Listado de detalles que pertenecen al ítem."
		"colores", "Listado de colores en que está disponible el ítem."

Vista InactivarItemModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template inactivar_item_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_items`` respectivamente para acceder a la misma, realiza el proceso de inactivar un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"item", "Objeto del ítem que se va a modificar de ser el caso."

Método POST
------------
Cambia el estado del ítem seleccionado a INACTIVO, recibe el id del ítem a inactivar.

Vista ActivarItemModal
===================================

Vista basada en funciones, hace el llamado al :ref:`Template inactivar_item_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.change_items`` respectivamente para acceder a la misma, realiza el proceso de activar un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"item", "Objeto del ítem que se va a modificar de ser el caso."

Método POST
------------
Cambia el estado del ítem seleccionado a ACTIVO, recibe el id del ítem a activar.

Vista ContarCotizacion
===================================

Vista basada en funciones, hace el llamado al :ref:`Template contar_cotizacion_modal`. Esta vista utiliza los decoradores ``@login_required`` y ``@permission_required`` propios de Django para validar si el usuario se encuentra autenticado y si cuenta con el permiso ``ctg.view_items`` respectivamente para acceder a la misma, realiza el proceso de registrar una nueva cotización de un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Envía el siguiente contexto hacia el template:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"item", "Objeto del ítem que se cotiza."

Método POST
------------
Crea un registro en el modelo :ref:`Modelo ConteoCotizaciones`, recibe como parámetro el tipo de cotización que se realiza 1 si se cotiza por un cliente o 2 si se cotiza por una consulta de un empleado.

Vista BusquedaDetalle
============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la informacion de un detalle perteneciente a un ítem determinado, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"item", "Id del ítem al que pertenece el detalle."
		"medida", "Id del detalle del que se desea obtener la información."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador DetallesSerializer`, luego se envía la respuesta al template.

Vista BusquedaDetallePiedra
============================

Vista de tipo ``APIView`` un tipo de vista perteneciente a ``rest_framework.views``. Se utiliza para obtener la informacion de un detalle perteneciente a una piedra determinada, cuenta con las siguientes acciones:

Método GET
-----------
Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

		"id_detalle", "Id del detalle de piedra del que se desea obtener la información."

Para procesar los datos obtenidos se utiliza el :ref:`Serializador DetallePiedraSerializer`, luego se envía la respuesta al template.
