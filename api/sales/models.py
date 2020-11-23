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
        """Trigger to automatically approves sales from VIP resellers"""
        cpf = re.sub(r"\D", "", self.reseller.cpf)

        if cpf not in settings.VIP_RESELLERS:
            return False

        self.status = Sale.APPROVED
        self.save(update_fields=["status"])

        logger.info(f"sale {self} was automatically approved")

        return True

    def process(self) -> bool:
        """Calculate cashback based on sum of sales from month"""

        # select all sales from related sale date
        # ---------------------------------------------------------------------
        sales = Sale.objects.filter(
            reseller=self.reseller,
            date__month=self.date.month,
            date__year=self.date.year
        )

        # create a "panorama" from month with total of sales and current level
        # ---------------------------------------------------------------------
        resume = sales.aggregate(
            total=models.Sum("value"),
            percentage=models.Case(
                models.When(total__lt=1000, then=Sale.TEN),
                models.When(total__lt=1500, then=Sale.FIFTEEN),
                default=Sale.TWENTY,
                output_field=models.DecimalField(),
            ),
            current_percentage=models.Max("percentage")
        )
        pct = resume.get("percentage")
        current_pct = resume.get("current_percentage")
        change_level = pct != current_pct

        # if the range is not changed just current sale is evaluated
        # ---------------------------------------------------------------------
        if not change_level:
            sales = sales.filter(id=self.id)

        sales.update(percentage=pct, cashback=(models.F("value") * pct) / 100)

        # send to log a "operation report"
        # ---------------------------------------------------------------------
        codes = sales.values("code", "percentage", "cashback")
        logger.info(f"Cashback is (re) calculated to {codes}")

        return True
