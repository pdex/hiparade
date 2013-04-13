from celery.signals import worker_process_init, worker_shutdown
from hiparade.celery import celery
from hiparade.tasks.partychat import received, Surrogate
from hiparade.xmpp import Client
import settings


@worker_process_init.connect
def client_start(signal=None, sender=None):
    partyClient = Client(settings.GCHAT_USER, settings.GCHAT_PASS, received, settings.GCHAT_ROOMS)
    # give the surrogate something to hold on to.
    Surrogate.set(partyClient)
    # kick off the xmpp client
    partyClient.start()

@worker_shutdown.connect
def client_stop(signal=None, sender=None):
    Surrogate.get().stopThePresses()


def main():
    # all of our tasks are instantiated and registered by now.

    # kick off the worker
    celery.start()

if __name__ == '__main__':
    main()
