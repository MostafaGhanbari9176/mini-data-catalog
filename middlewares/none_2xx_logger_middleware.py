import logging
from django.utils import timezone

logger = logging.getLogger("django.request")


class Non2xxLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not (200 <= response.status_code < 300):
            logger.error(
                f"{timezone.now()} {request.method} {request.path} {response.status_code}"
            )

        return response
