*******************
**Forms ubc**
*******************

Dentro de la carpeta **ubc** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación ubc, se detalla a continuación cada formulario.

Formulario RegionForm
======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Regiones`. Contiene los siguientes campos:

- nombre

Formulario PaisForm
====================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Paises`. Contiene los siguientes campos:

- nombre
- region
- iniciales
- bandera
- zona_horaria
- decimales

- simbolo_moneda

Formulario LocalidadForm
=========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Localidades`. Contiene los siguientes campos:

- nombre

- pais

Formulario ZonaForm
=========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Zonas`. Contiene los siguientes campos:

- nombre

- pais

Formulario CiudadForm
======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Ciudades`. Contiene los siguientes campos:

- nombre

- localidad

Formulario SectorForm
======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Sectores`. Contiene los siguientes campos:

- nombre

- zona