from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.views import generic
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from usr.backends import EmailBackend
from usr.models import Usuarios, UsuariosTiendas
from est.models import Tiendas


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url = 'bases:login'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        tienda_user = UsuariosTiendas.objects.filter(usuario_id=self.request.user.id).first()
        if tienda_user:
            tienda = Tiendas.objects.filter(id_tienda=tienda_user.tienda_id).first()
            tienda_id = tienda.id_tienda
            context['tienda_id'] = tienda_id
            if context:
                return context
            else:
                return None


def user_login(request):
    template_name = "bases/login.html"
    form = {}
    contexto = {}

    if request.method == 'POST':
        form = AuthenticationForm(request.user, request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = EmailBackend.authenticate(
            EmailBackend,
            request,
            username,
            password
        )
        if user is not None:
            login(request, user)
            return redirect("bases:home")

    return render(request, template_name, {'form': form})


class Logout(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/logout.html'
    login_url = 'bases:login'


class SinPermisosTemplate(LoginRequiredMixin, generic.TemplateView):
    login_url = 'bases:login'
    template_name = 'bases/sin_permisos.html'


class error404Template(LoginRequiredMixin, generic.TemplateView):
    login_url = 'bases:login'
    template_name = 'bases/error404.html'


class SinPermisos(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'bases:login'
    raise_exception = False
    redirect_field_name = 'redirect_to'

    def handle_no_permission(self):
        if not self.request.user == AnonymousUser():
            self.login_url = 'bases:sin_permisos'
        return HttpResponseRedirect(reverse_lazy(self.login_url))
