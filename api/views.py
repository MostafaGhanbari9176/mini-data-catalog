from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .service import file_parser as FileService, main as MainService
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


class UploadDataFile(APIView):
    def post(self, request: Request):
        file_path = MainService.store_data_file(request)
        
        FileService.parse_file(file_path)
        
        return Response(
            {"message": "file uploaded successfully"}, status=status.HTTP_201_CREATED
        )
