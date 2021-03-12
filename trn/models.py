from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from bases.models import Estados, ClaseModelo
from ubc.models import Paises
from clt.models import Clientes
from usr.models import Usuarios
from ctg.models import Tallas, Colores, Categorias, Piedras, DetallePiedras, Adicionales
from prv.models import Proveedores
from ctg.models import Items, DetalleItems, Adicionales
from est.models import Talleres, Tiendas, GruposEmpresariales

# signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from fn_compartidas import fnImagenes


class ConfiguracionRechazoSolicitudOrdenes(ClaseModelo):
  ''' 
    Modelo ConfiguracionRechazoSolicitudOrdenes..

    las propiedades del modelo, haran referencia a un concepto,
    que se usara como estandar para las ordenes o solicitudes
    que sean canceladas
    o rechazadas respectivamente.
  '''
  id_obs_rechazo = models.AutoField(primary_key=True)
  titulo_rechazo = models.CharField(max_length=80, help_text="texto a mostrar en modal")
  observacion_rechazo = models.CharField(max_length=500, help_text="factor comun del rechazo")
  taller = models.ForeignKey(Talleres, on_delete=models.CASCADE, default=None, blank=True, null=True)
  grupo_empresarial = models.ForeignKey(GruposEmpresariales, on_delete=models.CASCADE, default=None, blank=True, null=True)
  pais = models.ForeignKey(Paises, on_delete=models.CASCADE, default=None, blank=True, null=True)
  estado = models.ForeignKey(Estados, on_delete=models.CASCADE, default=1, blank=True, null=True)

  def save(self):
        self.descripcion = self.descripcion.upper()
        super(RubrosAsociados, self).save()

  def save(self):
    self.titulo_rechazo = self.titulo_rechazo.upper()
    super(ConfiguracionRechazoSolicitudOrdenes, self).save()

  class Meta:
        permissions = [
            ('permiso_motivo_rechazo', 'Permiso para configurar motivos de rechazo.')
        ]




class OrigenMaterial(ClaseModelo):
    id_origen = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.descripcion)


