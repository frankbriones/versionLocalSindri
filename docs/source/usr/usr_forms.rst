*******************
**Forms usr**
*******************

Dentro de la carpeta **usr** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación usr, se detalla a continuación cada formulario.

Formulario TipoUsuarioForm
===========================

Hereda de los formularios de autenticación de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo TipoUsuarios`. Contiene los siguientes campos:

- descripcion

Formulario GrupoForm
===========================

Hereda de los formularios de autenticación de Django ``forms.ModelForm``, este formulario afecta al ``Modelo Group`` generado por Django de forma automática.

Formulario RolForm
===========================

Hereda de los formularios de autenticación de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Roles`. Contiene los siguientes campos:

- descripcion

- zonal

Formulario RolGrupoForm
============================

Hereda de ``MultiModelForm``, es la unión de dos formularios :ref:`Formulario GrupoForm` y :ref:`Formulario RolForm`. Es utilizado para el registro o edición de roles de usuario.

Formulario RegistroForm
========================

Hereda de los formularios de autenticación de Django ``UserCreationForm``, este formulario afecta al :ref:`Modelo Usuarios`. Contiene los siguientes campos:

- username
- first_name
- last_name
- email
- rol
- telefono
- direccion
- ciudad
- sector

- img_perfil

Formulario AsignarGrupoForm
============================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo UsuariosGrupos`. Es una instancia vacía para asignar un grupo a un usuario.

Formulario UsuarioGrupoForm
============================

Hereda de ``MultiModelForm``, es la unión de dos formularios :ref:`Formulario RegistroForm` y :ref:`Formulario AsignarGrupoForm`. Es utilizado para el registro de nuevos usuarios.

Formulario EditarForm
========================

Hereda de los formularios de autenticación de Django ``UserChangeForm``, este formulario afecta al :ref:`Modelo Usuarios`. Contiene los siguientes campos:

- username
- first_name
- last_name
- email
- rol
- telefono
- direccion
- ciudad
- sector

- img_perfil

Formulario EditarUsuarioForm
=============================

Hereda de ``MultiModelForm``, es la unión de dos formularios :ref:`Formulario EditarForm` y :ref:`Formulario AsignarGrupoForm`. Es utilizado para edutar la información de un usuario determinado.

Formulario EditarPerfilForm
============================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Usuarios`. Contiene los siguientes campos:

- username
- first_name
- last_name
- email
- telefono
- direccion
- ciudad

- img_perfil
