from django.urls import path

from .views import SolicitudesListaView, SolicitudesCrearView,\
     TipoSolicitudView, SolicitudesEditarView, SolicitudDetalleView,\
     OrdenesListaView, TipoOrdenView, CrearOrdenSolicitudView,\
     CrearOrdenItemView, OrdenDetalleView, EnvioMaterialView, \
     RecibirMaterialView, AnularOrdenView, FinalizarTrabajoView, \
     EnviarProductoView, DevolverProductoView, FinalizarOrdenView, \
     EnviarCorreoView, SolicitarAExternoView, AgregarAdicionalView, \
     OrdenesListaAPIView, AgregarPiedraView, \
     SolicitudesListaAPIView, CorreoTemplateView, \
     ComprobanteTemplateView, OrdenesListaFechaAPIView, \
     ReporteOrdenesListaView, \
     GenerarOrdenSolicitudView, SolicitudesListaFechaAPIView, \
     FinalizarSinVentaView, OrdenesPagosListaView, \
     OrdenesPagosListaAPIView, AprobacionPagoModalView, \
     ReporteOrdenesPagos, ReporteOrdenesAdminOpView, \
     RecibirProductoView, CargarDocumentosTaller, \
     CargarDocumentosOperaciones, ReporteOrdenesListaExcel, \
     AprobarPagoOrden, PagarOrden, DetalleOrdenApi, \
     AprobarRevisionOrden, CrearFactura, ObtenerFacturasCreadas, \
     FacturasListaView, ObtenerFacturas, FacturasDetalles, \
     FacturasActualizar, EliminarFactura, BorrarDetalleFactura, \
     validarFactura, ReporteUsuarios, CrearOrdenAlianzaView, ReporteSolicitudListaExcel, \
     tooltip, editar_detalle_tooltip, eliminarTool

