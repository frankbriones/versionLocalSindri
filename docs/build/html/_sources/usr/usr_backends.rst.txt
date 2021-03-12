***********************
**Backends usr**
***********************

Dentro de la carpeta **usr** tenemos el archivo llamado ``backends.py``. Donde se encuentran los métodos de autenticación de usuarios para la aplicación usr.

Backend EmailBackend
======================

Método de autenticación de usuarios que hereda de ``backends.ModelBackend`` de Dajngo, y que se utiliza para modificar el modo de autenticación que trae Django por defecto, con este método el usuario se puede autenticar usando tanto su username como su email, este método no es sensible a mayúsculas o minúsculas para el username o email, verifica si la contraseña es correcta y luego permite al usuario ingresar al sistema. Recibe los siguientes parámetros:

.. csv-table::
	:header: "**Campo**","**Descripción**"
	:widths: 20, 80
        
        "username","Username o email del usuario."
        "password", "Contraseña del usuario."
