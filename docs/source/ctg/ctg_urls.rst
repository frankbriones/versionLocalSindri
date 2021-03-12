***************
**URLs ctg**
***************

Dentro de la carpeta **ctg** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación ctg, se detalla a continuación cada ruta

url divisiones_lista
=====================

``/divisiones/lista`` Ruta hacia la pantalla del listado de divisiones registradas para un taller determinado, hace un llamado a la :ref:`Vista DivisionesListaView`.

url divisiones_crear
=====================

``/divisiones/crear`` Ruta hacia la pantalla que permite crear una división para un taller determinado, hace un llamado a la :ref:`Vista DivisionesCrearView`.

url divisiones_editar
======================

``/divisiones/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una división para un taller determinado, hace un llamado a la :ref:`Vista DivisionesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la división a editar ``id_division``."

url divisiones_actualizar
==========================

``/divisiones/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una división para un taller determinado, hace un llamado a la :ref:`Vista ActualizarDivisionModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la división a editar ``id_division``."

url divisiones_buscar_api
===========================

``/divisiones/buscar/<int:taller>/<int:tipo>`` Ruta utilizada para la consulta de las divisiones registrados para un taller determinado, hace un llamado a la :ref:`Vista BusquedaDivisionesApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"taller","De tipo entero, se refiere al id del taller al que pertenecen las divisiones."
	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen las divisiones."

url categorias_lista
=====================

``/categorias/lista`` Ruta hacia la pantalla del listado de categorías registradas para un taller determinado, hace un llamado a la :ref:`Vista CategoriasListaView`.

url categorias_crear
=====================

``/categorias/crear`` Ruta hacia la pantalla que permite crear una categoría para un taller determinado, hace un llamado a la :ref:`Vista CategoriasCrearView`.

url categorias_editar
======================

``/categorias/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una categoría para un taller determinado, hace un llamado a la :ref:`Vista CategoriasEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la categoría a editar ``id_categoria``."

url categorias_actualizar
==========================

``/categorias/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una categoría para un taller determinado, hace un llamado a la :ref:`Vista ActualizarCategoriaModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la categoría a editar ``id_categoria``."

url categorias_buscar_api
===========================

``/categorias/buscar/<int:division>/<int:tipo>`` Ruta utilizada para la consulta de las categorías registradas para una división determinada, hace un llamado a la :ref:`Vista BusquedaCategoriasApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"division","De tipo entero, se refiere al id de la división a la que pertenecen las categorías."
	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen las categorías."

url tallas_lista
=====================

``/tallas/lista`` Ruta hacia la pantalla del listado de tallas registradas para un taller determinado, hace un llamado a la :ref:`Vista TallasListaView`.

url tallas_crear
=====================

``/tallas/crear`` Ruta hacia la pantalla que permite crear una talla para un taller determinado, hace un llamado a la :ref:`Vista TallasCrearView`.

url tallas_editar
======================

``/tallas/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una talla para un taller determinado, hace un llamado a la :ref:`Vista TallasEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la talla a editar ``id_talla``."

url tallas_actualizar
==========================

``/tallas/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una talla para un taller determinado, hace un llamado a la :ref:`Vista ActualizarTallaModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la talla a editar ``id_talla``."

url colores_lista
=====================

``/colores/lista`` Ruta hacia la pantalla del listado de colores registrados para un taller determinado, hace un llamado a la :ref:`Vista ColoresListaView`.

url colores_crear
=====================

``/colores/crear`` Ruta hacia la pantalla que permite crear un color para un taller determinado, hace un llamado a la :ref:`Vista ColoresCrearView`.

url colores_editar
======================

``/colores/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un color para un taller determinado, hace un llamado a la :ref:`Vista ColoresEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del color a editar ``id_color``."

url colores_actualizar
==========================

``/colores/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un color para un taller determinado, hace un llamado a la :ref:`Vista ActualizarColorModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del color a editar ``id_color``."

url adicionales_lista
======================