class SolicitudTrabajo(ClaseModelo):
    id_solicitud = models.AutoField(primary_key=True)
    secuencia = models.CharField(max_length=50)
    # usuario = models.ForeignKey(Usuarios,
    #                             on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE,
                               default=1)
    proveedor = models.ForeignKey(Proveedores,
                                  on_delete=models.CASCADE,
                                  default=1)
    rechazo = models.ForeignKey(ConfiguracionRechazoSolicitudOrdenes,\
      on_delete=models.CASCADE,
      null=True,
      default=None,
      blank=True
      )
    externa = models.BooleanField()
    origen_material = models.ForeignKey(OrigenMaterial,
                                        on_delete=models.CASCADE)
    peso_min = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0)
    peso_max = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0)
    talla = models.ForeignKey(Tallas,
                              on_delete=models.CASCADE)
    color = models.ForeignKey(Colores,
                              on_delete=models.CASCADE)
    longitud = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0)
    costo_gramo_base_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_gramo_base_taller = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    prct_utilidad_base_taller = models.DecimalField(max_digits=12,
                                                    decimal_places=8,
                                                    null=True,
                                                    blank=True,
                                                    default=0)
    utilidad_base_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    costo_base_total_ta = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True,
                                              default=0)
    precio_base_total_ta = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    costo_fabricacion_unitario = models.DecimalField(max_digits=30,
                                                     decimal_places=2,
                                                     null=True,
                                                     blank=True)
    precio_fabricacion_unitario = models.DecimalField(max_digits=30,
                                                      decimal_places=2,
                                                      null=True,
                                                      blank=True)
    costo_total_fabricacion_ta = models.DecimalField(max_digits=30,
                                                     decimal_places=2,
                                                     null=True,
                                                     blank=True)
    precio_fabricacion_total = models.DecimalField(max_digits=30,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    prct_util_sobre_fabrica_ta = models.DecimalField(max_digits=12,
                                                     decimal_places=8,
                                                     null=True,
                                                     blank=True,
                                                     default=0)
    util_sobre_fabrica_ta = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    # valor_error = models.DecimalField(max_digits=30,
    #                                   decimal_places=2,
    #                                   null=True,
    #                                   blank=True)
    total_rubros = models.DecimalField(max_digits=30,
                                       decimal_places=2,
                                       default=0)
    subtotal_taller = models.DecimalField(max_digits=30,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    prct_impuestos_ta = models.DecimalField(max_digits=5,
                                            decimal_places=2,
                                            default=0)
    impuestos_taller = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           default=0)
    total_taller = models.DecimalField(max_digits=30,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    costo_gramo_base_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    precio_gramo_base_op = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    prct_util_sobre_base_op = models.DecimalField(max_digits=12,
                                                  decimal_places=8,
                                                  null=True,
                                                  blank=True,
                                                  default=0)
    costo_base_total_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    precio_base_total_op = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    util_sobre_base_op = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             null=True,
                                             blank=True,
                                             default=0)
    prct_util_sobre_fabrica_op = models.DecimalField(max_digits=12,
                                                     decimal_places=8,
                                                     null=True,
                                                     blank=True,
                                                     default=0)
    util_sobre_fabrica_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    precio_unitario_op = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    precio_fabricacion_total_op = models.DecimalField(max_digits=15,
                                                      decimal_places=2,
                                                      null=True,
                                                      blank=True)
    subtotal_solicitud = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             default=0)
    prct_impuestos_op = models.DecimalField(max_digits=5,
                                            decimal_places=2,
                                            default=0)
    impuestos_op = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       default=0)
    descuento_solicitud = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              default=0)
    precio_sistema = models.DecimalField(max_digits=30,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    precio_final_venta = models.DecimalField(max_digits=30,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    acabado = models.CharField(max_length=200,
                               null=True,
                               blank=True)
    parte_interna = models.CharField(max_length=200,
                                     null=True,
                                     blank=True)
    cantidad_piedras = models.IntegerField(null=True,
                                           blank=True)
    sku_relacionado = models.CharField(max_length=50,
                                       null=True,
                                       blank=True)
    tiempo_ent_min = models.IntegerField(null=True,
                                         blank=True)
    tiempo_ent_max = models.IntegerField(null=True,
                                         blank=True)
    tiempo_respuesta = models.DateTimeField(auto_now=False,
                                            auto_now_add=False,
                                            null=True,
                                            blank=True)
    detalle = models.CharField(max_length=5000, null=True, blank=True)
    observacion_rechazo_op = models.CharField(max_length=500,
                                              null=True,
                                              blank=True)
    observacion_rechazo_ta = models.CharField(max_length=500,
                                              null=True,
                                              blank=True)
    observacion_cotizado = models.CharField(max_length=500,
                                            null=True,
                                            blank=True)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    generado_con_ext = models.BooleanField(default=False)
    solicitud_relacionada = models.CharField(max_length=100,
                                             null=True,
                                             blank=True)
    peso_solicitado = models.DecimalField(max_digits=10,
                                          decimal_places=2,
                                          default=0)
    unidades_solicitadas = models.IntegerField(default=1)
    fecha_cotizacion = models.DateTimeField(auto_now=False,
                                            auto_now_add=False,
                                            null=True,
                                            blank=True)
    tiempo_cotizacion = models.DecimalField(max_digits=50,
                                            decimal_places=2,
                                            null=True,
                                            blank=True)
    fabricacion_interna = models.BooleanField(default=0)

    fabricacion_dividida = models.BooleanField(default=0)


    origen_material_dividido = models.ForeignKey(OrigenMaterial,
                                  on_delete=models.CASCADE, null=True, blank=True, related_name="origen_dividido")
    peso_cliente_dividido = models.DecimalField(max_digits=30,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    peso_materia_dividida = models.DecimalField(max_digits=30,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)

    class Meta:
        verbose_name_plural = 'Solicitudes'
        ordering = ["-fecha_creacion"]
        permissions = [
            ('ver_detalle_costos_sol', 'Ver detalle de costos'),
            ('fabricacion_interna', 'Realizar Fabricaciones Internas'),
            ('fabricacion_dividida_solicitudes', 'Realizar Fabricaciones Divididas')
        ]


class DetalleSolicitud(ClaseModelo):
    id_detalle_solicitud = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudTrabajo,
                                  on_delete=models.CASCADE)
    item = models.ForeignKey(Items,
                             on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Detalles solicitudes'
        ordering = ["-fecha_creacion"]
        unique_together = (('pais', 'solicitud', 'item'),)


class SolicitudesPiedras(models.Model):
    id_solicitud_piedra = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudTrabajo,
                                  on_delete=models.CASCADE)
    piedra = models.ForeignKey(Piedras,
                               on_delete=models.CASCADE)
    piedra_detalle = models.ForeignKey(DetallePiedras,
                                       on_delete=models.CASCADE)
    cantidad_piedras = models.IntegerField()
    costo_piedra_taller = models.DecimalField(max_digits=15,
                                              decimal_places=2)
    precio_piedra_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2)
    prct_utilidad_piedra_op = models.DecimalField(max_digits=6,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_piedra_op = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    subtotal_piedras_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2)
    subtotal_piedras_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)

