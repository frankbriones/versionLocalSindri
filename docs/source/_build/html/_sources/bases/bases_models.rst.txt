*******************
**Modelos Bases**
*******************

Dentro de la carpeta **bases** tenemos el archivo llamado ``models.py``. Donde se encuentran los modelos de la aplicación bases

ClaseModelo
============

Modelo abstracto del cual heredarán varios modelos
posee campos de auditoría como son:

- fecha_creacion
- usuario_crea
- fecha_modificacion

- usuario_modifica

Estados
=======

Modelo para los estados de los diferentes elementos
del sistema, no incluye el estado Activo/Inactivo de
los usuarios
