from rest_framework import serializers

from .models import DetalleItems, DetallePiedras,\
    Items, Categorias, Colores, Divisiones, \
    ItemsImagenes, Piedras, DetallePiedras, \
    Anchuras, PiezasDetalles, PiezasPiedras


class DetallesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleItems
        fields = '__all__'


class DetallePiedraSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetallePiedras
        fields = '__all__'


class DivisionesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Divisiones
        fields = '__all__'


class CategoriasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorias
        fields = '__all__'


class ColoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colores
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):
    taller_nombre = serializers.CharField(source='taller.nombre')
    cantdetalles = serializers.SerializerMethodField()
    cantcolores = serializers.SerializerMethodField()
    imagen = serializers.SerializerMethodField()
    categoria_descripcion = serializers.\
        CharField(source='categoria.descripcion')
    estado_descripcion = serializers.\
        CharField(source='estado.descripcion')

    class Meta:
        model = Items
        fields = (
            'id_item',
            'sku',
            'descripcion',
            'imagen',
            'taller',
            'taller_nombre',
            'cantdetalles',
            'cantcolores',
            'categoria',
            'categoria_descripcion',
            'fecha_creacion',
            'estado',
            'estado_descripcion',
            )

    def get_cantdetalles(self, obj):
        return obj.num_detalles()

    def get_cantcolores(self, obj):
        return obj.num_colores()

    def get_imagen(self, obj):
        imagen = obj.imagen()
        if imagen:
            return imagen.url
        else:
            return None


class ItemsListaSerializer(serializers.ModelSerializer):
    categoria_descripcion = serializers.\
        CharField(source='categoria.descripcion')
    estado_descripcion = serializers.\
        CharField(source='estado.descripcion')
    taller_nombre = serializers.\
        CharField(source='taller.nombre')

    class Meta:
        model = Items
        fields = (
            'id_item',
            'tipo_catalogo_id',
            'sku',
            'descripcion',
            'categoria',
            'categoria_descripcion',
            'fecha_creacion',
            'estado',
            'estado_descripcion',
            'taller',
            'taller_nombre'
            )


class ItemDetalleOrdenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'


class ItemImagenesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemsImagenes
        fields = '__all__'


class PiedrasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Piedras
        fields = '__all__'


class DetallesPiedraSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetallePiedras
        fields = '__all__'


class AnchurasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Anchuras
        fields = '__all__'


class PiezasDetallesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PiezasDetalles
        fields = '__all__'

class PiezasDetallesPesosSerializer(serializers.ModelSerializer):

    class Meta:
        model = PiezasDetalles
        fields = ['peso', 'id_pieza_detalle']

class PiezasPiedrasItemSerializer(serializers.ModelSerializer):

    sku = serializers.CharField(source='detalle_piedra.piedra.sku')
    descripcion = serializers.CharField(source='detalle_piedra.piedra.descripcion')
    puntos = serializers.CharField(source='detalle_piedra.medida')
    class Meta:
        model = PiezasPiedras
        fields = ['id_pieza_piedra', 'sku', 'descripcion', 'puntos', 'cantidad']
    


class PiezasPiedrasSerializer(serializers.ModelSerializer):
    piedra_descripcion = serializers.\
        CharField(source='detalle_piedra.piedra.descripcion')
    piedra_medida = serializers.\
        DecimalField(
            source='detalle_piedra.medida',
            max_digits=15,
            decimal_places=2
            )
    piedra_costo_taller = serializers.\
        DecimalField(
            source='detalle_piedra.costo_taller',
            max_digits=15,
            decimal_places=2
            )
    piedra_precio_taller = serializers.\
        DecimalField(
            source='detalle_piedra.precio_taller',
            max_digits=15,
            decimal_places=2
            )
    piedra_prct_utilidad = serializers.\
        DecimalField(
            source='detalle_piedra.piedra.prct_utilidad_op',
            max_digits=15,
            decimal_places=2
            )

    class Meta:
        model = PiezasPiedras
        fields = (
            'id_pieza_piedra',
            'detalle_piedra_id',
            'detalle_pieza_id',
            'cantidad',
            'piedra_descripcion',
            'piedra_medida',
            'piedra_costo_taller',
            'piedra_precio_taller',
            'piedra_prct_utilidad'
        )
