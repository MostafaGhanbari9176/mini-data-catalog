from rest_framework.exceptions import ValidationError, status
from rest_framework.request import Request
from account.serializer import AccountValidationSerializer, AccountSerializer
import account.services.user as UserService
from account.models import OTP
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt import tokens


def log_in(request: Request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email: str = serializer.validated_data["email"]  # type: ignore

    send_otp(email)


def log_in_confirm(request: Request):
    serializer = AccountValidationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email: str = serializer.validated_data["email"]  # type: ignore
    otp: str = serializer.validated_data["otp"]  # type: ignore
    if not otp_is_valid(email, otp):
        raise ValidationError({"error":"otp is not valid or expired"})

    # creating user if user not exists
    UserService.create_user_nx(email)

    return generate_token_pair(email)


def otp_is_valid(email, otp) -> bool:
    otp_object = (
        OTP.objects.filter(email=email, otp=otp, invalidate=False)
        .order_by("-updated_at")
        .first()
    )

    if otp_object is None:
        return False

    now = timezone.now()

    valid = now < otp_object.updated_at + timedelta(minutes=2)

    if valid:
        otp_object.invalidate = True
        otp_object.save()

    return valid


def send_otp(email):
    if otp_is_limited(email):
        raise ValidationError({"error": "OTP generating Limitation"})

    otp = generate_otp()

    store_otp(email, otp)

    print(f"email:{email}, otp:{otp}")


def otp_is_limited(email) -> bool:
    last_send = OTP.objects.filter(email=email).order_by("-updated_at").first()
    if last_send is None:
        return False

    now = timezone.now()

    return now < last_send.updated_at + timedelta(minutes=2)


def store_otp(email: str, otp: str) -> None:
    otp_object = OTP.objects.filter(email=email).first()

    if otp_object is None:
        otp_object = OTP(email=email, otp=otp)
    else:
        otp_object.otp = otp
        otp_object.invalidate = False

    otp_object.save()


def generate_otp() -> str:
    return "123456"


def generate_token_pair(email) -> dict[str, str]:
    user = UserService.get_user(email)
    if user is None:
        raise ValidationError({"error":"something is go wrong"})

    refresh = tokens.RefreshToken.for_user(user)  # type: ignore

    return {"refresh": str(refresh), "access": str(refresh.access_token)}
