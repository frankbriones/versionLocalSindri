*******************
**Tasks cfg**
*******************

Dentro de la carpeta **cfg** tenemos el archivo llamado ``tasks.py``. Donde se encuentran las tareas asíncronas de la aplicación cfg, se detalla a continuación cada tarea.

Formulario CrearTareaEnvioReporte
==================================

Vista basada en funciones, utiliza el decorador ``@shared_task`` de Celery para ser identificada como una tarea compartida, realiza el proceso de creación de una tarea periódica que enviará un reporte al usuario que recibe como parámetro.
