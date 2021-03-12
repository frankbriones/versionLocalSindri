from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from bases.models import Estados, ClaseModelo
from ubc.models import Paises, Ciudades,Localidades
from est.models import GruposEmpresariales, Talleres, Tiendas


class TipoUsuarios(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(TipoUsuarios, self).save()

    class Meta:
        verbose_name_plural = 'Tipos usuario'


# class Taller(ClaseModelo):
#     pais = models.ForeignKey(Paises,
#                              on_delete=models.CASCADE)
#     nombre = models.CharField(max_length=200)
#     costo_gramo_fabricacion = models.DecimalField(max_digits=15,
#                                                   decimal_places=2,
#                                                   default=0.00)
#     precio_gramo_fabricacion = models.DecimalField(max_digits=15,
#                                                    decimal_places=2,
#                                                    default=0.00)
#     costo_gramo_base = models.DecimalField(max_digits=15,
#                                            decimal_places=2,
#                                            default=0.00)
#     precio_gramo_base = models.DecimalField(max_digits=15,
#                                             decimal_places=2,
#                                             default=0.00)
#     utilidad_sobre_fabricacion = models.DecimalField(max_digits=5,
#                                                      decimal_places=2,
#                                                      default=0.00)
#     utilidad_sobre_base = models.DecimalField(max_digits=5,
#                                               decimal_places=2,
#                                               default=0.00)
#     utilidad_sobre_piedras = models.DecimalField(max_digits=5,
#                                                  decimal_places=2,
#                                                  default=0.00)
#     utilidad_sobre_adicionales = models.DecimalField(max_digits=5,
#                                                      decimal_places=2,
#                                                      default=0.00)
#     prct_impuestos = models.DecimalField(max_digits=5,
#                                          decimal_places=2,
#                                          default=0)
#     tmp_resp_sol = models.IntegerField(default=5)
#     escala_peso = models.DecimalField(max_digits=15,
#                                       decimal_places=2,
#                                       default=0.10)
#     estandar_tallas = models.IntegerField(default=1)
#     configurado = models.BooleanField(default=False)
#     externo = models.BooleanField(default=False)
#     secuencia_ordenes = models.IntegerField(default=1)
#     secuencia_solicitudes = models.IntegerField(default=1)
#     prioridad = models.IntegerField()
#     logotipo = models.ImageField(upload_to='logotalleres/',
#                                  null=True,
#                                  blank=True)
#     recalcular_precio = models.BooleanField(default=False)
#     cargar_img_fin_trabajo = models.BooleanField(default=False)
#     tipo_precio_predefinido = models.IntegerField(null=True,
#                                                   blank=True)

#     def __str__(self):
#         return '{}'.format(self.nombre)

#     def save(self):
#         self.nombre = self.nombre.upper()
#         super(Taller, self).save()

#     class Meta:
#         verbose_name_plural = 'Talleres'
#         ordering = ["nombre"]
#         unique_together = (('pais', 'nombre'),)


class Roles(ClaseModelo):
    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados,
                               on_delete=models.CASCADE,
                               default=1)
    tipo_usuario = models.ForeignKey(TipoUsuarios,
                                     on_delete=models.CASCADE)
    primario = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    zonal = models.BooleanField(default=False)
    grupo = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              default=1)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Roles, self).save()

    class Meta:
        verbose_name_plural = 'Roles'
        ordering = ["-fecha_creacion"]
        # unique_together = (('pais', 'tipo_usuario', 'descripcion'),)


class RolesGruposEmpresariales(models.Model):
    id_rol_grupo_empresarial = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Roles,
                            on_delete=models.CASCADE)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)


class RolesTalleres(models.Model):
    id_rol_taller = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Roles,
                            on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)


class Usuarios(AbstractUser):
    tipo_usuario = models.ForeignKey(TipoUsuarios,
                                     on_delete=models.CASCADE,
                                     default=1)
    rol = models.ForeignKey(Roles,
                            on_delete=models.CASCADE,
                            default=1)
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE,
                             default=1)
    telefono = models.CharField(max_length=20, null=True)
    img_perfil = models.ImageField(upload_to='perfil_img',
                                   null=True,
                                   blank=True)

    zona = models.IntegerField(default=None, null=True)

    usuario_telegram = models.CharField(max_length=50, null=True)

    ver_notificaciones = models.BooleanField(default=True)


    def taller(self):
        registro = UsuariosTalleres.objects.\
            filter(usuario_id=self.id).first()
        if registro:
            return registro.taller
        else:
            return None

    def grupo_empresarial(self):
        registro = UsuariosGruposEmpresariales.objects.\
            filter(usuario_id=self.id).first()
        if registro:
            return registro.grupo_empresarial
        else:
            return None

    def tienda_usuario(self):
        registro = UsuariosTiendas.objects.\
            filter(usuario_id=self.id).count()
        
        if registro:
            return registro
        else:
            return None
    
    def tienda(self):
        registro = UsuariosTiendas.objects.\
            filter(usuario_id=self.id).first()
        
        if registro:
            return registro
        else:
            return None

    class Meta:
        unique_together = (('pais', 'username'),)


class UsuariosGruposEmpresariales(models.Model):
    id_usuario_grupo_empresarial = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios,
                                on_delete=models.CASCADE)
    grupo_empresarial = models.ForeignKey(GruposEmpresariales,
                                          on_delete=models.CASCADE)


class UsuariosTalleres(models.Model):
    id_usuario_taller = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios,
                                on_delete=models.CASCADE)
    taller = models.ForeignKey(Talleres,
                               on_delete=models.CASCADE)


class UsuariosTiendas(models.Model):
    id_usuario_tiendas = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios,
                                on_delete=models.CASCADE)

    tienda = models.ForeignKey(Tiendas,
                               on_delete=models.CASCADE)


# Modelos para asignacion de permisos

class UsuariosGrupos(models.Model):
    usuarios = models.ForeignKey(Usuarios, models.DO_NOTHING)
    group = models.ForeignKey(Group, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usr_usuarios_groups'
        unique_together = (('usuarios', 'group'),)


class GruposPermisos(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
