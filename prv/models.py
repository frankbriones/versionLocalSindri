from django.db import models

from bases.models import ClaseModelo
from ubc.models import Paises, Ciudades
from bases.models import Estados
from est.models import Zonas

class Proveedores(ClaseModelo):
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=30,
                                      null=False,
                                      blank=False)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=50, null=True)
    correo = models.EmailField(unique=True, null=True)
    zona = models.ForeignKey(Zonas,
                             on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudades,
                               on_delete=models.CASCADE,
                               default=1)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    tipo_usuario = models.IntegerField(null=False,
                                       blank=False,
                                       default=1)
    taller = models.IntegerField(null=True)
    escala_peso = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      default=0.10)
    secuencia_ordenes = models.IntegerField(default=1)
    secuencia_solicitudes = models.IntegerField(default=1)
    costo_gramo = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    prct_impuestos = models.DecimalField(max_digits=15,
                                         decimal_places=2)

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Proveedores, self).save()

    class Meta:
        verbose_name_plural = 'Proveedores'
        ordering = ["apellidos", "nombres"]
        unique_together = (('pais', 'identificacion'),)
