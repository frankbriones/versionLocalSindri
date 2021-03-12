from django import forms

# from .models import ConfigGeneral
from est.models import GruposEmpresariales
# from usr.models import Taller
from ubc.models import Paises
from trn.models import RubrosAsociados
from est.models import Talleres


class CfgOpeForm(forms.ModelForm):

    class Meta:
        model = GruposEmpresariales
        fields = ['utilidad_sobre_taller',
                  'limite_venta',
                  'aut_externo',
                  'descuento_max',
                  'costo_gramo_base',
                  'precio_gramo_base',
                  'origen_material',
                  'prct_impuestos',
                  'anticipo_fabricacion',
                  'envio_material',
                  'comprobante_env',
                  'envio_incluido',
                  'factura_taller',
                  'cta_por_pagar',
                  'orden_compra',
                  'tipo_precio_predefinido',
                  'precio_gramo_final',
                  'logotipo',
                  'politicas_pdf',
                  'politicas_doc',
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class CfgTalForm(forms.ModelForm):

    class Meta:
        model = Talleres
        fields = ['costo_gramo_fabricacion',
                  'precio_gramo_fabricacion',
                  'tmp_resp_sol',
                  'escala_peso',
                  'estandar_tallas',
                  'costo_gramo_base',
                  'precio_gramo_base',
                  'utilidad_sobre_fabricacion',
                #   'utilidad_sobre_piedras',
                #   'utilidad_sobre_adicionales',
                  'prct_impuestos',
                  'secuencia_ordenes',
                  'secuencia_solicitudes',
                  'logotipo',
                  'recalcular_precio',
                  'cargar_img_fin_trabajo',
                  'tipo_precio_predefinido'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


# class CfgMermaForm(forms.ModelForm):

#     class Meta:
#         model = Taller
#         fields = ['porcentaje_merma',
#                   'nombre'
#                   ]

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })


class CfgPaisForm(forms.ModelForm):

    class Meta:
        model = Paises
        fields = [
            'aut_externo',
            'zona_horaria',
            'decimales',
            'simbolo_moneda',
            'documentos_obligatorios',
            'separador_miles',
            'separador_decimal',
            'prefijo_cel',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class RubrosForm(forms.ModelForm):

    class Meta:
        model = RubrosAsociados
        fields = [
            'descripcion',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
