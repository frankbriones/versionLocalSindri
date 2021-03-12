**********************
**Ruta de WebSockets**
**********************

Dentro de la carpeta principal del proyecto llamada **sindri** tenemos el archivo de configuración llamado ``routing.py``. Aquí se declara el router para el uso de websockets quedando de la siguiente forma:

.. code-block:: py

    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                wso.routing.websocket_urlpatterns
            )
        ),
    })
