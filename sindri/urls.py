"""sindri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', include(('bases.urls', 'bases'), namespace='bases')),
     path('usuarios/', include(('usr.urls', 'usr'),
          namespace='usr')),
     path('usuarios/', include('django.contrib.auth.urls')),
     path('ubicaciones/', include(('ubc.urls', 'ubc'),
          namespace='ubc')),
     path('establecimientos/', include(('est.urls', 'est'),
          namespace='est')),
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

# Archivos media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
