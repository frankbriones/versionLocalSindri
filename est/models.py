from django.db import models

from bases.models import ClaseModelo, Estados
from ubc.models import Paises, Ciudades

class ManejadorGruposEmpresariales(models.Manager):
    def num_sociedades_relacionadas(self, id_grupo_empresarial):
        cantidad = Sociedades.objects.\
            filter(grupo_empresarial_id=id_grupo_empresarial).count()
        return cantidad

    def num_sociedades_activas(self, id_grupo_empresarial):
        cantidad = Sociedades.objects.\
            filter(
                grupo_empresarial_id=id_grupo_empresarial,
                estado__descripcion='ACTIVO'
                ).count()
        return cantidad


class GruposEmpresariales(ClaseModelo):
    id_grupo_empresarial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    utilidad_sobre_taller = models.DecimalField(max_digits=12,
                                                decimal_places=8,
                                                default=0)
    limite_venta = models.IntegerField(default=0)
    costo_gramo_base = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           default=0)
    precio_gramo_base = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            default=0)
    utilidad_sobre_base = models.DecimalField(max_digits=12,
                                              decimal_places=8,
                                              default=0)
    aut_externo = models.BooleanField(default=False)
    descuento_max = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        default=0)
    prct_impuestos = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         default=0)
    configurado = models.BooleanField(default=False)
    origen_material = models.IntegerField(default=1)
    anticipo_fabricacion = models.BooleanField(default=True)
    envio_material = models.BooleanField(default=True)
    comprobante_env = models.BooleanField(verbose_name="Comprobante de envío",default=True)
    envio_incluido = models.BooleanField(default=False)
    factura_taller = models.BooleanField(default=True)
    cta_por_pagar = models.BooleanField(default=True)
    orden_compra = models.BooleanField(default=True)
    tipo_precio_predefinido = models.IntegerField(null=True,
                                                  blank=True)
    precio_gramo_final = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             default=0)
    logotipo = models.ImageField(upload_to='logotipos/', null=True, blank=True)
    politicas_pdf = models.FileField(upload_to='politicas/',
                                     null=True, blank=True)
    politicas_doc = models.FileField(upload_to='politicas/',
                                     null=True, blank=True)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    objects = ManejadorGruposEmpresariales()

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(GruposEmpresariales, self).save()

    def sociedades_asociadas(self):
        cantidad = GruposEmpresariales.objects.\
            num_sociedades_relacionadas(self.id_grupo_empresarial)
        return cantidad

    def sociedades_activas(self):
        cantidad = GruposEmpresariales.objects.\
            num_sociedades_activas(self.id_grupo_empresarial)
        return cantidad

    class Meta:
        unique_together = (('pais', 'nombre'),)
        permissions = [
            ('env_reportes', 'Permisos para configurar envio de reportes'),
        ]




class Zonas(ClaseModelo):
    id_zona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Zonas, self).save()

    class Meta:
        verbose_name_plural = 'Zonas'
        ordering = ["nombre"]
        unique_together = (('grupo_empresarial', 'nombre'),)




class Sectores(ClaseModelo):
    id_sector = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Sectores, self).save()

    class Meta:
        verbose_name_plural = 'Sectores'
        ordering = ["nombre"]
        unique_together = (('grupo_empresarial','nombre'),)






class ManejadorSociedades(models.Manager):
    def num_tiendas_relacionadas(self, id_sociedad):
        cantidad = Tiendas.objects.\
            filter(sociedad_id=id_sociedad).count()
        return cantidad

    def num_tiendas_activas(self, id_sociedad):
        cantidad = Tiendas.objects.\
            filter(
                sociedad_id=id_sociedad,
                estado__descripcion='ACTIVO'
                ).count()
        return cantidad


