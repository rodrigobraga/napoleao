import logging
import re
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

logger = logging.getLogger(__name__)


class Sale(models.Model):
    IN_VALIDATION = "in_validation"
    REJECTED = "rejected"
    APPROVED = "approved"
    STATUS = (
        (IN_VALIDATION, "In Validation"),
        (REJECTED, "Rejected"),
        (APPROVED, "Approved"),
    )

    TEN = 10
    FIFTEEN = 15
    TWENTY = 20
    PERCENTAGES = (
        (TEN, "10%"),
        (FIFTEEN, "15%"),
        (TWENTY, "20%")
    )

    identifier = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    code = models.CharField(max_length=255, unique=True)
    value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    date = models.DateTimeField()
    reseller = models.ForeignKey(
        "users.User",
        related_name="sales",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=255, 
        choices=STATUS,
        default=IN_VALIDATION
    )
    percentage = models.PositiveSmallIntegerField(
        choices=PERCENTAGES,
        default=TEN,
        help_text="percentage applied to get cashback"
    )
    cashback = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["date"], name="date_idx"),
            models.Index(fields=["status"], name="status_idx"),
        ]
    
    def __str__(self) -> str:
        return self.code
    
    def automatic_approve(self) -> bool:
        cpf = re.sub(r"\D", "", self.reseller.cpf)

        if cpf not in settings.VIP_RESELLERS:
            return False

        self.status = Sale.APPROVED
        self.save(update_fields=["status"])

        logger.info(f"sale {self} was automatically approved")

        return True

