from django.db import models

from bases.models import ClaseModelo
from ubc.models import Paises, Ciudades
from prv.models import Proveedores
from est.models import Zonas, Sectores, GruposEmpresariales
from usr.models import Roles


class ConfiguracionSistema(models.Model):
    clave = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    observacion = models.CharField(max_length=100,
                                   null=True,
                                   blank=True)



class ConfigGeneral(ClaseModelo):
    empresa = models.CharField(max_length=100)
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
    comprobante_env = models.BooleanField(default=True)
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

    class Meta:
        unique_together = (('pais', 'empresa'),)
        # permissions = [
        #     ('envio_material', 'Permiso para envio_material')
        # ]



class ConfigUtilidadTaller(ClaseModelo):
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    id_usuario_op = models.IntegerField(default=1)
    usuario_op = models.CharField(max_length=200)
    id_taller = models.IntegerField(default=1)
    taller = models.CharField(max_length=200)
    utilidad = models.DecimalField(max_digits=5,
                                   decimal_places=2)

    class Meta:
        unique_together = (('id_usuario_op', 'id_taller'),)


class ConfigUtilidadProveedor(ClaseModelo):
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    id_usuario_op = models.IntegerField(default=1)
    usuario_op = models.CharField(max_length=200)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    proveedor = models.ForeignKey(Proveedores,
                                  on_delete=models.CASCADE)
    utilidad = models.DecimalField(max_digits=5,
                                   decimal_places=2)

    class Meta:
        unique_together = (('id_usuario_op', 'proveedor'),)


class OperacionesTallerVista(models.Model):
    id_user = models.IntegerField()
    username = models.CharField(max_length=500)
    id_taller = models.IntegerField()
    nombre_taller = models.CharField(max_length=500)
    pais_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_operaciones_taller'


class ZonasTallerVista(models.Model):
    id_zona = models.IntegerField()
    nombre = models.CharField(max_length=500)
    id_taller = models.IntegerField()
    nombre_taller = models.CharField(max_length=500)
    pais_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_zonas_taller'


class SectoresTallerVista(models.Model):
    id_sector = models.IntegerField()
    nombre = models.CharField(max_length=500)
    id_taller = models.IntegerField()
    nombre_taller = models.CharField(max_length=500)
    pais_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_sectores_taller'


class OperacionesProveedorVista(models.Model):
    id_user = models.IntegerField()
    username = models.CharField(max_length=500)
    id_proveedor = models.IntegerField()
    nombres = models.CharField(max_length=500)
    apellidos = models.CharField(max_length=500)
    pais_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_operaciones_proveedor'


class ZonasProveedorVista(models.Model):
    id_zona = models.IntegerField()
    nombre = models.CharField(max_length=500)
    id_proveedor = models.IntegerField()
    nombres = models.CharField(max_length=500)
    apellidos = models.CharField(max_length=500)
    pais_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_zonas_proveedor'


class ConfiguracionApiSMS(models.Model):
    clave = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    observacion = models.CharField(max_length=100,
                                   null=True,
                                   blank=True)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        permissions = [
            ('envio_sms', 'Permiso para envio de sms')
        ]


class ConfiguracionReporteUsuarios(models.Model):
    usuario_crea = models.IntegerField(null=True, blank=True)
    grupo_empresarial_id = models.IntegerField(null=True, blank=True)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    taller_id = models.IntegerField(null=True, blank=True)


    class Meta:
        permissions = [
            ('envio_reporte_user', 'Permiso para reporte de conexion')
        ]


# class ConfiguracionEnvioMaterial(models.Model):
#     usuario_crea = models.IntegerField(null=True, blank=True)
#     pais = models.IntegerField(null=True, blank=True)
#     observacion = models.CharField(max_length=100,
#                                    null=True,
#                                    blank=True)
#     class Meta:
#         permissions = [
#             ('envio_material', 'Permiso para envio de material')
#         ]



class PoliticasComerciales(ClaseModelo):
    id_politica = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    empresa = models.ForeignKey(GruposEmpresariales,
                                on_delete=models.CASCADE)
    ordenamiento = models.IntegerField()
