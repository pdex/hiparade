from celery import Task


class XmppTask(Task):
    abstract = True

    client_surrogate = None

    @property
    def client(self):
        return self.client_surrogate.get()
