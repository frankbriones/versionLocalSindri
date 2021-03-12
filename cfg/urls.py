from django.urls import path

from .views import CfgEmpresaEditarView, CfgTalEditarView, \
     CfgOperacionesTaller,\
     CfgOperacionesProveedor, CfgTiempoVenta, CfgPermitirExterno, \
     CfgPaisEditarView, CalculadoraPorcentajesView, EnvioReportesView, \
     RubrosListaView, RubrosFormView, ActualizarRubroModal, CfgApiMensajes,\
     PrioridadTalleresView, eliminar_rubro, EnvioReporteUsuario, ObservacionesListaView,\
     ObservacionesCrearView, ObservacionesEditarView, eliminar_observacion,\
     EditarPoliticasComerciales, ActualizarMotivoRechazo


urlpatterns = [
     path('configuracion/pais/<int:pk>',
          CfgPaisEditarView.as_view(),
          name='cfg_pais_editar'
          ),
     path('configuracion/empresa/<int:pk>',
          CfgEmpresaEditarView.as_view(),
          name='cfg_ope_editar'
          ),
     path('configuracion/porcentajes/modal/<int:pk>',
          CalculadoraPorcentajesView,
          name='calcular_porcentajes'
          ),
     path('configuracion/taller/<int:pk>',
          CfgTalEditarView.as_view(),
          name='cfg_tal_editar'
          ),
     path('configuracion/ope-taller/',
          CfgOperacionesTaller,
          name='cfg_ope_tal'
          ),
     path('configuracion/ope-proveedor/',
          CfgOperacionesProveedor,
          name='cfg_ope_prv'
          ),
     path('configuracion/tiempo-venta/',
          CfgTiempoVenta,
          name='cfg_tmp_vta'
          ),
     path('configuracion/aut-externo/',
          CfgPermitirExterno,
          name='cfg_aut_ext'
          ),
     path('configuracion/rubros/lista/',
          RubrosListaView.as_view(),
          name='cfg_rubros_lista'
          ),
     path('configuracion/rubros/form/<int:pk>',
          RubrosFormView,
          name='cfg_rubros_form'
          ),
     path('configuracion/rubros/actualizar/<int:pk>',
          ActualizarRubroModal,
          name='cfg_rubros_actualizar'
          ),
     path('reportes/envio/<int:id_usuario>',
          EnvioReportesView,
          name='cfg_envio_reportes'
          ),
     path('reportes/usuarios/conectados/',
          EnvioReporteUsuario,
          name='cfg_reporte_usuarios'
          ),
     path('api/mensajes/<int:pk>',
          CfgApiMensajes,
          name='api_mensajes_actualizar'
          ),
     path('talleres/prioridad/',
          PrioridadTalleresView,
          name='prioridad_talleres'
          ),
     path('configuracion/rubros/ajax/eliminar/', eliminar_rubro, name="eliminar_rubro"),
     # path('configuracion/obervaciones-rechazo/form/', crear_observacion, name="crear_observacion")

     path('observacion/lista',
          ObservacionesListaView.as_view(),
          name='obs_lista'
          ),
     path('observacion/crear',
          ObservacionesCrearView.as_view(),
          name='obs_crear'
          ),
     path('observacion/editar/<int:pk>',
          ObservacionesEditarView.as_view(),
          name='obs_editar'
          ),
     path('observacion/ajax/eliminar/',
          eliminar_observacion,
          name="eliminar_obs"
          ),
     path('politicas/editar/<int:id_empresa>',
          EditarPoliticasComerciales,
          name='editar_politicas'
     ),
     path('motivo-rechazo/actualizar/<int:pk>',
          ActualizarMotivoRechazo,
          name='rechazo_actualizar'
          ),

]
