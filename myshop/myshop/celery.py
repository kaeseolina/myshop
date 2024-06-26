from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings







os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



# устанавливаем модуль настроек Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

# Используем строку для задания настроек Celery.
# Используем 'CELERY' в качестве префикса всех Celery-настроек.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружаем задачи из всех зарегистрированных приложений Django.
app.autodiscover_tasks()