****************
**Tareas dsh**
****************

Dentro de la carpeta **dsh** tenemos otra carpeta llamada **templates**. Donde se encuentran los templates de la aplicación dsh, se describe cada uno a continuación.

Template dashboard_operaciones
=====================================

Template de la pantalla donde se muestra el panel de estadísticas para el administrador de operaciones con la información de todas las joyerías pertenecientes al país del administrador, las funciones que posee este template son las siguientes:

Función cargarDatos
----------------------------

Realiza una petición de tipo GET a la :ref:`url dashboard_usuario_api` enviando como parámetros la fecha inicio y fin de la consulta y el tipo de consulta que se realiza, obtiene los datos de las órdenes de trabajo dentro del periodo de tiempo dado.

Función cargarTotalesPorEstado
--------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las órdenes generadas clasificadas por estado.

Función cargarTotalesIntExt
--------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las órdenes generadas clasificadas por tipo insterna y externa.

Función cargarFabricacionesPorMes
-----------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las órdenes generadas clasificadas por mes de fabricación.

Función cargarGramosPorJoyeria
-----------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a los gramos fabricados clasificados por joyería.

Función cargarProductoMasCotizado
-----------------------------------

Genera el elemento HTML para mostrar el ítem más cotizado dentro de un periodo de tiempo.

Función cargarProductoMasFabricado
-----------------------------------

Genera el elemento HTML para mostrar el ítem con más fabricaciones dentro de un periodo de tiempo.

Función cargarDetallesProducto
-----------------------------------

Muestra un modal con la información detallada de un ítem.

Función cargarCategoriaColor
-----------------------------------

Genera el elemento HTML para mostrar el color y la categpría con más fabricaciones dentro de un periodo de tiempo.

Template dashboard_taller
=====================================

Template de la pantalla donde se muestra el panel de estadísticas para el administrador del taller con la información de todas las órdenes de trabajo asignadas a dicho taller, las funciones que posee este template son las siguientes:

Función cargarDatos
----------------------------

Realiza una petición de tipo GET a la :ref:`url dashboard_taller_api` enviando como parámetros la fecha inicio y fin de la consulta y el tipo de consulta que se realiza, obtiene los datos de las órdenes de trabajo dentro del periodo de tiempo dado.

Función cargarTotalesPorEstado
--------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las órdenes generadas clasificadas por estado.

Función cargarSolicitudesEstado
--------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las solicitudes generadas clasificadas por estado.

Función cargarFabricacionesPorMes
-----------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a las órdenes generadas clasificadas por mes de fabricación.

Función cargarGramosPorJoyeria
-----------------------------------

Genera el elemento HTML para mostrar las estadísticas correspondientes a los gramos fabricados clasificados por joyería.

Función cargarProductoMasCotizado
-----------------------------------

Genera el elemento HTML para mostrar el ítem más cotizado dentro de un periodo de tiempo.

Función cargarProductoMasFabricado
-----------------------------------

Genera el elemento HTML para mostrar el ítem con más fabricaciones dentro de un periodo de tiempo.

Función cargarDetallesProducto
-----------------------------------

Muestra un modal con la información detallada de un ítem.

Función cargarCategoriaColor
-----------------------------------

Genera el elemento HTML para mostrar el color y la categpría con más fabricaciones dentro de un periodo de tiempo.
