import psycopg2
import oracledb
from api.serializer import DatabaseConnectionSerializer
from rest_framework.request import Request
from django.db import transaction
from api.models import ETLNames, SchemaNames, TableNames, ETLTableRel
from rest_framework.exceptions import ValidationError
from celery import shared_task
from utils import utils
from django.utils import timezone


def read_data_from_db(request: Request):
    serializer = DatabaseConnectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    input = serializer.validated_data

    try:
        # first we create a temp connection for validating the connection info
        # for returning fine response
        connection = make_connection(input)  # type: ignore
        connection.close()    
        # then working with db in the background
        read_and_store_data.delay(input)  # type: ignore
    except:
        raise ValidationError("error on connecting into db source")


@shared_task
def read_and_store_data(input):
    result: list[tuple[str, str]] = []
    try:
        connection = make_connection(input)

        if input["db_type"] == "postgres":
            result = fetch_postgres_data(connection)
        else:
            result = fetch_oracle_data(connection)

        store_result(result, input["etl_name"])  # type: ignore
    except:
        utils.app_logger.error(
            f"{timezone.now()} error on reading data from db: {input.get("dbname")}"
        )


@transaction.atomic
def store_result(result, etl_name):
    etl_obj, _ = ETLNames.objects.get_or_create(name=etl_name)
    for schema_name, table_name in result:
        schema_obj, _ = SchemaNames.objects.get_or_create(name=schema_name)
        table_obj, _ = TableNames.objects.get_or_create(
            name=table_name, schema=schema_obj
        )
        ETLTableRel.objects.get_or_create(etl=etl_obj, table=table_obj)


def make_connection(input: dict):
    db_type = input.get("db_type")
    dsn = input.get("dsn")
    host = input.get("host")
    port = input.get("port")
    dbname = input.get("dbname")
    user = input.get("user")
    password = input.get("password")

    if db_type == "postgres":
        return psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
    else:
        if not dsn:
            dsn = oracledb.makedsn(host, port, service_name=dbname)  # type: ignore
        return oracledb.connect(user=user, password=password, dsn=dsn)


def fetch_postgres_data(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE';
    """
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def fetch_oracle_data(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT owner, table_name
        FROM all_tables
    """
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
