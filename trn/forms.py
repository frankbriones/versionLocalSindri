from django import forms

from betterforms.multiform import MultiModelForm

from .models import SolicitudTrabajo, DetalleSolicitud,\
    OrdenTrabajo, DetalleOrden, ConfiguracionTooltipOperaciones,\
    ConfiguracionRechazoSolicitudOrdenes

from prv.models import Proveedores
# from usr.models import Taller
from ctg.models import Colores, Tallas, Items
from est.models import Talleres, GruposEmpresariales


# class ConfiguracionTooltipForm(forms.ModelForm):

#   class Meta:
#     model = ConfiguracionTooltipOperaciones
#     fields = '__all__'

class ConfiguracionTooltipForm(forms.ModelForm):


    class Meta:
        model = GruposEmpresariales
        fields = [
                  'anticipo_fabricacion',
                  'envio_material',
                  'comprobante_env',
                  'envio_incluido',
                  'factura_taller',
                  'cta_por_pagar',
                  'orden_compra'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class SolicitudesForm(forms.ModelForm):
    class Meta:
        model = SolicitudTrabajo
        fields = ['taller',
                  'proveedor',
                  'talla',
                  'longitud',
                  'detalle',
                  'acabado',
                  'parte_interna',
                  'cantidad_piedras',
                  'sku_relacionado',
                  'color',
                  'peso_min',
                  'peso_max',
                  'costo_fabricacion_unitario',
                  'prct_impuestos_ta',
                  'precio_fabricacion_unitario',
                  'tiempo_ent_min',
                  'tiempo_ent_max',
                  'origen_material'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        tipo = kwargs.pop('tipo')
        id_item = kwargs.pop('id_item')
        item = Items.objects.filter(id_item=id_item).first()
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['origen_material'].empty_label = 'Seleccione un origen'

        if tipo == 1:
            self.fields['proveedor'].required = False
            self.fields['peso_min'].required = False
            self.fields['peso_max'].required = False
            self.fields['precio_fabricacion_unitario'].required = False
            self.fields['tiempo_ent_min'].required = False
            self.fields['tiempo_ent_max'].required = False

        if tipo == 2:
            self.fields['taller'].required = False

        # self.fields['talla'].empty_label =\
        #     'Seleccione una talla'
        # self.fields['color'].empty_label =\
        #     'Seleccione un color'

        # if not self.request.user.is_superuser:
        #     taller_neutral = Taller.objects.filter(nombre='NEUTRO').first()
        #     if self.request.user.taller_id == taller_neutral.id:
        #         self.fields['proveedor'].queryset = Proveedores.objects.\
        #             filter(pais_id=self.request.user.pais_id).\
        #             filter(taller=taller_neutral.id, estado_id=1)
        #     else:
        #         self.fields['proveedor'].queryset = Proveedores.objects.\
        #             filter(taller=self.request.user.taller_id, estado_id=1)

        # if not self.request.user.is_superuser:
        #     self.fields['taller'].queryset = \
        #         Taller.objects.filter(pais_id=self.request.user.pais_id)

        # if not self.request.user.is_superuser:
        #     self.fields['talla'].queryset = \
        #         Tallas.objects.filter(
        #             taller_id=item.taller_id,
        #             estado_id=1
        #         ) | Tallas.objects.filter(taller_id=1)

        # if not self.request.user.is_superuser:
        #     self.fields['color'].queryset = \
        #         Colores.objects.filter(
        #             taller_id=item.taller_id,
        #             estado_id=1
        #         )


class DetalleSolicitudForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitud
        fields = ['item'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        tipo = kwargs.pop('tipo')
        id_item = kwargs.pop('id_item')
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        # if tipo == 1:
        #     self.fields['item'].required = False

        # # self.fields['item'].empty_label =\
        # #     'Seleccione un item'

        # if not self.request.user.is_superuser:
        #     self.fields['item'].queryset = \
        #         Items.objects.filter(pais_id=self.request.user.pais_id).\
        #         filter(costo=0)


class SolicitudDetalleForm(MultiModelForm):
    form_classes = {
        'solicitud': SolicitudesForm,
        'detalle': DetalleSolicitudForm,
    }


class SolicitudEditarForm(forms.ModelForm):
    class Meta:
        model = SolicitudTrabajo
        fields = ['peso_min',
                  'peso_max',
                  'costo_fabricacion_unitario',
                  'prct_impuestos_ta',
                  'precio_fabricacion_unitario',
                  'tiempo_ent_min',
                  'tiempo_ent_max',
                  'acabado',
                  'parte_interna',
                  'cantidad_piedras',
                  'detalle',
                  'color',
                  'proveedor',
                  'talla',
                  'longitud',
                  'sku_relacionado',
                  'origen_material',
                  
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        id_item = kwargs.pop('id_item')
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['proveedor'].empty_label =\
            'Seleccione un proveedor'

        if not self.request.user.is_superuser:
            # self.fields['proveedor'].queryset = \
            #     Proveedores.objects.filter(pais_id=self.request.user.pais_id)
            taller_neutral = Talleres.objects.filter(nombre='NEUTRO').first()
            if self.request.user.taller() == taller_neutral:
                self.fields['proveedor'].queryset = Proveedores.objects.\
                    filter(pais_id=self.request.user.pais_id).\
                    filter(taller=taller_neutral.id_taller, estado_id=1)
            else:
                self.fields['proveedor'].queryset = Proveedores.objects.\
                    filter(taller=self.request.user.taller().id_taller, estado_id=1)


class OrdenEnvioMaterialForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['comp_envio_ta'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class OrdenAnticipoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['anticipo_fabricacion'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ObservacionForm(forms.ModelForm):

    class Meta:
        model = ConfiguracionRechazoSolicitudOrdenes
        fields = ['titulo_rechazo', 'observacion_rechazo']
        labels = {'titulo observacion': "Descripcion del Rechazo"}
        widget = {'titulo_rechazo': forms.TextInput, 'observacion_rechazo': forms.Textarea}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        