******************************
**Configuración del sistema**
******************************

Dentro de la carpeta principal del proyecto llamada **sindri** tenemos el archivo de configuración llamado ``settings.py``. Donde es necesario realizar ciertas configuraciones necesarias para el correcto funcionamiento del sistema. A continuación se muestran las configuraciones generales del proyecto:

Apps instaladas
---------------

Las aplicaciones instaladas dentro del proyecto además de las que instala Django por defecto son las siguientes:

**Aplicaciones externas:**

Channels_ 
 Utilizada para la comunicación en tiempo real mediante sockets,
 permite la actualización instantanea de la información mostrada
 en el sistema.

Rosetta_ 
 Utilizada para la internacionalización, nos brinda una interfaz
 gráfica para realizar la traducción a los diferentes idiomas
 configurados en el sistema.

Rest_framework_ 
 Framework utilizado para la construcción de APIs

Django_celery_beat_ 
 Utilizada para la creación de tareas periódicas o programadas
 en el sistema

.. _Channels: https://channels.readthedocs.io/en/latest/
.. _Rosetta: https://django-rosetta.readthedocs.io/
.. _Rest_framework: https://www.django-rest-framework.org/
.. _Django_celery_beat: https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

**Aplicaciones propias del sistema:**

usr.apps.UsrConfig
 Aplicacion para el manejo de usuarios del sistema,
 aqui están contenidas las vistas para la creación, edición, consulta, activación e inactivación para: usuarios y roles de usuario
 
bases
 Contiene templates, clases y modelos utilizadas
 en común dentro del sistema

ubc
 Aplicacion para el manejo de ubicaciones, aqui están
 contenidas las vistas para la creación, edición, consulta,
 activación e inactivación para: países, localidades, ciudades,
 zonas y sectores

prv
 Aplicacion para el manejo de proveedores, aqui están
 contenidas las vistas para la creación, edición, consulta,
 activación e inactivación para: proveedores

cfg
 Aplicacion para el manejo de configuraciones de usuario,
 aqui están contenidas las vistas para la edición de las
 diferentes configuraciones que pueden realizar los usuarios
 para definir el comportamiento que tendrá el sistema

ctg
 Aplicacion para el manejo del catálogo, aqui están contenidas
 las vistas para la creación, edición, consulta, activación e
 inactivación para: divisiones, categorías, tallas, colores,
 ítems, piedras y adicionales

clt
 Aplicacion para el manejo de los clientes, aqui están contenidas
 las vistas para la creación, edición, consulta, activación e
 inactivación para: clientes

trn
 Aplicacion para el manejo de las transacciones, aqui están
 contenidas las vistas para la creación, edición, consulta para:
 solicitudes y órdenes de trabajo así como también la aprobación
 de pagos de las mismas

wso
 Aplicacion que contiene la configuración del server para el uso
 de websockets, con los métodos para conectar, desconectar, enviar
 y recibir mensajes

ntf
 Aplicacion para el manejo de las notificaciones, contiene las
 vistas y los métodos para la generación y modificación automática
 de notificaciones para los usuarios del sistema

dsh
 Aplicacion para el manejo de las estadísticas, aqui están
 contenidas las vistas para las consultas de las estadísticas
 predefinidas en el sistema

La configuración queda de la siguiente forma:

.. code-block:: py


    INSTALLED_APPS = [
        'channels',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'usr.apps.UsrConfig',  # usuarios
        'bases',  # paginas principales
        'ubc',  # ubicaciones
        'prv',  # proveedores
        'cfg',  # configuraciones
        'ctg',  # catálogo
        'clt',  # clientes
        'trn',  # transacciones
        'rosetta',  # traduccion idiomas
        'rest_framework',  # apirest
        'wso',  # websockets
        'ntf',  # notificaciones
        'dsh',  # dashboard
        'django_celery_beat',  # tareas periódicas
    ]

Django Channels
---------------

La configuración necesaria para el funcionamiento de Channels es la siguiente:

.. code-block:: py


    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_rabbitmq.core.RabbitmqChannelLayer",
            "CONFIG": {
                "host": "amqp://guest:guest@127.0.0.1",
                # "ssl_context": ... (optional)
            },
        },
    }

Como broker de mensajes se utilizó RabbitMQ y se configura un host virtual desde el administrador, para más detalles sobre RabbitMQ, su configuración y uso puede revisar la documentación oficial aquí_

.. _aquí: https://www.rabbitmq.com/documentation.html

Base de datos
-------------

Para el proyecto se utilizó el gestor de bases de datos MySQL_, la configuración para el acceso a la base se la realiza en el siguiente bloque:

.. code-block:: py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sindridesarrollo',
            'USER': 'root',
            'PASSWORD': 'Innovacion2019',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

.. _MySQL: https://dev.mysql.com/doc/

Internacionalización
--------------------

La configuración realizada para la traducción a los diferentes idiomas y dialectos en el sistema es la siguiente:

.. code-block:: py

    # Lenguaje por defecto
    LANGUAGE_CODE = 'es-ec'

    # Lenguajes del sistema
    LANGUAGES = (
        ('es-ec', gettext('Español Ecuador')),
        ('es-co', gettext('Español Colombia')),
        ('es-cl', gettext('Español Chile')),
        ('es-pe', gettext('Español Perú')),
        ('en-us', gettext('English USA')),
        ('pt-br', gettext('Português Brasil'))
    )

    # Carpeta de lenguajes
    LOCALE_PATHS = (
        os.path.join(BASE_DIR, "locale"),
    )

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

Archivos estáticos y archivos media
-----------------------------------

Para la ubicación de los archivos estáticos y media se utiliza la siguiente configuración donde se establece la ruta hacia los archivos

.. code-block:: py

    # Archivos estáticos
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

    # Archivos media
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

En la ruta de archivos estáticos se guardan los archivos correspondientes a CSS, JavaScript e imágenes propias del sistema. Mientras que en los archivos media se guardan aquellos archivos que son cargados por los usuarios como imágenes de perfil, imágenes de catálogos, archivos de comprobantes, etc.

Autenticación de usuarios
-------------------------

Para la autenticación de los usuarios en el sistema se realizan las siguientes configuraciones:

.. code-block:: py

    # modelo de usuarios
    AUTH_USER_MODEL = 'usr.Usuarios'

    # Backend de autenticación de usuario
    AUTHENTICATION_BACKENDS = (
        'usr.backends.EmailBackend',
    )

Es necesaria esta configuración debido a que se modificó el modelo de usuario que provee Django por defecto, de la misma forma no se utiliza el backend de autenticación que provee Django por defecto, en su lugar se utiliza un backend personalizado el cual permite que el usuario se pueda autenticar usando su email registrado o su username

Servidor de correos
-------------------

Para el envío automático de correos electrónicos desde el sistema es necesaria la siguiente configuración

.. code-block:: py

    # Configuracion servidor de correos
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = '587'
    EMAIL_HOST_USER = 'correo@gmail.com'
    EMAIL_HOST_PASSWORD = 'Pass123'
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = False


