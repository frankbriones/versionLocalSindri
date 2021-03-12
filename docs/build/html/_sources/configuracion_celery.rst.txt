****************************
**Configuración de Celery**
****************************

Dentro de la carpeta principal del proyecto llamada **sindri** tenemos el archivo de configuración llamado ``celery.py``. Este archivo contiene la configuración necesaria para el funcionamiento de Celery_ dentro del proyecto

.. _Celery: https://docs.celeryproject.org/en/latest/index.html

.. code-block:: py

    # Setear variable de entorno
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sindri.settings")

    app = Celery('sindri',
                broker='amqp://celery_user:celery@localhost:5672/celery_host',
                )

    app.config_from_object("django.conf:settings", namespace='CELERY')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

En este archivo se configura una variable de entorno para la ejecución de Celery, luego se crea un objeto en este caso llamado **app** con la configuración correspondiente: El nombre de la aplicación y el broker con el cual se va a trabajar, en este caso es RabbitMQ_.

Por último se configura un namespace para el objeto creado **app** y con ``autodiscover_tasks`` la aplicación buscará de forma automática las nuevas tareas registradas.

.. _RabbitMQ: https://www.rabbitmq.com/documentation.html
