from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from usr.models import Usuarios


@shared_task
def CrearTareaEnvioReporte(usuario):
    usuario = Usuarios.objects.filter(username=usuario).first()
    zona_horaria = usuario.pais.zona_horaria
    nombre_tarea = 'envio_reporte_' + str(usuario.id) + \
        '_' + str(usuario.pais_id)
    periodo, _ = CrontabSchedule.objects.get_or_create(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    PeriodicTask.objects.create(
        crontab=periodo,
        name='enviar_reporte_' + usuario,
        task='trn.tasks.enviarReporte',
    )
