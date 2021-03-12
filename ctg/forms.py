from django import forms

from .models import Categorias, Colores, Adicionales,\
    Items, DetalleItems, Tallas, Piedras, CategoriaPiedras,\
    CategoriaAdicionales, DetallePiedras, Divisiones, \
    PreciosDefinidos, Acabados, PartesInternas, \
    Anchuras
from est.models import Talleres, GruposEmpresariales


class PreciosDefinidosForm(forms.ModelForm):
    class Meta:
        model = PreciosDefinidos
        fields = [
            'descripcion',
            'tipo',
            'costo',
            'precio',
            'prct_utilidad']
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['costo']
        self.fields['tipo'].empty_label =\
            'Seleccionar Tipo'


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Divisiones
        fields = ['descripcion', 'tipo_catalogo']
        labels = {'descripcion': "Descripcion de división"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['tipo_catalogo'].empty_label =\
            'Seleccionar'


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = [
            'descripcion',
            'unidad_medida',
            'division',
            'permite_solicitud',
            'valor_gramo_diferenciado',
            'escala_peso',
            'parte_interna',
            'acabado',
            'costo_piedras',
            'tiempos_entrega',
            'proveedor',
            'envio_material',
            'datos_extra',
            'categoria_alianzas']
        labels = {'descripcion': "Descripcion de categoria"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        categoria = kwargs.pop('categoria', None)
        taller_obj = self.request.user.taller()
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['unidad_medida'].empty_label =\
            'Seleccionar'
        self.fields['division'].empty_label =\
            'Seleccionar'

        if not categoria:
            self.fields['division'].queryset = \
                Divisiones.objects.\
                filter(taller_id=taller_obj.id_taller)
        else:
            self.fields['division'].queryset = \
                Divisiones.objects.\
                filter(taller_id=categoria.division.taller_id)


class TallasForm(forms.ModelForm):
    class Meta:
        model = Tallas
        fields = ['talla', 'estandar', 'diametro']
        labels = {'talla': "Descripcion de talla"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['estandar'].empty_label =\
            'Seleccione estándar'


class ColoresForm(forms.ModelForm):
    class Meta:
        model = Colores
        fields = ['descripcion',
                  'costo_adicional_ta',
                  'precio_adicional_op',
                  'precio_adicional_ta'
                  ]

        labels = {'descripcion': "Descripcion de color"}
        widget = {'descripción': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AdicionalesForm(forms.ModelForm):
    class Meta:
        model = Adicionales
        fields = ['descripcion',
                  'sku',
                  'imagen',
                  'costo_taller',
                  'precio_taller',
                  'utilidad_operaciones']
        labels = {
            'descripcion': "Descripcion de color"}

        widget = {
            'descripción': forms.TextInput,
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mt-3'
            })}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class PiedrasForm(forms.ModelForm):
    class Meta:
        model = Piedras
        fields = ['imagen',
                  'sku',
                  'descripcion']
        labels = {'descripcion': "Descripcion de piedra"}
        widget = {
            'descripción': forms.TextInput,
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mt-3'
            })}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class DetallesPiedraForm(forms.ModelForm):
    class Meta:
        model = DetallePiedras
        fields = ['medida',
                  'costo_taller',
                  'precio_taller'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['sku',
                  'descripcion',
                  'categoria',
                  'escala_peso',
                  'parte_interna',
                  'acabado',
                  'tiempo_entrega_min',
                  'tiempo_entrega_max',
                  'cantidad_piedras',
                  'costo_piedras',
                  'valor_gramo_dif',
                  'peso_max_dif',
                  'datos_extra']
        labels = {'descripcion': "Descripcion de color"}
        widget = {'descripción': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['categoria'].empty_label =\
            'Seleccionar'


class DetallesForm(forms.ModelForm):
    class Meta:
        model = DetalleItems
        fields = [
            # 'id_item',
            'peso_minimo',
            'peso_maximo',
            'cantidad_piedras',
            'costo_piedras'
            ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        taller = Talleres.objects.filter(nombre='NEUTRO').first()
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AcabadosForm(forms.ModelForm):
    class Meta:
        model = Acabados
        fields = ['descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class PartesInternasForm(forms.ModelForm):
    class Meta:
        model = PartesInternas
        fields = ['descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AnchurasForm(forms.ModelForm):
    class Meta:
        model = Anchuras
        fields = ['descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