``/adicionales/lista`` Ruta hacia la pantalla del listado de adicionales registrados para un taller determinado, hace un llamado a la :ref:`Vista AdicionalesListaView`.

url adicionales_crear
======================

``/adicionales/crear`` Ruta hacia la pantalla que permite crear un adicional para un taller determinado, hace un llamado a la :ref:`Vista AdicionalesCrearView`.

url detalles_adicional_crear
=============================

``/adicionales/detalles/crear/<int:pk>`` Ruta hacia la pantalla que permite crear un detalle para un adicional determinado, hace un llamado a la :ref:`Vista DetalleAdicionalCrearView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del adicional al que pertenece el detalle ``id_adicional``."

url adicionales_editar
=======================

``/adicionales/editar/<int:pk>`` Ruta hacia la pantalla que permite editar un adicional para un taller determinado, hace un llamado a la :ref:`Vista AdicionalesEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del adicional a editar ``id_adicional``."

url adicionales_actualizar
===========================

``/adicionales/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un adicional para un taller determinado, hace un llamado a la :ref:`Vista ActualizarAdicionalModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del adicional a editar ``id_adicional``."

url adicionales_modal_lista
============================

``/adicionales/modal/lista/<int:pk>`` Ruta que abre el modal que contiene los adicionales pertenecientes a un taller determinado, hace un llamado a la :ref:`Vista AdicionalesModalListaView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del taller al que pertenecen los adicionales ``id_taller``."

url adicional_detalle_modal
============================

``/adicionales/detalle/modal/<int:id_adicional>`` Ruta que abre el modal que contiene la información de un adicional en específico, hace un llamado a la :ref:`Vista adicionalDetalleView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_adicional","De tipo entero, se refiere al id del adicional que se consulta ``id_adicional``."

url piedras_lista
======================

``/piedras/lista`` Ruta hacia la pantalla del listado de piedras registradas para un taller determinado, hace un llamado a la :ref:`Vista PiedrasListaView`.

url piedras_crear
======================

``/piedras/crear`` Ruta hacia la pantalla que permite crear una piedra para un taller determinado, hace un llamado a la :ref:`Vista PiedrasCrearView`.

url detalles_piedra_crear
=============================

``/piedras/detalles/crear/<int:pk>`` Ruta hacia la pantalla que permite crear un detalle para una piedra determinada, hace un llamado a la :ref:`Vista DetallePiedraCrearView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la piedra al que pertenece el detalle ``id_piedra``."

url piedras_editar
=======================

``/piedras/editar/<int:pk>`` Ruta hacia la pantalla que permite editar una piedra para un taller determinado, hace un llamado a la :ref:`Vista PiedrasEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la piedra a editar ``id_piedra``."

url detalles_piedra_agregar
=============================

``/piedras/detalles/agregar/<int:pk>`` Ruta hacia la pantalla desde donde se pueden crear detalles para una piedra determinada, hace un llamado a la :ref:`Vista DetallePiedraAgregarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la piedra a la que se le agregan los detalles ``id_piedra``."

url detalles_piedra_categorias_agregar
=======================================

``/piedras/detalles/categorias/<int:pk>`` Ruta hacia la pantalla desde donde se registran las categorías en que está disponible una piedra determinada, hace un llamado a la :ref:`Vista DetallePiedraCategoriasView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la piedra ``id_piedra``."

url detalles_piedra_editar
=======================================

``/piedras/detalles/editar/<int:pk>`` Ruta hacia la pantalla desde donde se edita la información de un detalle perteneciente a una piedra determinada, hace un llamado a la :ref:`Vista DetallePiedraEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del detalle a editar."

url detalles_piedra_actualizar
===============================

``/piedras/detalles/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un detalle de una piedra determinada, hace un llamado a la :ref:`Vista ActualizarDetallePiedraModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del detalle a editar."

url piedra_detalle_modal
============================

``/piedras/detalle/modal/<int:id_piedra>`` Ruta que abre el modal que contiene la información de una piedra en específico, hace un llamado a la :ref:`Vista PiedraDetalleView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_piedra","De tipo entero, se refiere al id de la piedra que se consulta ``id_piedra``."

