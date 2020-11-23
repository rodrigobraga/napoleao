from faker import Faker
from model_bakery.recipe import Recipe

from .models import User

fake = Faker('pt_BR')

user = Recipe(
    User,
    username=fake.user_name,
    first_name=fake.first_name,
    last_name=fake.last_name,
    email=fake.email,
    cpf=fake.cpf,
    is_superuser=False,
    is_staff=False,
)
