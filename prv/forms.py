from django import forms

from .models import Proveedores
from ubc.models import Ciudades
from est.models import Zonas


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedores
        fields = ['identificacion',
                  'nombres',
                  'apellidos',
                  'ciudad',
                  'zona',
                  'direccion',
                  'telefono',
                  'correo',
                  'escala_peso',
                  'secuencia_ordenes',
                  'secuencia_solicitudes',
                  'costo_gramo',
                  'prct_impuestos'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ciudad'].empty_label = 'Seleccione ciudad'
        self.fields['zona'].empty_label = 'Seleccione zona'

        if not self.request.user.is_superuser:
            self.fields['ciudad'].queryset = \
                Ciudades.objects.filter(pais_id=self.request.user.pais_id)
            self.fields['zona'].queryset = \
                Zonas.objects.filter(grupo_empresarial__pais_id=self.request.user.pais_id)