url detalles_piedra_eliminar
=============================

``/piedras/detalles/eliminar/<int:id_detalle>`` Ruta que permite eliminar un detalle de una piedra en específico, hace un llamado a la :ref:`Vista DetallePiedraEliminarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_detalle","De tipo entero, se refiere al id del detalle a eliminar."

url piedras_modal_lista
============================

``/piedras/modal/lista/<int:pk>`` Ruta que abre el modal que contiene las piedras pertenecientes a un taller determinado, hace un llamado a la :ref:`Vista PiedrasModalListaView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del taller al que pertenecen las piedras ``id_taller``."

url piedras_actualizar
===============================

``/piedras/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar una piedra determinada, hace un llamado a la :ref:`Vista ActualizarPiedraModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id de la piedra a editar."

url productos_lista
======================

``/productos/lista`` Ruta hacia la pantalla del listado de ítems de tipo producto con precio fijo y producto con precio gramo registradas para un taller determinado, hace un llamado a la :ref:`Vista ProductosListaView`.

url servicios_lista
======================

``/servicios/lista`` Ruta hacia la pantalla del listado de ítems de tipo producto con precio fijo y producto con precio gramo registradas para un taller determinado, hace un llamado a la :ref:`Vista ProductosListaView`.

url detalles_crear
=============================

``/detalles/crear/<int:pk>`` Ruta hacia la pantalla que permite crear un detalle para un ítem determinado, hace un llamado a la :ref:`Vista DetalleCrearView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del ítem al que pertenece el detalle ``id_item``."

url items_crear
======================

``/items/crear/<int:tipo>`` Ruta hacia la pantalla que permite crear un ítem para un taller determinado, hace un llamado a la :ref:`Vista ItemsCrearView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"tipo","De tipo entero, se refiere al tipo de catálogo al que pertenece el ítem."

url items_editar
=======================

``/items/editar/<int:pk>/<int:tipo>`` Ruta hacia la pantalla que permite editar un ítem para un taller determinado, hace un llamado a la :ref:`Vista ItemsEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del ítem a editar ``id_item``."
	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenece el ítem."

url item_inactivar_modal
===============================

``/items/inactivar/modal/<int:id_item>`` Ruta que abre el modal para inactivar un ítem determinado, hace un llamado a la :ref:`Vista InactivarItemModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_item","De tipo entero, se refiere al id del ítem a editar."

url item_activar_modal
===============================

``/items/activar/modal/<int:id_item>`` Ruta que abre el modal para activar un ítem determinado, hace un llamado a la :ref:`Vista ActivarItemModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_item","De tipo entero, se refiere al id del ítem a editar."

url detalles_agregar
=============================

``/detalles/agregar/<int:pk>`` Ruta hacia la pantalla desde donde se pueden crear detalles para un ítem determinado, hace un llamado a la :ref:`Vista DetalleAgregarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del ítem al que se le agregan los detalles ``id_item``."

url detalles_colores_agregar
=======================================

``/detalles/colores/agregar/<int:pk>`` Ruta hacia la pantalla desde donde se registran los colores en que está disponible un ítem determinado, hace un llamado a la :ref:`Vista DetalleColoresAgregarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del ítem ``id_item``."

url items_detalle
============================

``/items/detalle/<int:id_item>`` Ruta que abre el modal que contiene la información de un ítem en específico, hace un llamado a la :ref:`Vista ItemDetalleView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_item","De tipo entero, se refiere al id del ítem que se consulta ``id_item``."

url items_detalle_editar
=======================================

``/items/detalle/editar/<int:pk>`` Ruta hacia la pantalla desde donde se edita la información de un detalle perteneciente a un ítem determinado, hace un llamado a la :ref:`Vista DetalleEditarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del detalle a editar."

url items_detalle_actualizar
===============================

``/items/detalle/actualizar/<int:pk>`` Ruta que abre el modal para activar o inactivar un detalle de un ítem determinado, hace un llamado a la :ref:`Vista ActualizarDetalleItemModal`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"pk","De tipo entero, se refiere al id del detalle a editar."

