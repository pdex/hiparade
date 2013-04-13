from celery.signals import worker_process_init, worker_shutdown
from hiparade.celery import celery
from hiparade.tasks.hipchat import received, Surrogate
from hiparade.xmpp import MucClient
import settings


@worker_process_init.connect
def client_start(signal=None, sender=None):
    hipClient = MucClient(settings.HCHAT_USER, settings.HCHAT_PASS, received, settings.HCHAT_ROOMS, settings.HCHAT_NICK)
    # give the surrogate something to hold on to.
    Surrogate.set(hipClient)
    # kick off keep alive
    hipClient.scheduler.add('keepalive', 60, hipClient.keepalive, repeat=True)
    # kick off the xmpp client
    hipClient.start()

@worker_shutdown.connect
def client_stop(signal=None, sender=None):
    Surrogate.get().stopThePresses()


def main():
    # all of our tasks are instantiated and registered by now.

    # kick off the worker
    celery.start()

if __name__ == '__main__':
    main()
