from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .services import auth as AccountService


@api_view(["POST"])
@permission_classes([AllowAny])
def log_in(request: Request):
    AccountService.log_in(request)
    return Response({"message": "otp was sent"}, status=status.HTTP_202_ACCEPTED)

@api_view(["POST"])
@permission_classes([AllowAny])
def log_in_confirm(request: Request):
    token = AccountService.log_in_confirm(request)
    return Response(token, status=status.HTTP_200_OK)
