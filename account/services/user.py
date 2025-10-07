from account.models import User
from django.utils import timezone


def emailIsExists(email) -> bool:
    return User.objects.filter(email=email).exists()


def create_user_nx(email):
    User.objects.get_or_create(email=email)


def get_user(email) -> User | None:
    return User.objects.filter(email=email).first()
