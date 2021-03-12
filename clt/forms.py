from django import forms

from .models import Clientes
from ubc.models import Ciudades


class ClientesForm(forms.ModelForm):

    class Meta:
        model = Clientes
        fields = [
            'identificacion',
            'nombres',
            'apellidos',
            'ciudad',
            'direccion',
            'telefono',
            'correo'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ciudad'].empty_label = 'Seleccione ciudad'

        if not self.request.user.is_superuser:
            self.fields['ciudad'].queryset = \
                Ciudades.objects.filter(pais_id=self.request.user.pais_id)
