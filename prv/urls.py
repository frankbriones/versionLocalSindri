from django.urls import path

from .views import ProveedoresListaView, ProveedoresCrearView,\
    ProveedoresEditarView, ActualizarProveedorModal, eliminar_proveedor


urlpatterns = [
     path('proveedores/lista',
          ProveedoresListaView.as_view(),
          name='proveedores_lista'
          ),
     path('proveedores/crear',
          ProveedoresCrearView.as_view(),
          name='proveedores_crear'
          ),
     path('proveedores/editar/<int:pk>',
          ProveedoresEditarView.as_view(),
          name='proveedores_editar'
          ),
     path('proveedores/actualizar/<int:pk>',
          ActualizarProveedorModal,
          name='proveedores_actualizar'
          ),
     
     path('proveedores/ajax/eliminar/', eliminar_proveedor, name="eliminar_proveedor"),
     
]
