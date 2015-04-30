from django.db import models


class QueuedActivityModelManager(models.Manager):
    def contribute_to_class(self, model, name):
        super(QueuedActivityModelManager, self).contribute_to_class(model, name)

        self._bind_flush_signal(model)

    def _bind_flush_signal(self, model):
        models.signals.post_save.connect(send_activity_to_queue, model)


def send_activity_to_queue(sender, **kwargs):
    instance = kwargs.pop('instance', False)
    print instance