urlpatterns = [
     path('solicitudes/lista',
          SolicitudesListaView.as_view(),
          name='solicitudes_lista'
          ),
     path('solicitudes/lista/api',
          SolicitudesListaAPIView.as_view(),
          name='solicitudes_api_lista'
          ),
     path('solicitudes/list/fecha/api/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          SolicitudesListaFechaAPIView.as_view(),
          name='solicitudes_api_lista_fecha'
          ),
     path('solicitudes/crear/<int:tipo>/<int:id_item>',
          # SolicitudesCrearView.as_view(),
          SolicitudesCrearView,
          name='solicitudes_crear'
          ),
     path('solicitudes/tipo/<int:id_item>',
          TipoSolicitudView.as_view(),
          name='solicitudes_tipo'
          ),
     path('solicitudes/editar/<int:pk>',
          SolicitudesEditarView.as_view(),
          name='solicitudes_editar'
          ),
     path('solicitudes/detalle',
          SolicitudDetalleView,
          name='solicitudes_detalle'
          ),
     path('solicitudes/detalle/modal/<int:id_solicitud>/<int:accion>',
          SolicitudDetalleView,
          name='solicitudes_detalle'
          ),
     path('solicitudes/solicitarexterno/<int:pk>',
          SolicitarAExternoView.as_view(),
          name='solicitar_externo'
          ),
     path('solicitudes/generarordensolicitud/<int:pk>',
          GenerarOrdenSolicitudView.as_view(),
          name='generar_orden_solicitud'
          ),
     path('ordenes/lista',
          OrdenesListaView.as_view(),
          name='ordenes_lista'
          ),
     path('ordenes/lista/api/<int:limite>',
          OrdenesListaAPIView.as_view(),
          name='ordenes_api_lista'
          ),
     path('ordenes/lista/fecha/api/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          OrdenesListaFechaAPIView.as_view(),
          name='ordenes_api_lista_fecha'
          ),
     path('ordenes/pagos/lista',
          OrdenesPagosListaView.as_view(),
          name='ordenes_pagos_lista'
          ),
     path('ordenes/lista/pagos/api',
          OrdenesPagosListaAPIView.as_view(),
          name='ordenes_pagos_api_lista'
          ),
     path('ordenes/tipo',
          TipoOrdenView.as_view(),
          name='ordenes_tipo'
          ),
     path('ordenes/solicitudcrear/<int:id_trn>/<str:identificacion>',
          CrearOrdenSolicitudView,
          name='ordenes_solicitud_crear'
          ),
     path('ordenes/itemcrear/<int:id_item>/<str:identificacion>',
          CrearOrdenItemView,
          name='ordenes_item_crear'
          ),
     path('ordenes/detalles/modal/<int:id_orden>',
          OrdenDetalleView,
          name='ordenes_detalle'
          ),
     path('ordenes/piedras/agregar/<int:id_orden>/<int:id_piedra>',
          AgregarPiedraView,
          name='ordenes_agregar_piedra'
          ),
     path('ordenes/adicionales/agregar/<int:id_orden>/<int:id_adicional>',
          AgregarAdicionalView,
          name='ordenes_agregar_adicional'
          ),
     path('ordenes/enviomaterial/<int:pk>',
          EnvioMaterialView.as_view(),
          name='envio_material'
          ),
     path('ordenes/recibematerial/<int:pk>',
          RecibirMaterialView.as_view(),
          name='recibe_material'
          ),
     path('ordenes/anularorden/<int:pk>',
          AnularOrdenView.as_view(),
          name='anular_orden'
          ),
     path('ordenes/finalizartrabajo/<int:pk>',
          FinalizarTrabajoView.as_view(),
          name='finalizar_trabajo'
          ),
     path('ordenes/enviarproducto/<int:pk>',
          EnviarProductoView.as_view(),
          name='enviar_producto'
          ),
     path('ordenes/recibirproducto/<int:pk>',
          RecibirProductoView.as_view(),
          name='recibir_producto'
          ),
     path('ordenes/cargardoctaller/<int:pk>',
          CargarDocumentosTaller.as_view(),
          name='cargar_doc_taller'
          ),
     path('ordenes/cargardocope/<int:pk>',
          CargarDocumentosOperaciones.as_view(),
          name='cargar_doc_ope'
          ),
     path('ordenes/devolverproducto/<int:pk>',
          DevolverProductoView.as_view(),
          name='devolver_producto'
          ),
     path('ordenes/finalizarorden/<int:pk>',
          FinalizarOrdenView.as_view(),
          name='finalizar_orden'
          ),
     path('ordenes/finalizarsinventa/<int:pk>',
          FinalizarSinVentaView.as_view(),
          name='finalizar_sin_venta'
          ),
     path('ordenes/aprobacion/pago/modal/<int:id_orden>',
          OrdenDetalleView,
          kwargs=dict(template_name="trn/aprobacion_pago_modal.html"),
          name='orden_aprobacion_pago'
          ),
     path('ordenes/aprobar/pago/<int:id_orden>',
          AprobarPagoOrden.as_view(),
          name='aprobar_pago_orden'
          ),
     path('ordenes/revision/pago/<int:id_orden>',
          AprobarRevisionOrden.as_view(),
          name='revision_pago_orden'
          ),
     path('ordenes/registrar/pago/<int:id_orden>',
          PagarOrden.as_view(),
          name='registrar_pago_orden'
          ),
     path('ordenes/enviarcorreocliente',
          EnviarCorreoView.as_view(),
          name='correo_cliente'
          ),
     path('correo/correocliente/<int:id_orden>',
          CorreoTemplateView,
          name='correo_cliente_tmp'
          ),
     path('comprobante/<int:id_orden>',
          ComprobanteTemplateView,
          name='comprobante_tmp'
          ),
     path('reporte/ordenes/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteOrdenesListaView,
          name='rep_ordenes'
          ),
     path('reporte/ordenes/adminop/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteOrdenesAdminOpView,
          name='rep_ordenes_admin_op'
          ),
     path('reporte/aprobacion/pagos',
          ReporteOrdenesPagos.as_view(),
          # ReporteOrdenesPagos,
          name='rep_pagos_aprobados'
          ),
     # reporte de conexion ususarios
     path('reporte/conexion/usuarios',
          ReporteUsuarios.as_view(),
          name='rep_conexion_usuario'
          ),
     path('reporte/excel/listaordenes/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteOrdenesListaExcel,
          name='rep_lista_ordenes_excel'
          ),
     
     path('orden/detalle/api/<int:id_orden>',
          DetalleOrdenApi.as_view(),
          name='orden_detalle_api'
          ),
     path('facturas/crear',
          CrearFactura.as_view(),
          name='facturas_crear'
          ),
     path('facturas/obtener/creadas/<int:id_taller>',
          ObtenerFacturasCreadas.as_view(),
          name='facturas_obtener_creadas'
          ),
     path('facturas/lista',
          FacturasListaView.as_view(),
          name='facturas_lista'
          ),
     path('facturas/obtener/<int:id_taller>',
          ObtenerFacturas.as_view(),
          name='facturas_obtener'
          ),
     path('facturas/detalles/<int:id_factura>',
          FacturasDetalles.as_view(),
          name='facturas_detalles'
          ),
     path('facturas/actualizar/<int:id_factura>',
          FacturasActualizar.as_view(),
          name='facturas_actualizar'
          ),
     path('facturas/detalle/eliminar',
          BorrarDetalleFactura.as_view(),
          name='facturas_detalle_eliminar'
     ),

     path('facturas/eliminar',
          EliminarFactura.as_view(),
          name='facturas_eliminar'
          ),
     path('configuracion/notas-de-ayuda/<int:grupo_id>',
          tooltip,
          name="tooltip"
          ),
     #ajax
     path('facturas/validarfactura/ajax/', validarFactura, name="validar_factura"),
     path('ordenes/alianzas/crear/<int:id_item>/<str:identificacion>',
          CrearOrdenAlianzaView,
          name='ordenes_alianzas_crear'
          ),

     path('reporte/excel/listasolicitudes/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteSolicitudListaExcel,
          name='rep_lista_solicitud_excel'
          ),
     path('notas-de-ayuda/editar-detalle/ajax/',
          editar_detalle_tooltip,
          name='editar_detalle_tooltip'
          ),
     path('notas-de-ayuda/ajax/eliminar/',
          eliminarTool,
          name="validar_factura"
          ),

     
]