class Sociedades(ClaseModelo):
    id_sociedad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    costo_gramo_base = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       default=0)
    precio_gramo_base = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            default=0)
    objects = ManejadorSociedades()

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Sociedades, self).save()

    def tiendas_asociadas(self):
        cantidad = Sociedades.objects.\
            num_tiendas_relacionadas(self.id_sociedad)
        return cantidad

    def tiendas_activas(self):
        cantidad = Sociedades.objects.\
            num_tiendas_activas(self.id_sociedad)
        return cantidad

    class Meta:
        verbose_name_plural = 'Sociedades'
        ordering = ["nombre"]
        unique_together = (('grupo_empresarial', 'nombre'),)


# class ManejadorTiendas(models.Manager):
#     def num_usuarios_relacionadas(self, id_sociedad):
#         cantidad = Sociedades.objects.\
#             filter(sociedad_id=id_sociedad).count()
#         return cantidad

#     def num_tiendas_activas(self, id_sociedad):
#         cantidad = Sociedades.objects.\
#             filter(
#                 sociedad_id=id_sociedad,
#                 estado__descripcion='ACTIVO'
#                 ).count()
#         return cantidad


class Tiendas(ClaseModelo):
    id_tienda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    sociedad = models.ForeignKey(Sociedades,
                                 on_delete=models.CASCADE)
    zona = models.ForeignKey(Zonas,
                             on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudades,
                               on_delete=models.CASCADE)
    sector = models.ForeignKey(Sectores,
                               on_delete=models.CASCADE)
    matriz = models.BooleanField(default=False)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    direccion_tienda = models.CharField(max_length=500,
                                null=True,
                                help_text='Direccion de la tienda')
    email = models.EmailField(help_text='Correo de la tienda', max_length=254, null=True)
    telefono = models.CharField(max_length=15, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Tiendas, self).save()

    def tot_ordenes(self):
        registro = OrdenesTrabajo.objects.\
            filter(
                tienda_id=self.id_tienda
            ).count()
        if registro:
            return registro
        else:
            return None

    class Meta:
        verbose_name_plural = 'Tiendas'
        ordering = ["nombre"]
        unique_together = (('sociedad', 'nombre'),)


class Talleres(ClaseModelo):
    id_taller = models.AutoField(primary_key=True)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    costo_gramo_fabricacion = models.DecimalField(max_digits=15,
                                                  decimal_places=2,
                                                  default=0.00)
    precio_gramo_fabricacion = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   default=0.00)
    costo_gramo_base = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           default=0.00)
    precio_gramo_base = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            default=0.00)
    utilidad_sobre_fabricacion = models.DecimalField(max_digits=5,
                                                     decimal_places=2,
                                                     default=0.00)
    utilidad_sobre_base = models.DecimalField(max_digits=5,
                                              decimal_places=2,
                                              default=0.00)
    utilidad_sobre_piedras = models.DecimalField(max_digits=5,
                                                 decimal_places=2,
                                                 default=0.00)
    utilidad_sobre_adicionales = models.DecimalField(max_digits=5,
                                                     decimal_places=2,
                                                     default=0.00)
    prct_impuestos = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         default=0)
    tmp_resp_sol = models.IntegerField(default=5)
    escala_peso = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      default=0.10)
    estandar_tallas = models.IntegerField(default=1)
    configurado = models.BooleanField(default=False)
    externo = models.BooleanField(default=False)
    secuencia_ordenes = models.IntegerField(default=1)
    secuencia_solicitudes = models.IntegerField(default=1)
    prioridad = models.IntegerField()
    logotipo = models.ImageField(upload_to='logotalleres/',
                                 null=True,
                                 blank=True)
    recalcular_precio = models.BooleanField(default=False)
    cargar_img_fin_trabajo = models.BooleanField(default=False)
    tipo_precio_predefinido = models.IntegerField(null=True,
                                                  blank=True)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Talleres, self).save()

    class Meta:
        verbose_name_plural = 'Talleres'
        ordering = ["nombre"]
        unique_together = (('pais', 'nombre'),)
        permissions = [
            ('prioridad_taller', 'Permisos para prioridades de talleres.')
        ]
