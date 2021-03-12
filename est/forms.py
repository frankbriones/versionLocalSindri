from django import forms

from .models import GruposEmpresariales, Sociedades,\
    Tiendas, Talleres


class GrupoEmpresarialForm(forms.ModelForm):
    class Meta:
        model = GruposEmpresariales
        fields = [
            'nombre',
            'logotipo',
            'pais'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class SociedadForm(forms.ModelForm):
    class Meta:
        model = Sociedades
        fields = [
            'nombre',
            'grupo_empresarial',
            'costo_gramo_base',
            'precio_gramo_base'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tiendas
        fields = [
            'codigo',
            'nombre',
            'sociedad',
            'zona',
            'ciudad',
            'sector',
            'matriz',
            'email',
            'direccion_tienda',
            'telefono'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class TallerForm(forms.ModelForm):
    class Meta:
        model = Talleres
        fields = [
            'nombre',
            'logotipo',
            'pais'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })








from est.models import Sectores

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sectores
        fields = ['nombre']
        labels = {'nombre': "Nombre de sector"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })





