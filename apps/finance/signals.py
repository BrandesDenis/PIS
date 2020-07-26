from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

from apps.finance.models import DayReport, FinanceRegister, FinanceDocumentRow


@receiver(post_save, sender='finance.DayReport')
def calculate_balance_post_save(sender,
                                instance: DayReport,
                                *args,
                                **kwargs) -> None:
    if instance.rows_added:
        FinanceRegister.calculate_month_balance(instance.date)


@receiver(post_delete, sender='finance.DayReport')
def calculate_balance_post_delete(sender,
                                  instance: DayReport,
                                  *args,
                                  **kwargs) -> None:

    FinanceRegister.calculate_month_balance(instance.date)


@receiver(pre_save, sender='finance.DayReportRow')
@receiver(pre_save, sender='finance.BudgetRow')
def check_description(sender,
                      instance: FinanceDocumentRow,
                      *args,
                      **kwargs) -> None:
    if instance.fin_object.need_description and not instance.description:
        raise ValueError(f'Для {instance.fin_object} необходимо указывать описание!')
