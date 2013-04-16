from hiparade.celery import celery
from hiparade.tasks.xmpptask import XmppTask

class Surrogate:
    client = None

    @staticmethod
    def get():
        return Surrogate.client

    @staticmethod
    def set(value):
        Surrogate.client = value

@celery.task
def received(room, msg):
    celery.send_task('hiparade.tasks.partychat.send', (room, msg))

@celery.task(base=XmppTask, client_surrogate=Surrogate)
def send(room, msg):
    send.client.send_to_room(room, msg)
