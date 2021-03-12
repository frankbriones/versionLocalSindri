*******************
**Forms cfg**
*******************

Dentro de la carpeta **cfg** tenemos el archivo llamado ``forms.py``. Donde se encuentran los formularios de la aplicación cfg, se detalla a continuación cada formulario.

Formulario CfgOpeForm
=======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al modelo :ref:`Modelo ConfigGeneral`. Contiene los siguientes campos:

- utilidad_sobre_taller
- limite_venta
- aut_externo
- descuento_max
- costo_gramo_base
- utilidad_sobre_base
- origen_material
- prct_impuestos
- anticipo_fabricacion
- envio_material
- comprobante_env
- envio_incluido
- factura_taller
- cta_por_pagar
- orden_compra
- precio_final_fijo
- gramo_final_catalogo

- gramo_final_especial

Formulario CfgTalForm
=======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al modelo :ref:`Modelo Taller`. Contiene los siguientes campos:

- valor_fraccion
- tmp_resp_sol
- escala_peso
- estandar_tallas
- costo_gramo_base
- utilidad_sobre_fabricacion
- utilidad_sobre_base
- utilidad_sobre_piedras
- utilidad_sobre_adicionales

- prct_impuestos

Formulario CfgPaisForm
=======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al modelo :ref:`Modelo Paises`. Contiene los siguientes campos:

- aut_externo
- zona_horaria
- decimales
- simbolo_moneda

- documentos_obligatorios

Formulario RubrosForm
=======================

Hereda de los formularios de Django ``forms.ModelForm``, este formulario afecta al modelo :ref:`Modelo RubrosAsociados`. Contiene los siguientes campos:

- descripcion