class SolicitudesAdicionales(models.Model):
    id_solicitud_adicional = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudTrabajo,
                                  on_delete=models.CASCADE)
    adicional = models.ForeignKey(Adicionales,
                               on_delete=models.CASCADE)
    cantidad_adicionales = models.IntegerField()
    costo_adicional_taller = models.DecimalField(max_digits=15,
                                              decimal_places=2)
    precio_adicional_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2)
    prct_utilidad_adicional_op = models.DecimalField(max_digits=6,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_adicional_op = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    subtotal_adicional_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2)
    subtotal_adicional_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)


class OrdenTrabajo(ClaseModelo):
    id_orden = models.AutoField(primary_key=True, auto_created=True)
    secuencia = models.CharField(max_length=50)
    cliente = models.ForeignKey(Clientes,
                                on_delete=models.CASCADE)
    # usuario = models.ForeignKey(Usuarios,
    #                             on_delete=models.CASCADE, related_name="user_orden")
    tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedores,
                                  on_delete=models.CASCADE, null=True, blank=True)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias,
                                  on_delete=models.CASCADE)
    color = models.ForeignKey(Colores,
                              on_delete=models.CASCADE)

    origen_material = models.ForeignKey(OrigenMaterial,
                                        on_delete=models.CASCADE)
    rechazo = models.ForeignKey(ConfiguracionRechazoSolicitudOrdenes,\
      on_delete=models.CASCADE,
      null=True,
      default=None,
      blank=True
      )

    fabricacion_dividida = models.BooleanField(default=0)


    datos_extra = models.CharField(max_length=200,
                                   null=True,
                                   blank=True)
    externa = models.BooleanField()
    env_material = models.BooleanField()
    gramos_enviados = models.DecimalField(max_digits=30,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    gramos_recibidos = models.DecimalField(max_digits=30,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    peso_solicitado = models.DecimalField(max_digits=20,
                                          decimal_places=2,
                                          default=0)
    unidades_solicitadas = models.IntegerField(default=1)
    peso_final = models.DecimalField(max_digits=20,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    costo_gramo_base_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_gramo_base_taller = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    prct_utilidad_base_taller = models.DecimalField(max_digits=12,
                                                    decimal_places=8,
                                                    null=True,
                                                    blank=True,
                                                    default=0)
    utilidad_base_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    costo_base_total_ta = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True,
                                              default=0)
    precio_base_total_ta = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    costo_fabricacion_unitario = models.DecimalField(max_digits=30,
                                                     decimal_places=2,
                                                     null=True,
                                                     blank=True)
    precio_fabricacion_unitario = models.DecimalField(max_digits=30,
                                                      decimal_places=2,
                                                      null=True,
                                                      blank=True)
    costo_total_fabricacion_ta = models.DecimalField(max_digits=30,
                                                     decimal_places=2,
                                                     null=True,
                                                     blank=True)
    precio_fabricacion_total = models.DecimalField(max_digits=30,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    prct_util_sobre_fabrica_ta = models.DecimalField(max_digits=12,
                                                     decimal_places=8,
                                                     null=True,
                                                     blank=True,
                                                     default=0)
    util_sobre_fabrica_ta = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    costo_color_unitario = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    costo_color_total = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            null=True,
                                            blank=True,
                                            default=0)
    costo_total_rubros = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             default=0)
    # valor_error = models.DecimalField(max_digits=15,
    #                                   decimal_places=2,
    #                                   default=0)
    servicio_fabricacion_total = models.DecimalField(max_digits=30,
                                                     decimal_places=2,
                                                     null=True,
                                                     blank=True)
    subtotal_taller = models.DecimalField(max_digits=30,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    prct_impuestos_ta = models.DecimalField(max_digits=5,
                                            decimal_places=2,
                                            default=0)
    impuestos_taller = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           default=0)
    costo_piedras_basicas = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                default=0)
    total_taller = models.DecimalField(max_digits=30,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    total_taller_recalculado = models.DecimalField(max_digits=30,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    costo_piedras_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True,
                                               default=0)
    util_sobre_piedras_taller = models.DecimalField(max_digits=15,
                                                    decimal_places=2,
                                                    null=True,
                                                    blank=True,
                                                    default=0)
    precio_piedras_taller = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    costo_adicionales_taller = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True,
                                                   default=0)
    util_sobre_adicionales_taller = models.DecimalField(max_digits=15,
                                                        decimal_places=2,
                                                        null=True,
                                                        blank=True,
                                                        default=0)
    precio_adicionales_taller = models.DecimalField(max_digits=15,
                                                    decimal_places=2,
                                                    null=True,
                                                    blank=True,
                                                    default=0)
    util_sobre_piedras_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    precio_piedras_op = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            null=True,
                                            blank=True,
                                            default=0)
    util_sobre_adicionales_op = models.DecimalField(max_digits=15,
                                                    decimal_places=2,
                                                    null=True,
                                                    blank=True)
    precio_adicionales_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    costo_gramo_base_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    precio_gramo_base_op = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    prct_util_sobre_base_op = models.DecimalField(max_digits=12,
                                                  decimal_places=8,
                                                  null=True,
                                                  blank=True,
                                                  default=0)
    costo_base_total_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    precio_base_total_op = models.DecimalField(max_digits=15,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    util_sobre_base_op = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             null=True,
                                             blank=True,
                                             default=0)
    prct_util_sobre_fabrica_op = models.DecimalField(max_digits=12,
                                                     decimal_places=8,
                                                     null=True,
                                                     blank=True,
                                                     default=0)
    util_sobre_fabrica_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True,
                                                default=0)
    precio_unitario_op = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    precio_fabricacion_total_op = models.DecimalField(max_digits=15,
                                                      decimal_places=2,
                                                      null=True,
                                                      blank=True)
    subtotal_orden = models.DecimalField(max_digits=15,
                                         decimal_places=2,
                                         default=0)
    prct_impuestos_op = models.DecimalField(max_digits=5,
                                            decimal_places=2,
                                            default=0)
    impuestos_op = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       default=0)
    descuento_orden = models.DecimalField(max_digits=15,
                                          decimal_places=2,
                                          default=0)
    precio_sistema = models.DecimalField(max_digits=30,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    precio_final_venta = models.DecimalField(max_digits=30,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    precio_recalculado = models.DecimalField(max_digits=30,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    comp_envio_ta = models.FileField(null=True,
                                     blank=True,
                                     upload_to='comprobantes_taller/')
    comp_envio_op = models.FileField(null=True,
                                     blank=True,
                                     upload_to='comprobantes_operaciones/')
    factura_vta = models.FileField(null=True,
                                   blank=True,
                                   upload_to='facturas/')
    costo_envio = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      null=True,
                                      blank=True,
                                      default=0)
    anticipo_fabricacion = models.FileField(null=True,
                                            blank=True,
                                            upload_to='anticipos/')
    factura_taller = models.FileField(null=True,
                                      blank=True,
                                      upload_to='facturas_taller/')
    cta_por_pagar = models.FileField(null=True,
                                     blank=True,
                                     upload_to='ctas_pagar/')
    orden_compra = models.FileField(null=True,
                                    blank=True,
                                    upload_to='orden_compra/')
    obs_recepcion_prod = models.CharField(max_length=500,
                                          null=True,
                                          blank=True)
    obs_venta = models.CharField(max_length=500,
                                 null=True,
                                 blank=True)
    obs_recepcion_mat = models.CharField(max_length=500,
                                         null=True,
                                         blank=True)
    fecha_envio_mat = models.DateTimeField(auto_now=False,
                                           auto_now_add=False,
                                           null=True,
                                           blank=True)
    fecha_recibe_mat = models.DateTimeField(auto_now=False,
                                            auto_now_add=False,
                                            null=True,
                                            blank=True)
    fecha_anulacion = models.DateTimeField(auto_now=False,
                                           auto_now_add=False,
                                           null=True,
                                           blank=True)
    fecha_fin_trabajo = models.DateTimeField(auto_now=False,
                                             auto_now_add=False,
                                             null=True,
                                             blank=True)
    fecha_envio_prod = models.DateTimeField(auto_now=False,
                                            auto_now_add=False,
                                            null=True,
                                            blank=True)
    fecha_recibe_prod = models.DateTimeField(auto_now=False,
                                             auto_now_add=False,
                                             null=True,
                                             blank=True)
    fecha_venta = models.DateTimeField(auto_now=False,
                                       auto_now_add=False,
                                       null=True,
                                       blank=True)
    tiempo_duracion_orden = models.DecimalField(max_digits=50,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    pago_aprobado = models.BooleanField(default=False)
    fecha_aprueba_pago = models.DateTimeField(auto_now=False,
                                              auto_now_add=False,
                                              null=True,
                                              blank=True)
    # orden_vendida = models.BooleanField(default=False)
    # usuario_aprueba_pago = models.IntegerField(null=True,
    #                                            blank=True)
    # costo_gramo_fabricado = models.DecimalField(max_digits=15,
    #                                             decimal_places=2,
    #                                             null=True,
    #                                             blank=True)
    orden_vendida = models.BooleanField(default=False)
    usuario_aprueba_pago = models.IntegerField(null=True,
                                               blank=True)
    orden_facturada = models.BooleanField(default=False)
    fecha_facturacion = models.DateTimeField(auto_now=False,
                                             auto_now_add=False,
                                             null=True,
                                             blank=True)
    usuario_registra_factura = models.IntegerField(null=True,
                                                   blank=True)
    orden_pagada = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(auto_now=False,
                                      auto_now_add=False,
                                      null=True,
                                      blank=True)
    usuario_registra_pago = models.IntegerField(null=True,
                                                blank=True)
    numero_factura = models.CharField(max_length=50,
                                      null=True,
                                      blank=True)

    fabricacion_interna = models.BooleanField(default=0)

    origen_material_dividido = models.ForeignKey(OrigenMaterial,
                                  on_delete=models.CASCADE, null=True, blank=True, related_name="origen_dividido_orden")
    peso_cliente_dividido = models.DecimalField(max_digits=30,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    peso_materia_dividida = models.DecimalField(max_digits=30,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)


    def diferencia_gramos(self):
        if self.gramos_recibidos and self.peso_final:
            diferencia_gramos = self.gramos_recibidos - self.peso_final
        else:
            diferencia_gramos = None
        return diferencia_gramos

    class Meta:
        verbose_name_plural = 'Ordenes de trabajo'
        ordering = ["-fecha_creacion"]
        permissions = [
            ('estadisticas_admin', 'Ver estadisticas administrador'),
            ('pagos_aprobados', 'Ver pagos aprobados'),
            ('ver_comp_envio_op', 'Ver comprobante envio material'),
            ('ver_comp_envio_ta', 'Ver comprobante envio producto'),
            ('envio_material_joyeria', 'Permiso para enviar el material al Taller'),
            ('ver_factura', 'Ver factura de venta'),
            ('ver_detalle_costos', 'Ver detalle de costos',),
            ('ver_anticipo', 'Ver anticipo de fabricacion'),
            ('ver_factura_taller', 'Ver factura de taller'),
            ('ver_cta_por_pagar', 'Ver cuenta por pagar'),
            ('ver_orden_compra', 'Ver orden de compra'),
            ('pagar_factura', 'Pagar facturas'),
            ('enviar_producto', 'Enviar Producto'),
            ('finalizar_trabajo', 'Finalizar Trabajo'),
            ('iniciar_orden', 'Iniciar Trabajo'),
            ('anular_orden', 'Anular Orden'),
            ('recibir_producto', 'Recibir Producto'),
            ('fabricacion_dividida_ordenes', 'Realizar Fabricaciones Divididas'),
        ]


class DetalleOrden(ClaseModelo):
    id_detalle_orden = models.AutoField(primary_key=True)
    orden = models.ForeignKey(OrdenTrabajo,
                              on_delete=models.CASCADE)
    id_solicitud = models.IntegerField(null=True, blank=True)
    id_item = models.IntegerField(null=True, blank=True)
    id_detalle_item = models.IntegerField(null=True, blank=True)
    id_adicional = models.IntegerField(null=True, blank=True)
    costo_unitario_adicional = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    prct_util_sobre_adicional = models.DecimalField(max_digits=5,
                                                    decimal_places=2,
                                                    null=True,
                                                    blank=True)
    utilidad_sobre_adicional = models.DecimalField(max_digits=15,
                                                   decimal_places=2,
                                                   null=True,
                                                   blank=True)
    precio_adicionales = models.DecimalField(max_digits=15,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)
    id_piedra = models.IntegerField(null=True, blank=True)
    id_detalle_piedra = models.IntegerField(null=True, blank=True)
    costo_unitario_piedra = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    prct_util_sobre_piedra = models.DecimalField(max_digits=5,
                                                 decimal_places=2,
                                                 null=True,
                                                 blank=True)
    utilidad_sobre_piedra = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    precio_piedras = models.DecimalField(max_digits=15,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    cantidad = models.IntegerField(default=1)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    precio_piedras_op = models.DecimalField(max_digits=15,
                                            decimal_places=2,
                                            null=True,
                                            blank=True)
    precio_adicionales_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    util_sobre_adicionales_op = models.DecimalField(max_digits=15,
                                                    decimal_places=2,
                                                    null=True,
                                                    blank=True)
    util_sobre_piedras_op = models.DecimalField(max_digits=15,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    # campos adicionales de alianzas
    # talla para hombre y mujeres con su inscripcion
    talla_mujer = models.IntegerField(default=None, blank=True, null=True)
    # talla_mujer = models.ForeignKey(Tallas, on_delete=models.CASCADE, default=None, related_name="tala_mujer")
    inscripcion_mujer = models.CharField(max_length=100, blank=True, null=True)
    piedra_mujer = models.IntegerField(default=None, blank=True, null=True)
    talla_hombre = models.IntegerField(default=None, blank=True, null=True)
    # talla_hombr = models.ForeignKey(Tallas, on_delete=models.CASCADE, default=None, related_name="tala_hombre")
    
    inscripcion_hombre = models.CharField(max_length=100, blank=True, null=True)
    piedra_hombre = models.IntegerField(default=None, blank=True, null=True)
    id_pieza_detalle = models.IntegerField(null=True, blank=True)




    class Meta:
        verbose_name_plural = 'Detalles ordenes'
        ordering = ["-fecha_creacion"]
        # unique_together = (('pais', 'orden', 'item'),)


#modelo de ordenes piedras agregado de la rama master

# class OrdenesPiedras(models.Model):
#     id_orden_piedra = models.AutoField(primary_key=True)
#     orden = models.ForeignKey(OrdenTrabajo,
#                               on_delete=models.CASCADE)
#     piedra = models.ForeignKey(Piedras,
#                                on_delete=models.CASCADE)
#     piedra_detalle = models.ForeignKey(DetallePiedras,
#                                        on_delete=models.CASCADE)
#     cantidad_piedras = models.IntegerField()
#     costo_piedra_taller = models.DecimalField(max_digits=15,
#                                               decimal_places=2)
#     precio_piedra_taller = models.DecimalField(max_digits=15,
#                                                decimal_places=2)
#     prct_utilidad_piedra_op = models.DecimalField(max_digits=6,
#                                                   decimal_places=2,
#                                                   null=True,
#                                                   blank=True)
#     precio_piedra_op = models.DecimalField(max_digits=15,
#                                            decimal_places=2,
#                                            null=True,
#                                            blank=True)
#     subtotal_piedras_taller = models.DecimalField(max_digits=15,
#                                                   decimal_places=2)
#     subtotal_piedras_op = models.DecimalField(max_digits=15,
#                                               decimal_places=2,
#                                               null=True,
#                                               blank=True)


class OrdenesAdicionales(models.Model):
    id_orden_adicional = models.AutoField(primary_key=True)
    orden = models.ForeignKey(OrdenTrabajo,
                              on_delete=models.CASCADE)
    adicional = models.ForeignKey(Adicionales,
                               on_delete=models.CASCADE)
    cantidad_adicionales = models.IntegerField()
    costo_adicional_taller = models.DecimalField(max_digits=15,
                                              decimal_places=2)
    precio_adicional_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2)
    prct_utilidad_adicional_op = models.DecimalField(max_digits=6,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_adicional_op = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    subtotal_adicional_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2)
    subtotal_adicional_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)



class RubrosAsociados(ClaseModelo):
    id_rubro = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    #1: taller, 2: operaciones
    tipo_rubro = models.IntegerField(blank=True, null=True)

    taller_id = models.IntegerField(blank=True, null=True, default=None)
    grupo_id = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(RubrosAsociados, self).save()

    class Meta:
        verbose_name_plural = 'Rubros asociados'
        ordering = ["-fecha_creacion"]
        unique_together = (('usuario_crea', 'descripcion'),)


class OrdenesPiedras(models.Model):
    id_orden_piedra = models.AutoField(primary_key=True)
    orden = models.ForeignKey(OrdenTrabajo,
                              on_delete=models.CASCADE)
    piedra = models.ForeignKey(Piedras,
                               on_delete=models.CASCADE)
    piedra_detalle = models.ForeignKey(DetallePiedras,
                                       on_delete=models.CASCADE)
    cantidad_piedras = models.IntegerField()
    costo_piedra_taller = models.DecimalField(max_digits=15,
                                              decimal_places=2)
    precio_piedra_taller = models.DecimalField(max_digits=15,
                                               decimal_places=2)
    prct_utilidad_piedra_op = models.DecimalField(max_digits=6,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    precio_piedra_op = models.DecimalField(max_digits=15,
                                           decimal_places=2,
                                           null=True,
                                           blank=True)
    subtotal_piedras_taller = models.DecimalField(max_digits=15,
                                                  decimal_places=2)
    subtotal_piedras_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              null=True,
                                              blank=True)
    diseño = models.CharField(max_length=20, null=True, blank=True, default=None)

    def save(self):
        if self.diseño != None:
          self.diseño = self.diseño.upper()
        else:
          self.diseño = None
        super(OrdenesPiedras, self).save()



# class OrdenesAdicionales(models.Model):
#     id_orden_adicional = models.AutoField(primary_key=True)
#     orden = models.ForeignKey(OrdenTrabajo,
#                               on_delete=models.CASCADE)
#     adicional = models.ForeignKey(Adicionales,
#                                on_delete=models.CASCADE)
#     cantidad_adicionales = models.IntegerField()
#     costo_adicional_taller = models.DecimalField(max_digits=15,
#                                               decimal_places=2)
#     precio_adicional_taller = models.DecimalField(max_digits=15,
#                                                decimal_places=2)
#     prct_utilidad_adicional_op = models.DecimalField(max_digits=6,
#                                                   decimal_places=2,
#                                                   null=True,
#                                                   blank=True)
#     precio_adicional_op = models.DecimalField(max_digits=15,
#                                            decimal_places=2,
#                                            null=True,
#                                            blank=True)
#     subtotal_adicional_taller = models.DecimalField(max_digits=15,
#                                                   decimal_places=2)
#     subtotal_adicional_op = models.DecimalField(max_digits=15,
#                                               decimal_places=2,
#                                               null=True,
#                                               blank=True)




class SolicitudRubros(ClaseModelo):
    id_solicitud_rubro = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudTrabajo,
                                  on_delete=models.CASCADE)
    rubro = models.ForeignKey(RubrosAsociados,
                              on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=15,
                                decimal_places=2)

    class Meta:
        unique_together = (('solicitud', 'rubro'),)


class SolicitudesImagenes(ClaseModelo):
    id_solicitud_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='solicitudes_img')
    solicitud = models.ForeignKey(SolicitudTrabajo,
                                  on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)

    # def save(self):
    #     self.imagen = fnImagenes.comprimirImagen(self.imagen)
    #     super(SolicitudesImagenes, self).save()

    class Meta:
        verbose_name_plural = 'SolicitudesImagenes'
        ordering = ["-fecha_creacion"]


class OrdenesImagenes(ClaseModelo):
    id_orden_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='ordenes_img')
    orden = models.ForeignKey(OrdenTrabajo,
                              on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)

    def save(self):
        self.imagen = fnImagenes.comprimirImagen(self.imagen)
        super(OrdenesImagenes, self).save()

    class Meta:
        verbose_name_plural = 'OrdenesImagenes'
        ordering = ["-fecha_creacion"]




class Facturas(ClaseModelo):
    id_factura = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=50)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE)


