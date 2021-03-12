from django.urls import path

from .views import ClientesListaView, ClientesCrearView,\
     ClientesEditarView, BusquedaCliente, ClientesModalView,\
     ClientesListaAPIView, ClientesCrearModal, \
     ActualizarClienteModal, eliminar_cliente


urlpatterns = [
     path('clientes/lista',
          ClientesListaView.as_view(),
          name='clientes_lista'
          ),
     path('clientes/crear',
          ClientesCrearView.as_view(),
          name='clientes_crear'
          ),
     path('clientes/editar/<int:pk>',
          ClientesEditarView.as_view(),
          name='clientes_editar'
          ),
     path('clientes/actualizar/<int:pk>',
          ActualizarClienteModal,
          name='clientes_actualizar'
          ),
     path('clientes/buscar/',
          ClientesListaAPIView.as_view(),
          name='clientes_lista_api'
          ),
     path('clientes/buscar/<str:identificacion>',
          BusquedaCliente.as_view(),
          name='clientes_buscar'
          ),
     path('clientes/modal/<int:id_trn>/<int:tipo>',
          # ClientesModalView.as_view(),
          ClientesCrearModal,
          name='clientes_modal'
          ),
     path('clientes/ajax/eliminar/', eliminar_cliente, name='eliminar_cliente'),
]
