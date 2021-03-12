from django.db import models

from bases.models import Estados, ClaseModelo


class Regiones(ClaseModelo):
    id_region = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Regiones, self).save()

    class Meta:
        verbose_name_plural = 'Regiones'
        ordering = ["nombre"]


class Paises(ClaseModelo):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    iniciales = models.CharField(max_length=5, default=None)
    region = models.ForeignKey(Regiones,
                               on_delete=models.CASCADE)
    aut_externo = models.BooleanField(default=False)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    bandera = models.ImageField(upload_to='banderas', null=True, blank=True)
    simbolo_moneda = models.CharField(max_length=10)
    decimales = models.BooleanField(default=True)
    zona_horaria = models.CharField(max_length=100)
    documentos_obligatorios = models.BooleanField(default=True)
    prefijo_cel = models.CharField(max_length=10)
    separador_miles = models.CharField(max_length=5)
    separador_decimal = models.CharField(max_length=5)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Paises, self).save()

    class Meta:
        verbose_name_plural = 'Paises'
        ordering = ["nombre"]


class Localidades(ClaseModelo):
    id_localidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Localidades, self).save()

    class Meta:
        verbose_name_plural = 'Localidades'
        ordering = ["nombre"]
        unique_together = (('pais', 'nombre'),)


# class Zonas(ClaseModelo):
#     id_zona = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=500)
#     pais = models.ForeignKey(Paises,
#                              on_delete=models.CASCADE)
#     estado = models.ForeignKey(Estados,
#                                on_delete=models.CASCADE,
#                                default=1)

#     def __str__(self):
#         return '{}'.format(self.nombre)

#     def save(self):
#         self.nombre = self.nombre.upper()
#         super(Zonas, self).save()

#     class Meta:
#         verbose_name_plural = 'Zonas'
#         ordering = ["nombre"]
#         unique_together = (('pais', 'nombre'),)


class Ciudades(ClaseModelo):
    id_ciudad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    localidad = models.ForeignKey(Localidades,
                                  on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE,
                             default=1)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Ciudades, self).save()

    class Meta:
        verbose_name_plural = 'Ciudades'
        ordering = ["nombre"]
        unique_together = (('localidad', 'nombre'),)


# class Sectores(ClaseModelo):
#     id_sector = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=500)
#     pais = models.ForeignKey(Paises,
#                              on_delete=models.CASCADE,
#                              default=1)
#     estado = models.ForeignKey(Estados,
#                                on_delete=models.CASCADE,
#                                default=1)

#     def __str__(self):
#         return '{}'.format(self.nombre)

#     def save(self):
#         self.nombre = self.nombre.upper()
#         super(Sectores, self).save()

#     class Meta:
#         verbose_name_plural = 'Sectores'
#         ordering = ["nombre"]
#         unique_together = (('pais', 'nombre'),)
