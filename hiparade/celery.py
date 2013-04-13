from __future__ import absolute_import

from celery import Celery

celery = Celery(
    backend='mongodb://localhost/',
    broker='amqp://hiparade:hiparade@localhost/hiparade',
    include=[
        'hiparade.tasks.hipchat',
        'hiparade.tasks.partychat'
    ],
)

celery.conf.update(
    CELERY_ROUTES={
        'hiparade.tasks.hipchat.received': {'queue': 'hipchat'},
        'hiparade.tasks.hipchat.send': {'queue': 'hipchat'},
        'hiparade.tasks.partychat.received': {'queue': 'partychat'},
        'hiparade.tasks.partychat.send': {'queue': 'partychat'},
    }
)
