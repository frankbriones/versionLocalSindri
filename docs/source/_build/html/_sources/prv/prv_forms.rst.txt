*******************
**Forms prv**
*******************

Dentro de la carpeta **prv** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación prv, se detalla a continuación cada formulario.

Formulario ProveedorForm
=========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Proveedores`. Contiene los siguientes campos:

- identificacion
- nombres
- apellidos
- ciudad
- zona
- direccion
- telefono
- correo
- porcentaje_merma

- escala_peso
