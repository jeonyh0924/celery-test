from __future__ import absolute_import, unicode_literals

import os
import uuid
from time import sleep

from celery import Celery, shared_task
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', broker='redis://localhost/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
#
# @app.task(bind=True)
# def new_task(self):
#     print('Request: {0!r}'.format(self.request))

@shared_task
def create_users_async(user_count):
    User = get_user_model()
    for i in range(user_count):
        a = 0 / 0
        sleep(3)
        User.objects.create(username=f'user_{i}')

        """
        워커가 죽는 이유를 알기 위해서 센트리의 역할이 필요하다.
        센트리에서  셀러리를 연결하기 위해서는 별도의 설정이 필요하다.
        
        """
