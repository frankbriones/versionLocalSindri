from django.urls import path

from .views import GruposEmpresarialesListaView, GrupoEmpresarialCrearView,\
     GrupoEmpresarialEditarView, ActualizarGrupoEmpresarialModal, \
     EliminarGrupoEmpresarialModal, SociedadesListaView, SociedadesCrearView,\
     SociedadesEditarView, ActualizarSociedadModal, EliminarSociedadModal, \
     TiendasListaView, TiendasCrearView, TiendasEditarView, \
     ActualizarTiendaModal, EliminarTiendaModal, TalleresListaView, \
     TalleresCrearView, TalleresEditarView, eliminar_tienda, obtener_tiendas, \
     eliminar_grupo, obtener_grupos, eliminar_taller


urlpatterns = [
     path('gruposempresariales/lista',
          GruposEmpresarialesListaView.as_view(),
          name='grupos_empresariales_lista'
          ),
     path('gruposempresariales/crear',
          GrupoEmpresarialCrearView.as_view(),
          name='grupos_empresariales_crear'
          ),
     path('gruposempresariales/editar/<int:pk>',
          GrupoEmpresarialEditarView.as_view(),
          name='grupos_empresariales_editar'
          ),
     path('gruposempresariales/actualizar/<int:pk>',
          ActualizarGrupoEmpresarialModal,
          name='grupos_empresariales_actualizar'
          ),
     path('gruposempresariales/eliminar/<int:pk>',
          EliminarGrupoEmpresarialModal,
          name='grupos_empresariales_eliminar'
          ),
     path('sociedades/lista',
          SociedadesListaView.as_view(),
          name='sociedades_lista'
          ),
     path('sociedades/crear',
          SociedadesCrearView.as_view(),
          name='sociedades_crear'
          ),
     path('sociedades/editar/<int:pk>',
          SociedadesEditarView.as_view(),
          name='sociedades_editar'
          ),
     path('sociedades/actualizar/<int:pk>',
          ActualizarSociedadModal,
          name='sociedades_actualizar'
          ),
     path('sociedades/eliminar/<int:pk>',
          EliminarSociedadModal,
          name='sociedades_eliminar'
          ),
     path('tiendas/lista',
          TiendasListaView.as_view(),
          name='tiendas_lista'
          ),
     path('tiendas/crear',
          TiendasCrearView.as_view(),
          name='tiendas_crear'
          ),
     path('tiendas/editar/<int:pk>',
          TiendasEditarView,
          name='tiendas_editar'
          ),
     path('talleres/lista',
          TalleresListaView.as_view(),
          name='talleres_lista'
          ),
     path('talleres/crear',
          TalleresCrearView.as_view(),
          name='talleres_crear'
          ),
     path('talleres/editar/<int:pk>',
          TalleresEditarView.as_view(),
          name='talleres_editar'
          ),
     path('tiendas/ajax/eliminartienda/', eliminar_tienda, name="eliminar_tienda"),
     path('tiendas/ajax/obtenertiendas/', obtener_tiendas, name="obtener_tiendas"),
     path('gruposempresariales/ajax/eliminargrupo/', eliminar_grupo, name="eliminar_grupo"),
     path('gruposempresariales/ajax/obtenergrupos/', obtener_grupos, name="obtener_grupos"),
     path('talleres/ajax/eliminar/', eliminar_taller, name="eliminar_taller"),


]
