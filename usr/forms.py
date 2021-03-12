from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from betterforms.multiform import MultiModelForm

from .models import Usuarios, UsuariosGrupos

from .models import TipoUsuarios, Roles
from cfg.models import ConfigGeneral
from ubc.models import Ciudades
from est.models import Sectores


class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuarios
        fields = ['descripcion']
        labels = {'descripcion': "Descripcion de tipo usuario"}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class GrupoForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class RolForm(forms.ModelForm):

    class Meta:
        model = Roles
        fields = [
            'descripcion',
            'zonal']
        labels = {'descripcion': 'Descripcion del rol'}
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class RolGrupoForm(MultiModelForm):
    form_classes = {
        'grupo': GrupoForm,
        'rol': RolForm,
    }


class RegistroForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Usuarios
        fields = [
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'rol',
                  'telefono',
                  'img_perfil',
                  'usuario_telegram'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AsignarGrupoForm(forms.ModelForm):

    class Meta:
        model = UsuariosGrupos
        fields = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class UsuarioGrupoForm(MultiModelForm):
    form_classes = {
        'usuario': RegistroForm,
        'grupo': AsignarGrupoForm,
    }


class EditarForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Usuarios
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'rol',
                  'telefono',
                  'img_perfil',
                  
                  ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class EditarUsuarioForm(MultiModelForm):
    form_classes = {
        'usuario': EditarForm,
        # 'grupo': AsignarGrupoForm,
    }


class EditarPerfilForm(forms.ModelForm):

    class Meta:
        model = Usuarios
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'telefono',
                  'img_perfil',
                  'usuario_telegram',
                  'ver_notificaciones'
                  ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
