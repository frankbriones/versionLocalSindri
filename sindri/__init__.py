# import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()
# Celery
from .celery import app as celery_app
