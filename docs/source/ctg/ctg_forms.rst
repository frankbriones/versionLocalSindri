*******************
**Forms ctg**
*******************

Dentro de la carpeta **ctg** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación ctg, se detalla a continuación cada formulario.

Formulario DivisionForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Divisiones`. Contiene los siguientes campos:

- descripcion

- tipo_catalogo

Formulario CategoriaForm
==========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Categorias`. Contiene los siguientes campos:

- descripcion
- unidad_medida

- division

Formulario TallasForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Tallas`. Contiene los siguientes campos:

- talla
- estandar

- diametro

Formulario ColoresForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Colores`. Contiene los siguientes campos:

- descripcion

- costo_adicional

Formulario AdicionalesForm
===========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Adicionales`. Contiene los siguientes campos:

- descripcion
- costo
- sku
- imagen

- utilidad_sobre_adicionales

Formulario PiedrasForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Piedras`. Contiene los siguientes campos:

- imagen
- sku
- descripcion

- utilidad_sobre_piedras

Formulario DetallesPiedraForm
===============================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo DetallePiedras`. Contiene los siguientes campos:

- medida

- costo

Formulario ItemsForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo Items`. Contiene los siguientes campos:

- descripcion
- sku
- categoria
- imagen
- valor_fraccion
- escala_peso
- parte_interna
- acabado
- tiempo_entrega_min
- tiempo_entrega_max
- costo
- cantidad_piedras
- costo_piedras
- valor_gramo_dif

- peso_max_dif

Formulario DetallesForm
========================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al :ref:`Modelo DetalleItems`. Contiene los siguientes campos:

- peso_minimo
- peso_maximo
- cantidad_piedras

- costo_piedras