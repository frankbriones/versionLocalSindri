from django import forms

from .models import Regiones, Paises, Localidades, \
    Ciudades
from bases.models import Estados
from est.models import Zonas, Sectores, GruposEmpresariales

class RegionForm(forms.ModelForm):
    class Meta:
        model = Regiones
        fields = ['nombre']
        labels = {'nombre': "Nombre de region"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class PaisForm(forms.ModelForm):
    class Meta:
        model = Paises
        fields = [
            'nombre',
            'region',
            'iniciales',
            'bandera',
            'zona_horaria',
            'decimales',
            'simbolo_moneda',
            'prefijo_cel',
            'separador_miles',
            'separador_decimal'
        ]
        labels = {'nombre': "Nombre de pais"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['region'].empty_label = 'Seleccione region'


class LocalidadForm(forms.ModelForm):
    class Meta:
        model = Localidades
        fields = ['nombre', 'pais']
        labels = {'nombre': "Nombre de localidad"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['pais'].empty_label = 'Seleccione pais'

        if not self.request.user.is_superuser:
            self.fields['pais'].queryset = \
                Paises.objects.filter(id_pais=self.request.user.pais_id)


class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zonas
        fields = ['nombre', 'grupo_empresarial']
        labels = {'nombre': "Grupo Empresarial"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['grupo_empresarial'].empty_label = 'Seleccione Grupo'

        if not self.request.user.is_superuser:
            self.fields['grupo_empresarial'].queryset = GruposEmpresariales.objects.all()


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudades
        fields = ['nombre', 'localidad']
        labels = {'nombre': "Nombre de ciudad"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['localidad'].empty_label = 'Seleccione localidad'

        if not self.request.user.is_superuser:
            estado = Estados.objects.\
                filter(descripcion='ACTIVO').first()
            self.fields['localidad'].queryset = \
                Localidades.objects.\
                filter(pais_id=self.request.user.pais_id).\
                filter(estado_id=estado.id_estado)


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sectores
        fields = ['nombre', 'grupo_empresarial']
        labels = {'nombre': "Nombre de sector"}
        widget = {'nombre': forms.TextInput}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })