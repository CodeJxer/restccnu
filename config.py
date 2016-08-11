# coding: utf-8

import os
from datetime import timedelta


class Config(object):

    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME') or 'ccnustatic'
    QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN') or 'oao7x1n3m.bkt.clouddn.com'

    CELERY_BROKER_URL = 'redis://localhost:6384/2'
    CELERY_RESULT_BACKEND = 'redis://localhost:6384/2'
    CELERYBEAT_SCHEDULE = {
            'restart_redis_every_86400s': {
                'task': 'cute_board_spider',
                'schedule': timedelta(seconds=86400)
            },
    }

    XNM = 2015
    XQM = 12


config = {
    'develop': Config,
    'test': Config,

    'default': Config
}
