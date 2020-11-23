from .tasks import automatic_approve, process


def approve_on_create(sender, instance, created, **kwargs) -> bool:
    if not created:
        return False
    
    instance.automatic_approve()

    return True
