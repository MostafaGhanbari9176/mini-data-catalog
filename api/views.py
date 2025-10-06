from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .service import main as MainService
from .models import ETLNames


class FetchETLTables(APIView):
    def get(self, request, etl_name: str):
        try:
            serializer = MainService.get_etl_tables(etl_name)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ETLNames.DoesNotExist:
            return Response(
                {"message": "etl not found"}, status=status.HTTP_404_NOT_FOUND
            )
