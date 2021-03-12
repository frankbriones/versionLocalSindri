from django.db import models
from django.contrib.auth.models import User


class ClaseModelo(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_crea = models.IntegerField(blank=False,
                                       null=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modifica = models.IntegerField(blank=True,
                                           null=True)

    class Meta:
        abstract = True


class Estados(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descripcion = models.CharField(unique=True, max_length=100)
    orden = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.descripcion)

    # class Meta:
    #     managed = False
    #     #db_table = 'tb_estados'
