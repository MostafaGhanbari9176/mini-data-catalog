import psycopg2
import oracledb
from api.serializer import DatabaseConnectionSerializer
from rest_framework.request import Request
from django.db import transaction
from api.models import ETLNames, SchemaNames, TableNames, ETLTableRel


def read_data_from_db(request: Request):
    serializer = DatabaseConnectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    input = serializer.validated_data

    result: list[tuple[str, str]] = []

    if input["db_type"] == "postgres":  # type: ignore
        result = fetch_postgres_tables(input["host"], input["port"], input["dbname"], input["user"], input["password"])  # type: ignore
    else:
        result = fetch_oracle_tables(input["dsn"], input["host"], input["port"], input["dbname"], input["user"], input["password"])  # type: ignore

    store_result(result, input["etl_name"])  # type: ignore


@transaction.atomic
def store_result(result, etl_name):
    etl_obj, _ = ETLNames.objects.get_or_create(name=etl_name)
    for schema_name, table_name in result:
        schema_obj, _ = SchemaNames.objects.get_or_create(name=schema_name)
        table_obj, _ = TableNames.objects.get_or_create(
            name=table_name, schema=schema_obj
        )
        ETLTableRel.objects.get_or_create(etl=etl_obj, table=table_obj)


def fetch_postgres_tables(host, port, dbname, user, password):
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE';
    """
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def fetch_oracle_tables(dsn, host, port, dbname, user, password):
    if not dsn:
        dsn = oracledb.makedsn(host, port, service_name=dbname)

    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT owner, table_name
        FROM all_tables
    """
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
