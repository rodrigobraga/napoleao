# coding: utf-8

from django.utils import timezone

from faker import Faker
from model_bakery.recipe import Recipe, foreign_key

from .models import Sale

fake = Faker("pt_BR")

sale = Recipe(
    Sale,
    code=fake.ean,
    value=700,
    date=timezone.localtime,
    reseller=foreign_key("users.user"),
    status=Sale.IN_VALIDATION,
    percentage=10,
    cashback=70
)
