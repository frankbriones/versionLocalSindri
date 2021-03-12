from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from bases.models import Estados, ClaseModelo
# from usr.models import Taller
from est.models import Talleres
from ubc.models import Paises
from usr.models import Usuarios
from cfg.models import ConfigGeneral
from prv.models import Proveedores
from est.models import GruposEmpresariales

from fn_compartidas import fnImagenes


class TiposCatalogo(ClaseModelo):
    id_tipo_catalogo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(TiposCatalogo, self).save()

    class Meta:
        verbose_name_plural = 'Tipos catalogo'
        ordering = ["descripcion"]


class UnidadesMedida(ClaseModelo):
    id_unidad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(UnidadesMedida, self).save()

    class Meta:
        verbose_name_plural = 'Unidades Medida'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'simbolo'),)


class ReglasCalcularPrecio(ClaseModelo):
    id_regla = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(ReglasCalcularPrecio, self).save()

    class Meta:
        verbose_name_plural = 'Reglas'
        ordering = ["descripcion"]
        unique_together = (('descripcion',),)


class TiposPrecios(ClaseModelo):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    regla_calculo = models.ForeignKey(
        ReglasCalcularPrecio,
        on_delete=models.CASCADE
    )
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(TiposPrecios, self).save()

    class Meta:
        verbose_name_plural = 'Tipos Precios'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'regla_calculo'),)


class PreciosDefinidos(ClaseModelo):
    id_precio = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    tipo = models.ForeignKey(
        TiposPrecios,
        on_delete=models.CASCADE
    )
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE,
                               default=1)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                default=0)
    precio = models.DecimalField(max_digits=15,
                                 decimal_places=2,
                                 default=0)
    prct_utilidad = models.DecimalField(max_digits=6,
                                        decimal_places=2,
                                        default=0)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(PreciosDefinidos, self).save()

    class Meta:
        verbose_name_plural = 'Precios Definidos'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'grupo_empresarial', 'taller'),)


class Divisiones(ClaseModelo):
    id_division = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    tipo_catalogo = models.ForeignKey(TiposCatalogo,
                                      on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Divisiones, self).save()

    class Meta:
        verbose_name_plural = 'Divisiones'
        ordering = ["descripcion"]
        unique_together = (('taller','tipo_catalogo', 'descripcion'),)


class ManejadorCategorias(models.Manager):
    def obtener_precio_taller(self, id_precio):
        precio = PreciosDefinidos.objects.filter(id_precio=id_precio).first()
        return precio

    def obtener_precio_empresa(self, id_precio):
        precio = PreciosDefinidos.objects.filter(id_precio=id_precio).first()
        return precio


