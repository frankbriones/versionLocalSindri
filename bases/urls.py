from django.urls import path, include
from django.contrib.auth import views as auth_views

from bases.views import Home, SinPermisosTemplate, Logout,\
     error404Template, user_login

urlpatterns = [
     path('',
          Home.as_view(),
          name='home'
          ),
     path('login/',
          user_login,
          name='login'
          ),
     path('logout/',
          auth_views.LogoutView.as_view(template_name='bases/login.html'),
          name='logout'
          ),
     path('logoutmodal/',
          Logout.as_view(),
          name='logout_modal'
          ),
     path('sin_permisos/',
          SinPermisosTemplate.as_view(),
          name='sin_permisos'
          ),
     path('error404/',
          error404Template.as_view(),
          name='error404'
          ),
     path('password_reset/',
          auth_views.PasswordResetView.as_view(
               template_name='usr/contrasena_olvidada.html'
          ),
          name='password_reset'
          ),
     path('usuarios/password_reset/done/',
          auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_done'
          ),
     path('usuarios/reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
               template_name='bases/resetear_contrasena.html'
          ),
          name='password_reset_confirm'
          ),
     path('usuarios/reset/done/',
          auth_views.PasswordResetCompleteView.as_view(
               template_name='bases/resetear_contrasena_confirmado.html'
          ),
          name='password_reset_complete'
          ),
]
