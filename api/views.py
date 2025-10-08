from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .service import (
    file_parser as FileService,
    main as MainService,
    db_reader as DBService,
)
from .models import ETLNames


@api_view(["GET"])
def fetch_etl_tables(request: Request, etl_name: str):
    try:
        serializer = MainService.get_etl_tables(etl_name)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ETLNames.DoesNotExist:
        return Response({"message": "etl not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def upload_data_file(request: Request):
    file_path = MainService.store_data_file(request)
    FileService.parse_file.delay(file_path)  # type: ignore

    return Response(
        {"message": "file uploaded successfully"}, status=status.HTTP_201_CREATED
    )

# for reading data from a live database
@api_view(["POST"])
def data_source(request: Request):
    DBService.read_data_from_db(request)

    return Response(
        {"message": "data was read successfully"}, status=status.HTTP_201_CREATED
    )
