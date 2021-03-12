*******************
**Templates ctg**
*******************

Dentro de la carpeta **ctg** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación ctg correspondiente a la creación, consulta y modificación de clientes en el sistema.

Template activar_item_modal
==================================

Template del modal que aparecerá cuando el usuario desea activar un ítem, las funciones que posee este template son las siguientes:

Función activarItem
--------------------------

Realiza una petición de tipo POST a la :ref:`url item_activar_modal` enviando como parámetro el id del ítem a activar.

Template inactivar_item_modal
==================================

Template del modal que aparecerá cuando el usuario desea inactivar un ítem, las funciones que posee este template son las siguientes:

Función inactivarItem
--------------------------

Realiza una petición de tipo POST a la :ref:`url item_inactivar_modal` enviando como parámetro el id del ítem a inactivar.

Template actualizar_adicional_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un adicional, las funciones que posee este template son las siguientes:

Función actualizarAdicional
-----------------------------

Realiza una petición de tipo POST a la :ref:`url adicionales_actualizar` enviando como parámetro el id del adicional a actualizar.

Template actualizar_categoria_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una categoría, las funciones que posee este template son las siguientes:

Función actualizarCategoria
-----------------------------

Realiza una petición de tipo POST a la :ref:`url categorias_actualizar` enviando como parámetro el id de la categoría a actualizar.

Template actualizar_color_modal
====================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un color, las funciones que posee este template son las siguientes:

Función actualizarColor
-----------------------------

Realiza una petición de tipo POST a la :ref:`url colores_actualizar` enviando como parámetro el id del color a actualizar.

Template actualizar_detalle_item_modal
=======================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un detalle de ítem, las funciones que posee este template son las siguientes:

Función actualizarDetalle
-----------------------------

Realiza una petición de tipo POST a la :ref:`url items_detalle_actualizar` enviando como parámetro el id del detalle a actualizar.

Template actualizar_detalle_piedra_modal
=========================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar un detalle de piedra, las funciones que posee este template son las siguientes:

Función actualizarDetallePiedra
---------------------------------

Realiza una petición de tipo POST a la :ref:`url detalles_piedra_actualizar` enviando como parámetro el id del detalle a actualizar.

Template actualizar_division_modal
=========================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una división, las funciones que posee este template son las siguientes:

Función actualizarDivision
---------------------------------

Realiza una petición de tipo POST a la :ref:`url divisiones_actualizar` enviando como parámetro el id de la división a actualizar.

Template actualizar_piedra_modal
=========================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una piedra, las funciones que posee este template son las siguientes:

Función actualizarPiedra
---------------------------------

Realiza una petición de tipo POST a la :ref:`url piedras_actualizar` enviando como parámetro el id de la piedra a actualizar.

Template actualizar_talla_modal
=========================================

Template del modal que aparecerá cuando el usuario desea activar o inactivar una talla, las funciones que posee este template son las siguientes:

Función actualizarTalla
---------------------------------

Realiza una petición de tipo POST a la :ref:`url tallas_actualizar` enviando como parámetro el id de la talla a actualizar.

Template adicional_agregar_modal
=========================================

Template del modal que aparecerá cuando el usuario desea agregar un adicional a la órden que está generando, en el modal se mostrarán los adicionales que estén disponibles para la transacción. Para la consulta de los adicionales realiza una petición de tipo GET a la :ref:`url adicionales_modal_lista`.

Template adicionales_form
==========================

Template de la pantalla que permite crear o editar un adicional para un taller determinado, realiza una petición de tipo POST a la :ref:`url adicionales_crear` en caso de creación de un adicional, y una petición de tipo POST a la :ref:`url adicionales_editar` en caso de modificar los datos de un adicional enviando como parámetro el id del adicional a editar, las funciones que posee este template son las siguientes:

Función validarImagen
----------------------

Valida si la imagen que se carga posee las extensiones de archivo permitidas y si el peso del archivo no supera el máximo permitido.

Función seleccionarImagen
--------------------------

Crea una vista previa de la imagen cargada en caso de que cumpla con la validación.