class DetallesFacturas(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Facturas,
                                on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenTrabajo,
                              on_delete=models.CASCADE)





# signals
def NuevaTransaccion(sender, instance, **kwargs):
    if instance.pais:
        grupo = 'ws_' + str(instance.pais).lower()
    else:
        grupo = 'ws_neutro'
    channel_layer = get_channel_layer()
    print(grupo)
    # print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        grupo,
        {
            'type': 'chat_message',
            'message': 'nuevo registro'
        }
    )


post_save.connect(NuevaTransaccion, sender=OrdenTrabajo)

post_save.connect(NuevaTransaccion, sender=SolicitudTrabajo)




''' Modelo de configuración para los tooltip al admin de operaciones,
    en las diferentes opciones de cargas de documentos
    y estados de las ordenes.
'''

class ConfiguracionTooltipOperaciones(models.Model):

  id_tooltip=models.AutoField(primary_key=True)
  campo_orden = models.CharField(max_length=100)
  texto = models.CharField(max_length=200, help_text="texto de tooltip")
  grupo = models.IntegerField(blank=True, null=True, help_text="grupo_empresarial de tooltip")
  estado = models.BooleanField(default=1, blank=True)
  pais = models.IntegerField(blank=True, null=True, help_text="pais realcionado al tooltip")
  
  def save(self):
    if self.texto != None:
      self.texto = self.texto.capitalize()
    super(ConfiguracionTooltipOperaciones, self).save()



  class Meta:
    # unique_together = (('grupo', 'pais', 'campo_orden'),) 
    permissions = [
      ('permiso_tooltip', 'Permiso para tooltip en Operaciones')
    ]



