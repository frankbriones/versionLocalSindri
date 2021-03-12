****************
**Tareas usr**
****************

Dentro de la carpeta **usr** tenemos el archivo llamado ``tasks.py``. Donde se encuentran las tareas en segundo plano de la aplicación usr

Tarea enviarCorreoContrasena
=============================

Tarea que se encarga que enviar un correo electrónico al usuario con la contraseña que se le ha asignado una vez creado el usuario o reestablecida la contraseña del mismo, esta tarea recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "id","Id del usuario a quien se envía el correo."
		"contrasena","Contraseña generada para el usuario."
