from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Usuarios


@shared_task
def enviarCorreoContrasena(id, contrasena, tipo):
    usuario = Usuarios.objects.filter(pk=id).first()
    correos = []
    correo_usuario = usuario.email
    correos.append(correo_usuario)
    to = correos
    desde = settings.EMAIL_HOST_USER
    from_email = desde
    if tipo == 1:
        subject = "Nuevo usuario creado"
        message = "El usuario " + usuario.first_name + " "\
            + usuario.last_name + " se ha creado,"\
            + " su contraseña es: " + contrasena
    else:
        subject = "Reestablecimiento de contraseña"
        message = "Saludos " + usuario.first_name + " "\
            + usuario.last_name \
            + " se le ha asignado la siguiente contraseña temporal: "\
            + contrasena

    email = EmailMessage(subject, message, bcc=to, from_email=from_email)
    # email.content_subtype = "text"
    email.send()
