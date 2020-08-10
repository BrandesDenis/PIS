from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.tasks.models import Task
from apps.core.dates import today


@receiver(pre_save, sender=Task)
def check_description(sender,
                      instance: Task,
                      *args,
                      **kwargs) -> None:
    if instance.status != instance.TaskStatuses.IN_PROGRESS:
        instance.end = min(today(), instance.end)
