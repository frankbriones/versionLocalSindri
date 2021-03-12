from django.db import models

from bases.models import Estados, ClaseModelo
# from usr.models import Taller
from ubc.models import Paises, Ciudades

class Clientes(ClaseModelo):
    id_cliente = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=30)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudades,
                               on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    correo = models.EmailField()

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Clientes, self).save()

    class Meta:
        verbose_name_plural = 'Clientes'
        ordering = ["apellidos"]
        unique_together = (('pais', 'identificacion'),)
