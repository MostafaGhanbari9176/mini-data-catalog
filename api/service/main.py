import uuid
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from api.serializer import ETLTablesSerializer
from api.models import ETLNames
from django.core.files.uploadedfile import UploadedFile
import os

upload_path = "/tmp/mini_data_catalog/uploads/"


def get_etl_tables(etl_name: str) -> ETLTablesSerializer:
    etl_object = ETLNames.objects.prefetch_related("tables__schema").get(name=etl_name)

    return ETLTablesSerializer(etl_object)  # type: ignore


def store_data_file(request: Request) -> str:
    file = validate_file(request)

    os.makedirs(upload_path, exist_ok=True)

    file_path = f"{upload_path}{uuid.uuid4()}_{file.name}"
    with open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return file_path


def validate_file(request: Request) -> UploadedFile:
    allowed_file_types = ["csv", "json"]

    file = request.FILES.get("file")  # type: ignore
    if not file:
        raise ValidationError("Please upload a file.")

    file_type = file.name.split(".")[-1].lower()

    if file_type not in allowed_file_types:
        raise ValidationError(
            f"Invalid file type: {file_type}, Only {allowed_file_types.append(",")} allowed."
        )

    return file
