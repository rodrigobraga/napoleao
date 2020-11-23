def approve_on_create(sender, instance, created, **kwargs) -> bool:
    if not created:
        return False
    
    instance.automatic_approve()

    return True


def process_on_change_handler(sender, instance, created, **kwargs) -> bool:
    """Calculate the cashback when a sale is changed or created"""
    instance.process()

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

    sale.process()

    return True 
