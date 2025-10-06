from rest_framework.request import Request
from api.serializer import ETLTablesSerializer
from api.models import ETLNames


def get_etl_tables(etl_name:str) -> ETLTablesSerializer:
    etl_object = ETLNames.objects.prefetch_related("tables__schema").get(name=etl_name)

    return ETLTablesSerializer(etl_object) # type: ignore

