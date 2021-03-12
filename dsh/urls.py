from django.urls import path
from .views import DashboardAdminOpeView, DashboardAdminOpeAPIView,\
     DashboardAdminTalView, DashboardAdminTalAPIView, ReporteTiendasEstadisticasExcel,\
     ReporteUsuariosEstadisticasExcel, gramos_fabricados, gramos_fabricados_servicios,\
     cargar_fabricaciones, CiudadOrdenes, ciudades_ordenes, ZonasOrdenes,\
     zonas_ordenes

urlpatterns = [
     path('adminop/',
          DashboardAdminOpeView.as_view(),
          name='dashboard_operaciones'
          ),
     path('adminta/',
          DashboardAdminTalView.as_view(),
          name='dashboard_taller'
          ),
     path('adminop/api/<int:opcion>',
          DashboardAdminOpeAPIView.as_view(),
          name='dashboard_usuario_api'
          ),
     path('adminop/api/<int:opcion>/<str:f_inicio>/<str:f_fin>',
          DashboardAdminOpeAPIView.as_view(),
          name='dashboard_usuario_api'
          ),
     path('adminta/api/<int:opcion>',
          DashboardAdminTalAPIView.as_view(),
          name='dashboard_taller_api'
          ),
     path('adminta/api/<int:opcion>/<str:f_inicio>/<str:f_fin>',
          DashboardAdminTalAPIView.as_view(),
          name='dashboard_taller_api'
          ),
     path('adminta/api/<int:opcion>/<str:f_inicio>/<str:f_fin>',
          DashboardAdminTalAPIView.as_view(),
          name='dashboard_taller_api'
          ),
     path('reporte/excel/listatiendas/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteTiendasEstadisticasExcel.as_view(),
          name='rep_lista_tiendas_excel'
          ),
     # reporte ususarios conectados
     path('reporte/excel/usuarios/<str:f_inicio>/<str:f_fin>/<int:opcion>',
          ReporteUsuariosEstadisticasExcel.as_view(),
          name='reporte_usuarios'
          ),
     path('estadistica/grafica/gramos-fabricados/ajax/',
          gramos_fabricados,
          name="grafica_gramos"
          ),
     path('estadistica/grafica/gramos-fabricados-servicios/ajax/',
          gramos_fabricados_servicios,
          name="grafica_gramos_servicios"
          ),
     path('estadistica/grafica/items-fabricaciones/ajax/',
          cargar_fabricaciones,
          name="cargar_fabricaciones"
          ),
     path('estadistica/grafica/ciudad_modal/ajax/',
          CiudadOrdenes.as_view(),
          name="ciudad_modal"
          ),
     path('estadistica/grafica/ciudades_ordenes/ajax/',
          ciudades_ordenes,
          name="ciudades_ordenes"
          ),
     path('estadistica/grafica/zonas_modal/ajax/',
          ZonasOrdenes.as_view(),
          name="zona_modal"
          ),
     path('estadistica/grafica/zonas_ordenes/ajax/',
          zonas_ordenes,
          name="zonas_ordenes"
          ),
     
     
]
