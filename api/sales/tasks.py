import logging

from celery import shared_task
from .models import Sale

logger = logging.getLogger(__name__)


@shared_task
def automatic_approve(sale_id: int) -> str:
    sale = Sale.objects.get(pk=sale_id)
    sale.automatic_approve()

    message = f"sale {sale} enqueued to automatic approval"

    logger.info(message)

    return message


@shared_task
def process(sale_id: int) -> str:
    sale = Sale.objects.get(pk=sale_id)
    sale.process()

    message = f"sale {sale} enqueued to be processed"

    logger.info(message)

    return message
