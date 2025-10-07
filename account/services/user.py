from django.contrib.auth import get_user_model


def create_user_nx(email):
    User = get_user_model()
    user, created = User.objects.get_or_create(email=email)

    if created:
        user.set_unusable_password()
        user.is_active = True
        user.save()

    return user


def get_user(email):
    return get_user_model().objects.get(email=email)
