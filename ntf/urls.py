from django.urls import path

from .views import ObtenerNotificacionesUsuarioView, \
     ActualizarNotificacionView, ObtenerNotificacionesTallerView,\
     PrimeraNotificacionesUsuarioView, PrimeraNotificacionesTallerView


urlpatterns = [
     path('usuario/lista/<int:id_usuario>/<int:limite>/',
          ObtenerNotificacionesUsuarioView.as_view(),
          name='notificaciones_usuario_lista'
          ),
     path('taller/lista/<int:id_taller>/<int:limite>',
          ObtenerNotificacionesTallerView.as_view(),
          name='notificaciones_taller_lista'
          ),
     path('usuario/primera/<int:id_usuario>',
          PrimeraNotificacionesUsuarioView.as_view(),
          name='notificaciones_usuario_primera'
          ),
     path('taller/primera/<int:id_taller>',
          PrimeraNotificacionesTallerView.as_view(),
          name='notificaciones_taller_primera'
          ),
     path('actualizar/<int:pk>',
          ActualizarNotificacionView.as_view(),
          name='notificacion_actualizar'
          ),
]
