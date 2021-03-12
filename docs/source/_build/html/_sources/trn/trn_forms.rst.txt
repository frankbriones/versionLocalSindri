*******************
**Forms trn**
*******************

Dentro de la carpeta **trn** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación trn, se detalla a continuación cada formulario.

Formulario SolicitudesForm
===========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo SolicitudTrabajo`. Contiene los siguientes campos:

- taller
- proveedor
- imagen
- talla
- longitud
- detalle
- acabado
- parte_interna
- cantidad_piedras
- sku_relacionado
- color
- peso_min
- peso_max
- valor_gramo
- valor_error
- tiempo_ent_min
- tiempo_ent_max

- origen_material

Formulario DetalleSolicitudForm
================================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo DetalleSolicitud`. Contiene los siguientes campos:

- item

Formulario SolicitudDetalleForm
================================

Hereda de ``MultiModelForm``, es la unión de dos formularios :ref:`Formulario SolicitudesForm` y :ref:`Formulario DetalleSolicitudForm`. Es utilizado para el registro de solicitudes.

Formulario SolicitudEditarForm
===============================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo SolicitudTrabajo`. Contiene los siguientes campos:

- proveedor
- imagen
- talla
- longitud
- detalle
- acabado
- parte_interna
- cantidad_piedras
- sku_relacionado
- color
- peso_min
- peso_max
- valor_gramo
- valor_error
- tiempo_ent_min
- tiempo_ent_max

- origen_material

Formulario OrdenEnvioMaterialForm
==================================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo OrdenTrabajo`. Contiene los siguientes campos:

- comp_envio_ta

Formulario OrdenAnticipoForm
==================================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo OrdenTrabajo`. Contiene los siguientes campos:

- anticipo_fabricacion