Template adicionales_lista
===========================

Template de la pantalla para consultar todos los adicionales que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_adicional_modal` y a la pantalla de creación o edición de adicionales :ref:`Template adicionales_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver adicionales. Para la consulta de los adicionales se realiza una petición de tipo GET a la :ref:`url adicionales_lista`.

Template catalogo_fijo
===========================

Template de la pantalla para consultar todos los ítems de tipo precio fijo que pertenezcan a un país, esta pantalla es solo para los usuarios de tipo operaciones y que posean el permiso para ver ítems. Para la consulta de los ítems se realiza una petición de tipo GET a la :ref:`url catalogo_fijo`, las funciones que posee este template son las siguientes:

Función buscarItems
----------------------

Obtiene los ítems cuyo nombre coincida con el texto ingresado por el usuario en la caja de texto buscar, para obtener los ítems realiza una petición de tipo GET a la :ref:`url buscar_items_api` enviando como parámetro el texto ingresado por el usuario.

Función buscarItemsTaller
--------------------------

Obtiene los ítems que pertenezcan a un taller en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_taller_api` enviando como parámetro el id del taller seleccionado por el usuario y el tipo de catálogo de los ítems.

Función buscarItemsDivision
----------------------------

Obtiene los ítems que pertenezcan a una división en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_division_api` enviando como parámetro el id de la división seleccionada por el usuario y el tipo de catálogo de los ítems.

Función buscarItemsCategoria
-----------------------------

Obtiene los ítems que pertenezcan a una categoría en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_categoria_api` enviando como parámetro el id de la categoría seleccionada por el usuario y el tipo de catálogo de los ítems.

Función cargarItems
-----------------------------

Genera los elementos HTML para mostrar la información de los ítems obtenidos en la consulta, recibe como parámetro un arreglo de objetos que contiene los ítems obtenidos y el tipo de catálogo al que pertenecen.

Función verDetalles
-----------------------------

Abre un modal que contiene la información detallada de un ítem en específico, para esto realiza una petición de tipo GET a la :ref:`url items_detalle` enviando como parámetro el id del ítem a consultar.

Función cargarDivisiones
-----------------------------

Obtiene las divisiones que pertenecen a un taller en específico seleccionado por el usuario, para esto realiza una petición de tipo GET a la :ref:`url divisiones_buscar_api` enviando como parámetro el id del taller a consultar y el tipo de catálogo de los ítems.

Función llenarDivisiones
-----------------------------

Llena el elemento HTML que contiene el listado de divisiones para el taller seleccionado, recibe como parámetro un arreglo de objetos que contiene las divisiones obtenidas y el tipo de catálogo al que pertenecen.

Función cargarCategorias
-----------------------------

Obtiene las categorías que pertenecen a una división en específico seleccionada por el usuario, para esto realiza una petición de tipo GET a la :ref:`url categorias_buscar_api` enviando como parámetro el id de la división a consultar y el tipo de catálogo de los ítems.

Función llenarCategorias
-----------------------------

Llena el elemento HTML que contiene el listado de categorías para la división seleccionada, recibe como parámetro un arreglo de objetos que contiene las categorías obtenidas y el tipo de catálogo al que pertenecen.

Template catalogo_gramo
===========================

Template de la pantalla para consultar todos los ítems de tipo precio gramo que pertenezcan a un país, esta pantalla es solo para los usuarios de tipo operaciones y que posean el permiso para ver ítems. Para la consulta de los ítems se realiza una petición de tipo GET a la :ref:`url catalogo_gramos`, las funciones que posee este template son las siguientes:

Función buscarItems
----------------------

Obtiene los ítems cuyo nombre coincida con el texto ingresado por el usuario en la caja de texto buscar, para obtener los ítems realiza una petición de tipo GET a la :ref:`url buscar_items_api` enviando como parámetro el texto ingresado por el usuario.

Función buscarItemsTaller
--------------------------

Obtiene los ítems que pertenezcan a un taller en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_taller_api` enviando como parámetro el id del taller seleccionado por el usuario y el tipo de catálogo de los ítems.

