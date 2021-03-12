from django.db import models

from usr.models import Usuarios
from est.models import Talleres, Tiendas
from bases.models import Estados


class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    usuario_genera = models.ForeignKey(Usuarios,
                                       on_delete=models.CASCADE)
    #  tipo 1 operaciones tipo 2 taller
    tipo_notificacion = models.IntegerField(null=True, blank=True, default=0)
    tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=500)
    vista = models.BooleanField(default=False)
    principal = models.BooleanField(default=False)
    postergada = models.BooleanField(default=False)
    id_transaccion = models.IntegerField(null=True, blank=True)
    #  tipo 1 solicitudes tipo 2 ordenes
    tipo_transaccion = models.IntegerField(null=True, blank=True)

    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Notificaciones'
        ordering = ["-fecha_creacion"]
