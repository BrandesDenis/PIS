from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from apps.finance.models import DayReport, FinanceRegister


@receiver(post_save, sender='finance.DayReport')
def _calculate_balance_post_save(sender,
                                 instance: DayReport,
                                 *args,
                                 **kwargs) -> None:
    if instance.rows_added:
        FinanceRegister.calculate_month_balance(instance.date)


@receiver(post_delete, sender='finance.DayReport')
def _calculate_balance_post_delete(sender,
                                   instance: DayReport,
                                   *args,
                                   **kwargs) -> None:

    FinanceRegister.calculate_month_balance(instance.date)
