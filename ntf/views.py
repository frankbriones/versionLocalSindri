from django.shortcuts import render

from .models import Notificaciones
import json

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NotificacionesSerializer
from usr.models import UsuariosTiendas, Usuarios
from est.models import Tiendas


class ObtenerNotificacionesUsuarioView(APIView):
    def get(self, request, id_usuario, limite):
        usuario = Usuarios.objects.filter(id=id_usuario).first()
        tiendas = UsuariosTiendas.objects.\
            filter(
                usuario=usuario
                ).\
            values('tienda_id')


        if limite > 1:
            notificaciones = Notificaciones.objects.\
                filter(vista=False, tienda__in=tiendas).\
                order_by('-fecha_creacion')[:limite]
        else:
            notificaciones = Notificaciones.objects.\
                filter(tienda__in=tiendas).\
                order_by('-fecha_creacion')
        data = NotificacionesSerializer(notificaciones, many=True).data
        return Response(data)


class ObtenerNotificacionesTallerView(APIView):
    def get(self, request, id_taller, limite):
        if limite > 1:
            notificaciones = Notificaciones.objects.\
                filter(taller_id=id_taller).\
                filter(tipo_notificacion='2').\
                order_by('-fecha_creacion')[:limite]

        else:
            notificaciones = Notificaciones.objects.\
                filter(taller_id=id_taller).\
                order_by('-fecha_creacion')

        data = NotificacionesSerializer(notificaciones, many=True).data
        return Response(data)


class PrimeraNotificacionesUsuarioView(APIView):

    def get(self, request, id_usuario):
        usuario = Usuarios.objects.filter(id=id_usuario).first()
        tiendas = UsuariosTiendas.objects.\
            filter(
                usuario=usuario
                ).\
            values('tienda_id')

        notificaciones = (
            Notificaciones.objects.
            filter(
                vista=False,
                tipo_notificacion=1,
                tienda__in=tiendas
                ).\

            order_by('fecha_creacion') |
            Notificaciones.objects.
            filter(
                vista=False,
                tipo_notificacion=1,
                estado__descripcion='ESPERA DE EVALUACION',
                tienda__in=tiendas

                ).\
            order_by('fecha_creacion') |
            Notificaciones.objects.
            filter(
                vista=False,
                estado__descripcion='RECHAZADO TALLER',
                tipo_notificacion=1,
                tienda__in=tiendas
                ).
            order_by('fecha_creacion'))[:1]
        data = NotificacionesSerializer(notificaciones, many=True).data
        print(data)
        return Response(data)


class PrimeraNotificacionesTallerView(APIView):
    def get(self, request, id_taller):
        id_usuario = self.request.user.id
        notificaciones = (
            Notificaciones.objects.
            filter(
                taller_id=id_taller,
                tipo_notificacion=2,
                vista=False,
                estado__descripcion='ESPERA COTIZACION TALLER'
                ).
            order_by('fecha_creacion') |
            Notificaciones.objects.
            filter(
                taller_id=id_taller,
                vista=True,
                tipo_notificacion=2,
                estado__descripcion='ESPERA COTIZACION TALLER'
                ).
            order_by('fecha_creacion') |
            Notificaciones.objects.
            filter(
                taller_id=id_taller,
                vista=False,
                tipo_notificacion=2,
                ).
            order_by('fecha_creacion'))[:1]
        data = NotificacionesSerializer(notificaciones, many=True).data
        print(data)
        return Response(data)


class ActualizarNotificacionView(APIView):

    def post(self, request, pk=None):
        notificacion = Notificaciones.objects.\
            filter(id_notificacion=pk).first()
        if notificacion:
            notificacion.vista = True
            notificacion.save()
            return Response('ok', status=200)
        else:
            return Response('error', status=400)
