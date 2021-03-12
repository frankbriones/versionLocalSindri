from django.urls import path

from .views import CategoriasListaView, CategoriasCrearView,\
     CategoriasEditarView, ColoresListaView, ColoresCrearView, \
     ColoresEditarView, AdicionalesListaView, AdicionalesCrearView, \
     AdicionalesEditarView, ItemsListaView, ItemsCrearView,\
     DetalleCrearView, DetalleAgregarView, ServiciosListaView, \
     ItemDetalleView, BusquedaDetalle, CatalogoItemsView, FijoListaView,\
     TallasListaView, TallasCrearView, TallasEditarView, PiedrasListaView, \
     PiedrasCrearView, DetallePiedraCrearView, DetallePiedraAgregarView, \
     DetalleAdicionalCrearView, PiedrasModalListaView, BusquedaDetallePiedra,\
     DetalleColoresAgregarView, ItemsEditarView,\
     InactivarItemModal, ActivarItemModal, ActualizarCategoriaModal,\
     ActualizarTallaModal, ActualizarColorModal, PiedrasEditarView, \
     DetallePiedraEliminarView, DetallePiedraCategoriasView, \
     ActualizarPiedraModal, ActualizarAdicionalModal, \
     AdicionalesModalListaView, ContarCotizacion, DetalleEditarView, \
     ActualizarDetalleItemModal, DetallePiedraEditarView, \
     ActualizarDetallePiedraModal, BusquedaItemsApiView, \
     BusquedaCategoriasApiView, ItemsPorTallerApiView, \
     ItemsPorCategoriaApiView, ItemsTodosApiView, adicionalDetalleView, \
     PiedraDetalleView, DivisionesListaView, DivisionesCrearView, \
     DivisionesEditarView, ActualizarDivisionModal, BusquedaDivisionesApiView,\
     ItemsPorDivisionApiView, BusquedaItemsTallerApiView, \
     PreciosDefinidosListaView, PreciosCrearView, PreciosEditarView, \
     ActualizarPrecioModal, ItemsListaServiciosApiView, ProductosOpeListaView,\
     ItemsOpeListaProductosApiView, ServiciosOpeListaView,\
     ItemsOpeListaServiciosApiView, ActualizarPrecioOpeView, \
     CategoriasTalleresApiView, ObtenerCostoColorProveedor, PiedrasFormView, \
     eliminar_precio, eliminar_division, eliminar_categoria, eliminar_talla, \
     eliminar_color, eliminar_piedra, AdicionalesFormView, AdicionalSolicitudCrear, \
     AcabadosListaView, AcabadosCrearView, AcabadosEditarView, \
     ActualizarAcabadoModal, PartesInternasListaView, PartesInternasCrearView,\
     PartesInternasEditarView, ActualizarParteInternaModal, AnchurasListaView,\
     AnchurasCrearView, AnchurasEditarView, ActualizarAnchurasModal, \
     AlianzasCrearView, PiedrasAgregarModalListaView, PiedraAgregarAItemView, \
     PiedrasListaApi, DetallePiedraApi, AlianzasListaView, \
     BusquedaAlianzasApiView, BusquedaAnchuras, BusquedaPesos, \
     BusquedaPiedras, AlianzasEditarView, obtener_piedras, obtener_acabados,\
     eliminar_alianzas, eliminar_item, detalles_editados, eliminar_detalle_item,\
     eliminar_detalle_alianza, eliminar_piedra_detalle, eliminar_un_detalle



