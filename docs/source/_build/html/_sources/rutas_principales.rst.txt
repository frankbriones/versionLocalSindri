*********************************
**Rutas principales del sistema**
*********************************

Dentro de la carpeta principal del proyecto llamada **sindri** tenemos el archivo de configuración llamado ``urls.py``. Donde se encuentran las rutas principales del proyecto correspondientes a las distintas aplicaciones existentes

La configuración de las rutas es la siguiente:

.. code-block:: py

    urlpatterns = [
        path('', include(('bases.urls', 'bases'), namespace='bases')),
        path('usuarios/', include(('usr.urls', 'usr'),
            namespace='usr')),
        path('usuarios/', include('django.contrib.auth.urls')),
        path('ubicaciones/', include(('ubc.urls', 'ubc'),
            namespace='ubc')),
        path('proveedores/', include(('prv.urls', 'prv'),
            namespace='prv')),
        path('configuraciones/', include(('cfg.urls', 'cfg'),
            namespace='cfg')),
        path('catalogo/', include(('ctg.urls', 'ctg'),
            namespace='ctg')),
        path('clientes/', include(('clt.urls', 'clt'),
            namespace='clt')),
        path('transacciones/', include(('trn.urls', 'trn'),
            namespace='trn')),
        path('websocket/', include(('wso.urls', 'wso'),
            namespace='wso')),
        path('notificaciones/', include(('ntf.urls', 'ntf'),
            namespace='ntf')),
        path('dashboard/', include(('dsh.urls', 'dsh'),
            namespace='dsh')),

        path('admin/', admin.site.urls),
        path('rosetta/', include('rosetta.urls')),
        path('i18n/', include('django.conf.urls.i18n')),
    ]

Cada ruta incluye su namespace debido a que las aplicaciones poseen sub-rutas dentro de las mismas. También están presentes las rutas hacia el sitio administrador proporcionado por Django, el cual se genera de forma automática con el proyecto, además de las rutas para las traducciones de idiomas del sistema.

Para el uso de archivos media en la etapa de dasarrollo **Modo DEBUG activo** es necesaria la siguiente configuración:

.. code-block:: py

    # Archivos media en modo DEBUG
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
