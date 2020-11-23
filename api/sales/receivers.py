import logging

from .tasks import automatic_approve, process

logger = logging.getLogger(__name__)

def approve_on_create_handler(sender, instance, created, **kwargs) -> bool:
    if not created:
        return False

    automatic_approve.delay(sale_id=instance.id)

    logger.info(f"sale {instance} enqueued to check automatic approval")

    return True


def process_on_change_handler(sender, instance, created, **kwargs) -> bool:
    """Calculate the cashback when a sale is changed or created"""
    process.delay(sale_id=instance.id)

    logger.info(f"sale {instance} enqueued to be processed")

    return True


def process_on_delete_handler(sender, instance, **kwargs) -> bool:
    """Recalculate cash back when a sale is removed"""
    sales = sender.objects.filter(
        reseller=instance.reseller,
        date__month=instance.date.month,
        date__year=instance.date.year
    )

    if not sales.exists():
        return False

    sale = sales.first()

    process.delay(sale_id=sale.id)

    logger.info(f"sale {instance} was removed, the remaining are be evaluated")
    
    return True 