urlpatterns = [
     path('precios/lista',
          PreciosDefinidosListaView.as_view(),
          name='precios_definidos_lista'
          ),
     path('precios/crear',
          PreciosCrearView.as_view(),
          name='precios_definidos_crear'
          ),
     path('precios/editar/<int:pk>',
          PreciosEditarView.as_view(),
          name='precios_definidos_editar'
          ),
     path('precios/actualizar/<int:pk>',
          ActualizarPrecioModal,
          name='precios_definidos_actualizar'
          ),
     path('divisiones/lista',
          DivisionesListaView.as_view(),
          name='divisiones_lista'
          ),
     path('divisiones/crear',
          DivisionesCrearView.as_view(),
          name='divisiones_crear'
          ),
     path('divisiones/editar/<int:pk>',
          DivisionesEditarView.as_view(),
          name='divisiones_editar'
          ),
     path('divisiones/actualizar/<int:pk>',
          ActualizarDivisionModal,
          name='divisiones_actualizar'
          ),
     path('divisiones/buscar/<int:taller>/<int:tipo>',
          BusquedaDivisionesApiView.as_view(),
          name='divisiones_buscar_api'
          ),
     path('categorias/lista',
          CategoriasListaView.as_view(),
          name='categorias_lista'
          ),
     path('categorias/crear',
          CategoriasCrearView.as_view(),
          name='categorias_crear'
          ),
     path('categorias/editar/<int:pk>',
          CategoriasEditarView.as_view(),
          name='categorias_editar'
          ),
     path('categorias/actualizar/<int:pk>',
          ActualizarCategoriaModal,
          name='categorias_actualizar'
          ),
     path('categorias/buscar/<int:division>/<int:tipo>',
          BusquedaCategoriasApiView.as_view(),
          name='categorias_buscar_api'
          ),
     path('tallas/lista',
          TallasListaView.as_view(),
          name='tallas_lista'
          ),
     path('tallas/crear',
          TallasCrearView.as_view(),
          name='tallas_crear'
          ),
     path('tallas/editar/<int:pk>',
          TallasEditarView.as_view(),
          name='tallas_editar'
          ),
     path('tallas/actualizar/<int:pk>',
          ActualizarTallaModal,
          name='tallas_actualizar'
          ),
     path('colores/lista',
          ColoresListaView.as_view(),
          name='colores_lista'
          ),
     path('colores/crear',
          ColoresCrearView.as_view(),
          name='colores_crear'
          ),
     path('colores/editar/<int:pk>',
          ColoresEditarView.as_view(),
          name='colores_editar'
          ),
     path('colores/actualizar/<int:pk>',
          ActualizarColorModal,
          name='colores_actualizar'
          ),
     path('adicionales/lista',
          AdicionalesListaView.as_view(),
          name='adicionales_lista'
          ),
     path('adicionales/crear',
          AdicionalesCrearView.as_view(),
          name='adicionales_crear'
          ),
     # adicionales creados en solicitudes
     path('adicionales/solicitud/crear',
          AdicionalSolicitudCrear,
          name='adicional_crear'
          ),

     path('adicionales/detalles/crear/<int:pk>',
          DetalleAdicionalCrearView,
          name='detalles_adicional_crear'
          ),
     path('adicionales/editar/<int:pk>',
          AdicionalesEditarView.as_view(),
          name='adicionales_editar'
          ),
     path('adicionales/actualizar/<int:pk>',
          ActualizarAdicionalModal,
          name='adicionales_actualizar'
          ),
     path('adicionales/modal/lista/<int:pk>',
          AdicionalesModalListaView.as_view(),
          name='adicionales_modal_lista'
          ),
     path('adicionales/detalle/modal/<int:id_adicional>',
          adicionalDetalleView,
          name='adicional_detalle_modal'
          ),
     path('piedras/lista',
          PiedrasListaView.as_view(),
          name='piedras_lista'
          ),
     path('piedras/crear',
          # PiedrasCrearView.as_view(),
          PiedrasFormView,
          name='piedras_crear'
          ),
     path('piedras/crear/modal',
          PiedrasFormView,
          kwargs=dict(template_name="ctg/piedras_form_modal.html"),
          name='piedra_crear_modal'
          ),
     path('adicionales/crear/modal',
          AdicionalesFormView,
          kwargs=dict(template_name="ctg/adicionales_form_modal.html"),
          name='adicional_modal'
          ),
     path('piedras/editar/<int:pk>',
          # PiedrasEditarView.as_view(),
          PiedrasFormView,
          name='piedras_editar'
          ),
     path('piedras/detalles/crear/<int:pk>',
          DetallePiedraCrearView,
          name='detalles_piedra_crear'
          ),
     path('piedras/detalles/agregar/<int:pk>',
          DetallePiedraAgregarView,
          name='detalles_piedra_agregar'
          ),
     path('piedras/detalles/categorias/<int:pk>',
          DetallePiedraCategoriasView,
          name='detalles_piedra_categorias_agregar'
          ),
     path('piedras/detalles/editar/<int:pk>',
          DetallePiedraEditarView.as_view(),
          name='detalles_piedra_editar'
          ),
     path('piedras/detalles/actualizar/<int:pk>',
          ActualizarDetallePiedraModal,
          name='detalles_piedra_actualizar'
          ),
     path('piedras/detalle/modal/<int:id_piedra>',
          PiedraDetalleView,
          name='piedra_detalle_modal'
          ),
     path('piedras/detalles/eliminar/<int:id_detalle>',
          DetallePiedraEliminarView,
          name='detalles_piedra_eliminar'
          ),
     path('piedras/modal/lista/<int:pk>',
          PiedrasModalListaView.as_view(),
          name='piedras_modal_lista'
          ),
     path('piedras/actualizar/<int:pk>',
          ActualizarPiedraModal,
          name='piedras_actualizar'
          ),
     path('items/lista/<int:tipo>',
          ItemsListaView.as_view(),
          name='items_lista'
          ),
     path('items/lista/api/',
          BusquedaItemsTallerApiView.as_view(),
          name='items_lista_api'
          ),
     path('servicios/lista',
          ServiciosListaView.as_view(),
          name='servicios_lista'
          ),
     path('servicios/lista/api/<int:tipo>/<int:limite>',
          ItemsListaServiciosApiView.as_view(),
          name='servicios_lista_api'
          ),
     path('productosop/lista',
          ProductosOpeListaView.as_view(),
          name='productos_ope_lista'
          ),
     path('productosop/lista/api/<int:tipo>/<int:limite>',
          ItemsOpeListaProductosApiView.as_view(),
          name='productos_ope_lista_api'
          ),
     path('serviciosop/lista',
          ServiciosOpeListaView.as_view(),
          name='servicios_ope_lista'
          ),
     path('serviciosop/lista/api/<int:tipo>/<int:limite>',
          ItemsOpeListaServiciosApiView.as_view(),
          name='servicios_ope_lista_api'
          ),
     path('detalles/crear/<int:pk>',
          DetalleCrearView,
          name='detalles_crear'
          ),
     path('items/crear/<int:tipo>',
          # ItemsCrearView.as_view(),
          ItemsCrearView,
          name='items_crear'
          ),
     path('items/detalles/editados/<int:pk>',
          # ItemsCrearView.as_view(),
          detalles_editados,
          name='detalles_editados'
          ),
     path('items/editar/<int:pk>',
          ItemsEditarView.as_view(),
          name='items_editar'
          ),
     path('items/inactivar/modal/<int:id_item>',
          InactivarItemModal,
          name='item_inactivar_modal'
          ),
     path('items/activar/modal/<int:id_item>',
          ActivarItemModal,
          name='item_activar_modal'
          ),
     path('detalles/agregar/<int:pk>',
          DetalleAgregarView,
          name='detalles_agregar'
          ),
     path('detalles/colores/agregar/<int:pk>',
          DetalleColoresAgregarView,
          name='detalles_colores_agregar'
          ),
     path('items/detalle/<int:id_item>',
          ItemDetalleView,
          name='items_detalle'
          ),
     path('items/detalle/editar/<int:pk>',
          DetalleEditarView.as_view(),
          name='items_detalle_editar'
          ),
     path('items/detalle/actualizar/<int:pk>',
          ActualizarDetalleItemModal,
          name='items_detalle_actualizar'
          ),
     path('items/actualizar/precioope/<int:id_item>',
          ActualizarPrecioOpeView,
          name='items_actualizar_precio_ope'
          ),
     path('items/cotizar/<int:id_item>/<int:tipo>',
          ContarCotizacion,
          name='contar_cotizacion'
          ),
     path('items/buscar/',
          BusquedaItemsApiView.as_view(),
          name='buscar_items_api'
          ),
     path('items/todos/<int:tipo>',
          ItemsTodosApiView.as_view(),
          name='items_todos_api'
          ),
     path('items/taller/<int:taller>/<int:tipo>',
          ItemsPorTallerApiView.as_view(),
          name='items_taller_api'
          ),
     path('items/division/<int:division>/<int:tipo>',
          ItemsPorDivisionApiView.as_view(),
          name='items_division_api'
          ),
     path('items/categoria/<int:categoria>/<int:tipo>',
          ItemsPorCategoriaApiView.as_view(),
          name='items_categoria_api'
          ),
     path('detalle/buscar/<int:item>/<int:medida>',
          BusquedaDetalle.as_view(),
          name='detalle_buscar'
          ),
     path('detalle/piedra/buscar/<int:id_detalle>',
          BusquedaDetallePiedra.as_view(),
          name='detalle_piedra_buscar'
          ),
     path('catalogo/items/<int:tipo>',
          CatalogoItemsView.as_view(),
          name='catalogo_items'
          ),
     path('catalogo/fijo',
          FijoListaView,
          name='catalogo_fijo'
          ),
     path('catalogo/categorias/',
          CategoriasTalleresApiView.as_view(),
          name='categorias_taller_api'
          ),
     path('color/costo/proveedor/<int:id_color>/<int:id_proveedor>',
          ObtenerCostoColorProveedor.as_view(),
          name='obtener_costo_proveedor'
          ),
     #ajax
     path('precios/ajax/eliminar/',
          eliminar_precio,
          name="eliminar_precio"
          ),
     path('divisiones/ajax/eliminar/',
          eliminar_division,
          name="eliminar_division"
          ),
     path('categorias/ajax/eliminar/',
          eliminar_categoria,
          name="eliminar_categoria"
          ),
     path('tallas/ajax/eliminar/',
          eliminar_talla,
          name="eliminar_talla"
          ),
     path('colores/ajax/eliminar/',
          eliminar_color,
          name="eliminar_color"
          ),
     path('piedras/ajax/eliminar/',
          eliminar_piedra,
          name="eliminar_piedra"
          ),
     path('obtener/colores_item/ajax/',
          obtener_piedras,
          name="obtener_piedras"
          ),
     path('obtener/acabados_item/ajax/',
          obtener_acabados,
          name="obtener_acabados"
          ),
     path('detalle_items/eliminar/ajax/',
          eliminar_detalle_item,
          name="eliminar_detalle_item"
          ),
     path('detalle_alianza/eliminar/ajax/',
          eliminar_detalle_alianza,
          name="eliminar_detalle_alianza"
          ),
     path('detalle-piedra-alianza/eliminar/ajax/',
          eliminar_piedra_detalle,
          name="eliminar_piedra_detalle"
          ),
     path('detalle-alianza/eliminar/ajax/',
          eliminar_un_detalle,
          name="eliminar_un_detalle"
          ),
     
     
     # alianzas
     path('acabados/lista/',
          AcabadosListaView.as_view(),
          name='acabados_lista'
          ),
     path('acabados/crear',
          AcabadosCrearView.as_view(),
          name='acabados_crear'
          ),
     path('acabados/editar/<int:pk>',
          AcabadosEditarView.as_view(),
          name='acabados_editar'
          ),
     path('acabados/actualizar/<int:pk>',
          ActualizarAcabadoModal,
          name='acabados_actualizar'
          ),
     path('partes-internas/lista/',
          PartesInternasListaView.as_view(),
          name='partes_internas_lista'
          ),
     path('partes-internas/crear',
          PartesInternasCrearView.as_view(),
          name='partes_internas_crear'
          ),
     path('partes-internas/editar/<int:pk>',
          PartesInternasEditarView.as_view(),
          name='partes_internas_editar'
          ),
     path('partes-internas/actualizar/<int:pk>',
          ActualizarParteInternaModal,
          name='partes_internas_actualizar'
          ),
     path('anchuras/lista/',
          AnchurasListaView.as_view(),
          name='anchuras_lista'
          ),
     path('anchuras/crear',
          AnchurasCrearView.as_view(),
          name='anchuras_crear'
          ),
     path('anchuras/editar/<int:pk>',
          AnchurasEditarView.as_view(),
          name='anchuras_editar'
          ),
     path('anchuras/actualizar/<int:pk>',
          ActualizarAnchurasModal,
          name='anchuras_actualizar'
          ),
     path('alianzas/crear',
          AlianzasCrearView,
          name='alianzas_crear'
          ),
     path('alianzas/editar/<int:id_item>',
          AlianzasEditarView,
          name='alianzas_editar'
          ),
     path('piedras/agregar/lista/modal',
          PiedrasAgregarModalListaView.as_view(),
          name='piedras_agregar_lista'
          ),
     path('piedras/agregar/item/modal/<int:id_piedra>',
          PiedraAgregarAItemView,
          name='piedras_agregar_a_item'
          ),
     path('piedras/agregar/lista',
          PiedrasListaApi.as_view(),
          name='piedras_lista_api'
          ),
     path('piedra/detalle/api/<int:id_piedra>',
          DetallePiedraApi.as_view(),
          name='piedra_detalle_api'
          ),
     path('alianzas/lista',
          AlianzasListaView.as_view(),
          name='alianzas_lista'
          ),
     path('alianzas/lista/catalogo',
          AlianzasListaView.as_view(
               template_name='ctg/alianzas_lista_op.html',
          ),
          name='alianzas_lista_op'
          ),
     path('alianzas/lista/api/',
          BusquedaAlianzasApiView.as_view(),
          name='alianzas_lista_api'
          ),
     path('alianzas/bucar/anchuras',
          BusquedaAnchuras.as_view(),
          name='alianzas_buscar_anchuras'
          ),
     path('alianzas/bucar/pesos',
          BusquedaPesos.as_view(),
          name='alianzas_buscar_pesos'
          ),
     path('alianzas/bucar/piedras',
          BusquedaPiedras.as_view(),
          name='alianzas_buscar_piedras'
          ),
     path('alianzas/ajax/aliminar/',
          eliminar_alianzas,
          name='eliminar_alianzas'),
     path('items/ajax/aliminar/',
          eliminar_item,
          name='eliminar_item'),

]