class Categorias(ClaseModelo):
    id_categoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    unidad_medida = models.ForeignKey(UnidadesMedida,
                                      on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    division = models.ForeignKey(Divisiones,
                                 on_delete=models.CASCADE)
    precio_taller_id = models.IntegerField(null=True, blank=True)
    precio_empresa_id = models.IntegerField(null=True, blank=True)
    costo_taller = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    precio_taller = models.DecimalField(max_digits=15,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    prct_utilidad_taller = models.DecimalField(max_digits=6,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    prct_utilidad_empresa = models.DecimalField(max_digits=6,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    precio_empresa = models.DecimalField(max_digits=15,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    permite_solicitud = models.BooleanField(default=False)
    valor_gramo_diferenciado = models.BooleanField(default=False)
    escala_peso = models.BooleanField(default=False)
    parte_interna = models.BooleanField(default=False)
    acabado = models.BooleanField(default=False)
    costo_piedras = models.BooleanField(default=False)
    tiempos_entrega = models.BooleanField(default=False)
    proveedor = models.BooleanField(default=False)
    datos_extra = models.BooleanField(default=False)
    envio_material = models.BooleanField(default=False)
    categoria_alianzas = models.BooleanField(default=False)
    objects = ManejadorCategorias()

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categorias, self).save()

    def precio_taller_obj(self):
        precio = Categorias.objects.\
            obtener_precio_taller(self.precio_taller_id)
        return precio

    def precio_empresa_obj(self):
        precio = Categorias.objects.\
            obtener_precio_empresa(self.precio_empresa_id)
        return precio

    class Meta:
        verbose_name_plural = 'Categorias'
        ordering = ["descripcion"]
        unique_together = (('division', 'descripcion'),)


class ManejadorItems(models.Manager):
    def contar_detalles(self, id_item):
        detalles = DetalleItems.objects.filter(id_item_id=id_item).count()
        return detalles

    def contar_colores(self, id_item):
        colores = ItemsColores.objects.filter(item_id=id_item).count()
        return colores

    def obtener_imagen(self, id_item):
        imagen = ItemsImagenes.objects.filter(item_id=id_item).first()
        return imagen

    def obtener_proveedor(self, id_proveedor):
        proveedor = Proveedores.objects.filter(id=id_proveedor).first()
        return proveedor


class Items(ClaseModelo):
    id_item = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=200)
    tipo_catalogo = models.ForeignKey(TiposCatalogo,
                                      on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias,
                                  on_delete=models.CASCADE)
    costo_taller = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    precio_taller = models.DecimalField(max_digits=15,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    prct_utilidad_taller = models.DecimalField(max_digits=6,
                                               decimal_places=2,
                                               null=True,
                                               blank=True)
    precio_empresa = models.DecimalField(max_digits=15,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    prct_utilidad_empresa = models.DecimalField(max_digits=6,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)
    valor_gramo_dif = models.DecimalField(max_digits=15,
                                          decimal_places=2,
                                          null=True,
                                          blank=True)
    peso_max_dif = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       null=True,
                                       blank=True)
    escala_peso = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    parte_interna = models.CharField(max_length=200,
                                     null=True,
                                     blank=True)
    acabado = models.CharField(max_length=200,
                               null=True,
                               blank=True)
    tiempo_entrega_min = models.IntegerField(null=True,
                                             blank=True)
    tiempo_entrega_max = models.IntegerField(null=True,
                                             blank=True)
    costo_piedras = models.DecimalField(max_digits=15,
                                        decimal_places=2,
                                        null=True,
                                        blank=True,
                                        default=0)
    cantidad_piedras = models.IntegerField(default=0)
    id_proveedor = models.IntegerField(null=True, blank=True)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    datos_extra = models.BooleanField(default=False)
    unidad_medida = models.ForeignKey(UnidadesMedida,
                                      on_delete=models.CASCADE)
    objects = ManejadorItems()

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Items, self).save()

    def num_detalles(self):
        num = Items.objects.contar_detalles(self.id_item)
        return num

    def num_colores(self):
        num_col = Items.objects.contar_colores(self.id_item)
        return num_col

    def imagen(self):
        imagen = Items.objects.obtener_imagen(self.id_item)
        if imagen:
            return imagen.imagen
        else:
            return None

    def proveedor(self):
        if self.id_proveedor:
            proveedor = Items.objects.obtener_proveedor(self.id_proveedor)
        else:
            proveedor = None
        return proveedor

    class Meta:
        verbose_name_plural = 'Items'
        ordering = ["descripcion"]
        unique_together = (('sku', 'taller'),)


class ItemsImagenes(ClaseModelo):
    id_item_imagen = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='items/')
    item = models.ForeignKey(Items,
                             on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)

    def save(self):
        self.imagen = fnImagenes.comprimirImagen(self.imagen)
        super(ItemsImagenes, self).save()

    class Meta:
        verbose_name_plural = 'ItemsImagenes'
        ordering = ["-fecha_creacion"]


class Colores(ClaseModelo):
    id_color = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)
    costo_adicional_ta = models.DecimalField(max_digits=15,
                                          decimal_places=2)
    precio_adicional_ta = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              default=0)
    precio_adicional_op = models.DecimalField(max_digits=15,
                                              decimal_places=2,
                                              default=0)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Colores, self).save()

    class Meta:
        verbose_name_plural = 'Colores'
        ordering = ["descripcion"]
        unique_together = (('taller', 'descripcion'),)


class ItemsColores(ClaseModelo):
    id_item_color = models.AutoField(primary_key=True)
    item = models.ForeignKey(Items,
                             on_delete=models.CASCADE)
    color = models.ForeignKey(Colores,
                              on_delete=models.CASCADE)

    class Meta:
        unique_together = (('item', 'color'),)


