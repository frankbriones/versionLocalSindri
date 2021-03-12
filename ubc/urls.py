from django.urls import path

from .views import RegionesListaView, PaisesListaView, LocalidadesListaView, \
     ZonasListaView, CiudadesListaView, SectoresListaView, RegionesCrearView, \
     RegionesEditarView, PaisesCrearView, PaisesEditarView, \
     LocalidadesCrearView, LocalidadesEditarView, ZonasCrearView, \
     ZonasEditarView, CiudadesCrearView, CiudadEditarView, SectoresCrearView, \
     SectoresEditarView, ActualizarLocalidadModal, ActualizarZonaModal,\
     ActualizarCiudadModal, ActualizarSectorModal, eliminar_localidad,\
     eliminar_zona, eliminar_ciudad, eliminar_sector


urlpatterns = [
     path('regiones/lista',
          RegionesListaView.as_view(),
          name='regiones_lista'
          ),
     path('regiones/crear',
          RegionesCrearView.as_view(),
          name='regiones_crear'
          ),
     path('regiones/editar/<int:pk>',
          RegionesEditarView.as_view(),
          name='regiones_editar'
          ),
     path('paises/lista',
          PaisesListaView.as_view(),
          name='paises_lista'
          ),
     path('paises/crear',
          PaisesCrearView.as_view(),
          name='paises_crear'
          ),
     path('paises/editar/<int:pk>',
          PaisesEditarView.as_view(),
          name='paises_editar'
          ),
     path('localidades/lista',
          LocalidadesListaView.as_view(),
          name='localidades_lista'
          ),
     path('localidades/crear',
          LocalidadesCrearView.as_view(),
          name='localidades_crear'
          ),
     path('localidades/editar/<int:pk>',
          LocalidadesEditarView.as_view(),
          name='localidades_editar'
          ),
     path('localidades/actualizar/<int:pk>',
          ActualizarLocalidadModal,
          name='localidades_actualizar'
          ),
     path('zonas/lista',
          ZonasListaView.as_view(),
          name='zonas_lista'
          ),
     path('zonas/crear',
          ZonasCrearView.as_view(),
          name='zonas_crear'
          ),
     path('zonas/editar/<int:pk>',
          ZonasEditarView.as_view(),
          name='zonas_editar'
          ),
     path('zonas/actualizar/<int:pk>',
          ActualizarZonaModal,
          name='zonas_actualizar'
          ),
     path('ciudades/lista',
          CiudadesListaView.as_view(),
          name='ciudades_lista'
          ),
     path('ciudades/crear',
          CiudadesCrearView.as_view(),
          name='ciudades_crear'
          ),
     path('ciudades/editar/<int:pk>',
          CiudadEditarView.as_view(),
          name='ciudades_editar'
          ),
     path('ciudades/actualizar/<int:pk>',
          ActualizarCiudadModal,
          name='ciudades_actualizar'
          ),
     path('sectores/lista',
          SectoresListaView.as_view(),
          name='sectores_lista'
          ),
     path('sectores/crear',
          SectoresCrearView.as_view(),
          name='sectores_crear'
          ),
     path('sectores/editar/<int:pk>',
          SectoresEditarView.as_view(),
          name='sectores_editar'
          ),
     path('sectores/actualizar/<int:pk>',
          ActualizarSectorModal,
          name='sectores_actualizar'
          ),
     #ajax
     path('localidades/ajax/eliminar/', eliminar_localidad, name="eliminar_localidad"),
     path('zonas/ajax/eliminar/', eliminar_zona, name="eliminar_zona"),
     path('ciudades/ajax/eliminar/', eliminar_ciudad, name="eliminar_ciudad"),
     path('sectores/ajax/eliminar/', eliminar_sector, name="eliminar_sector"),


]