Función buscarItemsDivision
----------------------------

Obtiene los ítems que pertenezcan a una división en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_division_api` enviando como parámetro el id de la división seleccionada por el usuario y el tipo de catálogo de los ítems.

Función buscarItemsCategoria
-----------------------------

Obtiene los ítems que pertenezcan a una categoría en específico, para obtener los ítems realiza una petición de tipo GET a la :ref:`url items_categoria_api` enviando como parámetro el id de la categoría seleccionada por el usuario y el tipo de catálogo de los ítems.

Función cargarItems
-----------------------------

Genera los elementos HTML para mostrar la información de los ítems obtenidos en la consulta, recibe como parámetro un arreglo de objetos que contiene los ítems obtenidos y el tipo de catálogo al que pertenecen.

Función verDetalles
-----------------------------

Abre un modal que contiene la información detallada de un ítem en específico, para esto realiza una petición de tipo GET a la :ref:`url items_detalle` enviando como parámetro el id del ítem a consultar.

Función cargarDivisiones
-----------------------------

Obtiene las divisiones que pertenecen a un taller en específico seleccionado por el usuario, para esto realiza una petición de tipo GET a la :ref:`url divisiones_buscar_api` enviando como parámetro el id del taller a consultar y el tipo de catálogo de los ítems.

Función llenarDivisiones
-----------------------------

Llena el elemento HTML que contiene el listado de divisiones para el taller seleccionado, recibe como parámetro un arreglo de objetos que contiene las divisiones obtenidas y el tipo de catálogo al que pertenecen.

Función cargarCategorias
-----------------------------

Obtiene las categorías que pertenecen a una división en específico seleccionada por el usuario, para esto realiza una petición de tipo GET a la :ref:`url categorias_buscar_api` enviando como parámetro el id de la división a consultar y el tipo de catálogo de los ítems.

Función llenarCategorias
-----------------------------

Llena el elemento HTML que contiene el listado de categorías para la división seleccionada, recibe como parámetro un arreglo de objetos que contiene las categorías obtenidas y el tipo de catálogo al que pertenecen.

Template categorias_form
==========================

Template de la pantalla que permite crear o editar una categoría para un taller determinado, realiza una petición de tipo POST a la :ref:`url categorias_crear` en caso de creación de una categoría, y una petición de tipo POST a la :ref:`url categorias_editar` en caso de modificar los datos de una categoría enviando como parámetro el id de la categoría a editar.

Template categorias_lista
===========================

Template de la pantalla para consultar todas las categorías que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_categoria_modal` y a la pantalla de creación o edición de categorías :ref:`Template categorias_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver categorías. Para la consulta de las categorías se realiza una petición de tipo GET a la :ref:`url categorias_lista`.

Template colores_form
==========================

Template de la pantalla que permite crear o editar un color para un taller determinado, realiza una petición de tipo POST a la :ref:`url colores_crear` en caso de creación de un color, y una petición de tipo POST a la :ref:`url colores_editar` en caso de modificar los datos de un color enviando como parámetro el id del color a editar.

Template colores_lista
===========================

Template de la pantalla para consultar todos los colores que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_color_modal` y a la pantalla de creación o edición de colores :ref:`Template colores_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver colores. Para la consulta de los colores se realiza una petición de tipo GET a la :ref:`url colores_lista`.

Template contar_cotizacion_modal
=================================

Template del modal desde donde se contabiliza la cantidad de veces en que un ítem es cotizado, las funciones que posee este template son las siguientes:

Función guardarCotizacion
--------------------------

Realiza una petición de tipo POST a la :ref:`url contar_cotizacion` enviando como parámetro el id del ítem que se va a cotizar y el tipo sea 1 si se cotiza por un cliente o 2 si se cotiza por una consulta de un empleado, esto para registrar una nueva cotización.

Template detalle_adicional_modal
=================================

Template del modal donde se muestra la información detallada de un adicional esta pantalla es solo para los usuarios de tipo operaciones y que posean el permiso para ver adicionales. Para la consulta realiza una petición de tipo GET a la :ref:`url adicional_detalle_modal` enviando como parámetro el id del adicional a consultar.

Template detalle_agregar_modal
=================================

Template del modal que permite al usuario agregar detalles a un ítem en específico, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para modificar ítems. Realiza una petición de tipo POST a la :ref:`url detalles_agregar`, la data que se envía en la petición se describe a continuación:

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

Template detalle_editar_modal
==============================

Template del modal que permite al usuario modificar los valores de un detalle perteneciente a un ítem en específico, realiza una petición de tipo POST a la :ref:`url items_detalle_editar` para modificar los datos de un detalle de ítem enviando como parámetro el id del detalle a editar.

Template detalle_item_modal
==============================

Template del modal que permite al usuario ver los detalles de un ítem en específico, realiza una petición de tipo GET a la :ref:`url items_detalle` para ver los detalles del ítem y poder realizar una cotización o solicitud de trabajo.

Template detalle_piedra_agregar_modal
=======================================

Template del modal que permite al usuario agregar detalles a una piedra en específico, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para modificar piedras. Realiza una petición de tipo POST a la :ref:`url detalles_piedra_agregar`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"medida","Medida del detalle de la piedra."
	"costo","Costo especificado para el detalle de piedra."

Template detalle_piedra_editar_modal
=====================================

Template del modal que permite al usuario modificar los valores de un detalle perteneciente a una piedra en específico, realiza una petición de tipo POST a la :ref:`url detalles_piedra_editar` para modificar los datos de un detalle de piedra enviando como parámetro el id del detalle a editar.

Template detalle_piedra_modal
==============================

Template del modal que permite al usuario ver los detalles de una piedra en específico, realiza una petición de tipo GET a la :ref:`url piedra_detalle_modal` para ver los detalles de la piedra con sus medidas y categorías en las que se encuentra disponible.

Template detalles_adicional_form
=======================================

Template de la pantalla que permite al usuario agregar las categorías para las que estará disponible a un adicional en específico, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para modificar adicionales. Realiza una petición de tipo POST a la :ref:`url detalles_adicional_crear`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"categorias[]","Arreglo que contiene los id's de las categorías en las que estará disponible el adicional."

Template detalles_categorias_piedra_form
==========================================

Template de la pantalla que permite al usuario agregar las categorías para las que estará disponible a una piedra en específico, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para modificar piedras. Realiza una petición de tipo POST a la :ref:`url detalles_piedra_categorias_agregar`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"categorias[]","Arreglo que contiene los id's de las categorías en las que estará disponible la piedra."

Template detalles_colores_form
==========================================

Template de la pantalla que permite al usuario agregar los colores en que estará disponible un ítem en específico, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para modificar ítems. Realiza una petición de tipo POST a la :ref:`url detalles_colores_agregar`, la data que se envía en la petición se describe a continuación:

.. csv-table::
	:header: "**Dato**","**Descripción**"
	:widths: 20, 80

	"colores[]","Arreglo que contiene los id's de los colores en las que estará disponible el ítem."

Template detalles_form
=================================

Template de la pantalla que le permite al usuario agregar o eliminar detalles para un ítem en específico, para consultar la información del ítem realiza una petición de tipo GET a la :ref:`url detalles_crear` las funciones que posee este template son las siguientes:

Función guardarItem
--------------------------

Valida si el usuario tiene agregado al menos un detalle al ítem consultado de ser así lo redirige a la :ref:`url detalles_colores_agregar` enviando como parámetro el id del ítem.

Función EliminarDetalle
--------------------------

Elimina un detalle específico para el ítem consultado, para ello realiza una petición de tipo POST a la :ref:`url items_detalle_eliminar` enviando como parámetro el id del detalle a eliminar.

Template detalles_piedra_form
=================================

Template de la pantalla que le permite al usuario agregar o eliminar detalles para una piedra en específico, para consultar la información de la piedra realiza una petición de tipo GET a la :ref:`url detalles_piedra_crear` las funciones que posee este template son las siguientes:

Función guardarItem
--------------------------

Valida si el usuario tiene agregado al menos un detalle a la piedra consultada de ser así lo redirige a la :ref:`url detalles_piedra_categorias_agregar` enviando como parámetro el id de la piedra.

Función EliminarDetalle
--------------------------

Elimina un detalle específico para la piedra consultada, para ello realiza una petición de tipo POST a la :ref:`url detalles_piedra_eliminar` enviando como parámetro el id del detalle a eliminar.

Template divisiones_form
==========================

Template de la pantalla que permite crear o editar una división para un taller determinado, realiza una petición de tipo POST a la :ref:`url divisiones_crear` en caso de creación de una división, y una petición de tipo POST a la :ref:`url divisiones_editar` en caso de modificar los datos de una división enviando como parámetro el id de la división a editar.

Template divisiones_lista
===========================

Template de la pantalla para consultar todas las divisiones que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_division_modal` y a la pantalla de creación o edición de divisiones :ref:`Template divisiones_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver divisiones. Para la consulta de las divisiones se realiza una petición de tipo GET a la :ref:`url divisiones_lista`.

Template items_form
==========================

Template de la pantalla que permite crear o editar un ítem para un taller determinado, realiza una petición de tipo POST a la :ref:`url items_crear` en caso de creación de un ítem, y una petición de tipo POST a la :ref:`url items_editar` en caso de modificar los datos de un ítem enviando como parámetro el id del ítem a editar.

Template piedra_agregar_modal
=========================================

Template del modal que aparecerá cuando el usuario desea agregar una piedra a la órden que está generando, en el modal se mostrarán las piedras que estén disponibles para la transacción. Para la consulta de las piedras realiza una petición de tipo GET a la :ref:`url piedras_modal_lista`.

Template piedras_form
==========================

Template de la pantalla que permite crear o editar una piedra para un taller determinado, realiza una petición de tipo POST a la :ref:`url piedras_crear` en caso de creación de una piedra, y una petición de tipo POST a la :ref:`url piedras_editar` en caso de modificar los datos de una piedra enviando como parámetro el id de la piedra a editar.

Template piedras_lista
===========================

Template de la pantalla para consultar todas las piedras que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_piedra_modal` y a la pantalla de creación o edición de piedras :ref:`Template piedras_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver piedras. Para la consulta de las piedras se realiza una petición de tipo GET a la :ref:`url piedras_lista`.

Template productos_lista
===========================

Template de la pantalla para consultar los ítems de tipo producto con precio fijo y producto con precio gramo que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template activar_item_modal` o :ref:`Template inactivar_item_modal` para activar o inactivar el ítem y a la pantalla de creación o edición de ítems :ref:`Template items_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver ítems. Para la consulta de los ítems se realiza una petición de tipo GET a la :ref:`url productos_lista`.

Template servicios_lista
===========================

Template de la pantalla para consultar los ítems de tipo servicio con precio fijo y servicio con precio gramo que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template activar_item_modal` o :ref:`Template inactivar_item_modal` para activar o inactivar el ítem y a la pantalla de creación o edición de ítems :ref:`Template items_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver ítems. Para la consulta de los ítems se realiza una petición de tipo GET a la :ref:`url servicios_lista`.

Template tallas_form
==========================

Template de la pantalla que permite crear o editar una talla para un taller determinado, realiza una petición de tipo POST a la :ref:`url tallas_crear` en caso de creación de una talla, y una petición de tipo POST a la :ref:`url tallas_editar` en caso de modificar los datos de una talla enviando como parámetro el id de la talla a editar.

Template tallas_lista
===========================

Template de la pantalla para consultar todas las tallas que pertenezcan al mismo taller. Desde esta pantalla se puede acceder al modal :ref:`Template actualizar_talla_modal` y a la pantalla de creación o edición de piedras :ref:`Template tallas_form`, esta pantalla es solo para los usuarios de tipo taller y que posean el permiso para ver tallas. Para la consulta de las tallas se realiza una petición de tipo GET a la :ref:`url tallas_lista`.