class EstandarTallas(ClaseModelo):
    id_estandar = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(EstandarTallas, self).save()

    class Meta:
        verbose_name_plural = 'EstandarTallas'
        ordering = ["descripcion"]


class Tallas(ClaseModelo):
    id_talla = models.AutoField(primary_key=True)
    diametro = models.DecimalField(max_digits=10, decimal_places=2)
    talla = models.DecimalField(max_digits=3, decimal_places=1)
    estandar = models.ForeignKey(EstandarTallas, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{} : {}'.format(self.talla, self.estandar)

    class Meta:
        verbose_name_plural = 'Tallas'
        ordering = ["talla"]
        unique_together = (('talla', 'estandar', 'taller'),)


class DetalleItems(ClaseModelo):
    id_detalle_item = models.AutoField(primary_key=True)
    id_item = models.ForeignKey(Items,
                                on_delete=models.CASCADE)
    medida = models.DecimalField(max_digits=5,
                                 decimal_places=2)
    estandar = models.CharField(max_length=30,
                                null=True,
                                blank=True)
    peso_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    peso_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_piedras = models.IntegerField(null=True, default=0)
    costo_piedras = models.DecimalField(max_digits=15,
                                        decimal_places=2,
                                        null=True,
                                        blank=True,
                                        default=0)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    class Meta:
        verbose_name_plural = 'Detalles items'
        ordering = ["medida"]
        unique_together = (('id_item', 'medida'),)


class Adicionales(ClaseModelo):
    id_adicional = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=10)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    imagen = models.ImageField(null=True, upload_to='adicionales/')

    # costo = models.DecimalField(max_digits=15, decimal_places=2)
    # utilidad_sobre_adicionales = models.DecimalField(max_digits=5,
    #                                                  decimal_places=2)
    costo_taller = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    precio_taller = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    utilidad_operaciones = models.DecimalField(max_digits=5,
                                                     decimal_places=2, default=0)

    pais = models.ForeignKey(Paises, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        # self.imagen = self.comprimirImagen(self.imagen)
        super(Adicionales, self).save()

    def comprimirImagen(self, imagen):
        imagenTemporal = Image.open(imagen).convert('RGBA')
        fondo = Image.new('RGBA', imagenTemporal.size, (255, 255, 255))
        outputIoStream = BytesIO()
        imagenTemporalModificada = imagenTemporal.resize((500, 500))
        imagenTemporal = Image.alpha_composite(fondo, imagenTemporal)
        imagenTemporal = imagenTemporal.convert('RGB')
        imagenTemporal.save(
            outputIoStream,
            format='JPEG',
            quality=85
        )
        outputIoStream.seek(0)
        imagen = InMemoryUploadedFile(
            outputIoStream,
            'ImageField',
            "%s.jpg" % imagen.name.split('.')[0],
            'image/jpeg',
            sys.getsizeof(outputIoStream),
            None
        )
        return imagen

    class Meta:
        verbose_name_plural = 'Adicionales'
        ordering = ["descripcion"]
        unique_together = (('sku'),)


class CategoriaAdicionales(ClaseModelo):
    id_categoria_adicional = models.AutoField(primary_key=True)
    adicional = models.ForeignKey(Adicionales, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'CategoriaAdicional'
        ordering = ["-fecha_creacion"]
        unique_together = (('adicional', 'categoria'),)


class Piedras(ClaseModelo):
    id_piedra = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=10)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    prct_utilidad_op = models.DecimalField(max_digits=15,
                                                 decimal_places=2,
                                                 null=True,
                                                 default=0)
    imagen = models.ImageField(null=True, upload_to='piedras/')
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        # self.imagen = self.comprimirImagen(self.imagen)
        super(Piedras, self).save()

    def comprimirImagen(self, imagen):
        imagenTemporal = Image.open(imagen).convert('RGBA')
        fondo = Image.new('RGBA', imagenTemporal.size, (255, 255, 255))
        outputIoStream = BytesIO()
        imagenTemporalModificada = imagenTemporal.resize((500, 500))
        imagenTemporal = Image.alpha_composite(fondo, imagenTemporal)
        imagenTemporal = imagenTemporal.convert('RGB')
        imagenTemporal.save(
            outputIoStream,
            format='JPEG',
            quality=85
        )
        outputIoStream.seek(0)
        imagen = InMemoryUploadedFile(
            outputIoStream,
            'ImageField',
            "%s.jpg" % imagen.name.split('.')[0],
            'image/jpeg',
            sys.getsizeof(outputIoStream),
            None
        )
        return imagen

    class Meta:
        verbose_name_plural = 'Piedras'
        ordering = ["descripcion"]
        unique_together = (('sku'),)


class DetallePiedras(ClaseModelo):
    id_detalle_piedra = models.AutoField(primary_key=True)
    piedra = models.ForeignKey(Piedras, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    medida = models.DecimalField(max_digits=10, decimal_places=2)
    costo_taller = models.DecimalField(max_digits=15, decimal_places=2)
    precio_taller = models.DecimalField(max_digits=15, decimal_places=2)
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    class Meta:
        verbose_name_plural = 'DetallePiedras'
        ordering = ["-fecha_creacion"]
        unique_together = (('piedra', 'medida'),)


class CategoriaPiedras(ClaseModelo):
    id_categoria_piedra = models.AutoField(primary_key=True)
    piedra = models.ForeignKey(Piedras, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'CategoriaPiedras'
        ordering = ["-fecha_creacion"]
        unique_together = (('piedra', 'categoria'),)


class ConteoCotizaciones(models.Model):
    id_cotizacion = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    tipo = models.IntegerField()  # 1: cliente, 2: interno


class Acabados(ClaseModelo):
    id_acabado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Acabados, self).save()

    class Meta:
        verbose_name_plural = 'Acabados'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'taller'),)