url items_detalle_eliminar
=============================

``/items/detalle/eliminar/<int:id_detalle>`` Ruta que permite eliminar un detalle de un ítem en específico, hace un llamado a la :ref:`Vista DetalleEliminarView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_detalle","De tipo entero, se refiere al id del detalle a eliminar."

url contar_cotizacion
=============================

``/items/cotizar/<int:id_item>/<int:tipo>`` Ruta que permite registrar una cotización para un ítem en específico, hace un llamado a la :ref:`Vista ContarCotizacion`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_item","De tipo entero, se refiere al id del ítem que se cotiza."
	"tipo", "De tipo entero, se refiere al tipo de cotización que se realiza."

url buscar_items_api
===========================

``/items/buscar/<str:clave>/<int:tipo>`` Ruta utilizada para la consulta de un ítem en específico, hace un llamado a la :ref:`Vista BusquedaItemsApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"clave","De tipo string, se refiere al texto de búsqueda ingresada por el usuario."
	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenece el ítem."

url items_todos_api
===========================

``/items/todos/<int:tipo>`` Ruta utilizada para la consulta de todos los ítems pertenecientes a un tipo de catálogo en específico, hace un llamado a la :ref:`Vista ItemsTodosApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen los ítems."

url items_taller_api
===========================

``/items/taller/<int:taller>/<int:tipo>`` Ruta utilizada para la consulta de todos los ítems pertenecientes a un tipo de catálogo en específico y a un taller determinado, hace un llamado a la :ref:`Vista ItemsPorTallerApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen los ítems."
	"taller", "De tipo entero, se refiere al id del taller al que pertenecen los ítems."

url items_division_api
===========================

``/items/division/<int:division>/<int:tipo>`` Ruta utilizada para la consulta de todos los ítems pertenecientes a un tipo de catálogo en específico y a una división determinada, hace un llamado a la :ref:`Vista ItemsPorDivisionApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen los ítems."
	"division", "De tipo entero, se refiere al id de la división a la que pertenecen los ítems."

url items_categoria_api
===========================

``/items/categoria/<int:categoria>/<int:tipo>`` Ruta utilizada para la consulta de todos los ítems pertenecientes a un tipo de catálogo en específico y a una categoría determinada, hace un llamado a la :ref:`Vista ItemsPorCategoriaApiView`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"tipo", "De tipo entero, se refiere al tipo de catálogo al que pertenecen los ítems."
	"categoria", "De tipo entero, se refiere al id de la categoría a la que pertenecen los ítems."

url detalle_buscar
===========================

``/detalle/buscar/<int:item>/<int:medida>`` Ruta utilizada para la consulta de un detalle perteneciente a un ítem específico, hace un llamado a la :ref:`Vista BusquedaDetalle`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"medida", "De tipo entero, se refiere al id del detalle."
	"item", "De tipo entero, se refiere al id del ítem al que pertenece el detalle."

url detalle_piedra_buscar
===========================

``/detalle/piedra/buscar/<int:id_detalle>`` Ruta utilizada para la consulta de un detalle perteneciente a una piedra específica, hace un llamado a la :ref:`Vista BusquedaDetallePiedra`, recibe los siguientes parámetros:

.. csv-table::
	:header: "**Parámetro**","**Descripción**"
	:widths: 20, 80

	"id_detalle", "De tipo entero, se refiere al id del detalle."

url catalogo_gramos
=====================

``/catalogo/gramo`` Ruta hacia la pantalla del listado de ítem de tipo producto con precio gramo y servicio con precio gramo registrados para un taller determinado, hace un llamado a la :ref:`Vista GramoListaView`.

url catalogo_fijo
=====================

``/catalogo/fijo`` Ruta hacia la pantalla del listado de ítem de tipo producto con precio fijo y servicio con precio fijo registrados para un taller determinado, hace un llamado a la :ref:`Vista FijoListaView`.
