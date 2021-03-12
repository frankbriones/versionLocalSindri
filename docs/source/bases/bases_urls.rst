***************
**URLs Bases**
***************

Dentro de la carpeta **bases** tenemos el archivo llamado ``urls.py``. Donde se encuentran las rutas de la aplicación bases, se detalla a continuación cada ruta

url home
========

``/`` Ruta a la página principal del sistema, hace un llamado a la :ref:`Vista Home`.

url login
=========

``/login/`` Ruta hacia la pantalla del autenticación del sistema, hace un llamado a la :ref:`Vista user_login`.

url logout
==========

``/logout/`` Ruta para el cierre de sesión de un usuario, hace uso de una vista propia de Django ``auth_views.LogoutView``.

url logout_modal
================

``/logoutmodal/`` Ruta hacia el modal de cierre de sesión, hace un llamado a la :ref:`Vista Logout`.

url sin_permisos
================

``/sin_permisos/`` Ruta hacia la pantalla Sin permisos, hace un llamado a la :ref:`Vista SinPermisosTemplate`.

url error404
============

``/error404/`` Ruta hacia la pantalla error 404, hace un llamado a la :ref:`Vista error404Template`.