class PartesInternas(ClaseModelo):
    id_parte_interna = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(PartesInternas, self).save()

    class Meta:
        verbose_name_plural = 'Partes Internas'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'taller'),)


class Anchuras(ClaseModelo):
    id_anchura = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Anchuras, self).save()

    class Meta:
        verbose_name_plural = 'Anchuras'
        ordering = ["descripcion"]
        unique_together = (('descripcion', 'taller'),)


class Piezas(ClaseModelo):
    id_pieza = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=20)
    talla_minima_a = models.IntegerField()
    talla_maxima_a = models.IntegerField()
    talla_minima_b = models.IntegerField()
    talla_maxima_b = models.IntegerField()
    item = models.ForeignKey(
        Items,
        on_delete=models.CASCADE
    )
    taller = models.ForeignKey(Talleres, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    longitud_inscripcion = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Piezas'
        ordering = ["sku"]
        unique_together = (('sku', 'taller'),)


class PiezasDetalles(ClaseModelo):
    id_pieza_detalle = models.AutoField(primary_key=True)
    parte_interna = models.ForeignKey(
        PartesInternas,
        on_delete=models.CASCADE
    )
    anchura = models.ForeignKey(
        Anchuras,
        on_delete=models.CASCADE
    )
    pieza = models.ForeignKey(
        Piezas,
        on_delete=models.CASCADE
    )
    peso = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)

    class Meta:
        verbose_name_plural = 'PiezasDetalles'
        ordering = ["id_pieza_detalle"]
        unique_together = (('pieza', 'parte_interna', 'anchura', 'peso'),)


class PiezasAcabados(ClaseModelo):
    id_pieza_acabado = models.AutoField(primary_key=True)
    pieza = models.ForeignKey(
        Piezas,
        on_delete=models.CASCADE
    )
    acabado = models.ForeignKey(
        Acabados,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'PiezasAcabados'
        unique_together = (('pieza', 'acabado'),)


class PiezasPiedras(ClaseModelo):
    id_pieza_piedra = models.AutoField(primary_key=True)
    detalle_pieza = models.ForeignKey(
        PiezasDetalles,
        on_delete=models.CASCADE
    )
    detalle_piedra = models.ForeignKey(
        DetallePiedras,
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'PiezasPiedras'
        unique_together = (('detalle_pieza', 'detalle_piedra'),)



