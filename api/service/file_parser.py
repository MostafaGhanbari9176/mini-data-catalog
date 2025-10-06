import os
import csv
import json
from itertools import islice
from django.db import transaction
from api.models import ETLNames, SchemaNames, TableNames, ETLTableRel
from rest_framework.exceptions import ValidationError

CHUNK_SIZE = 1024

def parse_file(file_path: str):
    print(file_path)
    # try:
    if file_path.endswith(".csv"):
        process_csv(file_path)
    elif file_path.endswith(".json"):
        process_json(file_path)
    # except:
    #     raise ValidationError("Error in parsing file.")
    # finally:
    #     os.remove(file_path)

def process_csv(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        while True:
            chunk = list(islice(reader, CHUNK_SIZE))
            if not chunk:
                break
            insert_chunk(chunk)

def process_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in range(0, len(data), CHUNK_SIZE):
            chunk = data[i:i+CHUNK_SIZE]
            insert_chunk(chunk)

def insert_chunk(chunk: list[dict]):
    etls_cache = {e.name: e for e in ETLNames.objects.all()}
    schemas_cache = {s.name: s for s in SchemaNames.objects.all()}
    new_tables = []
    etl_table_rels = []

    for row in chunk:
        etl_name = row.get("etl_name")
        schema_name = row.get("schema_name")
        table_name = row.get("table_name")

        etl_objct = etls_cache.get(etl_name) # type: ignore
        if not etl_objct:
            etl_objct = ETLNames(name=etl_name)
            etls_cache[etl_name] = etl_objct # type: ignore

        schema_object = schemas_cache.get(schema_name) # type: ignore
        if not schema_object:
            schema_object = SchemaNames(name=schema_name)
            schemas_cache[schema_name] = schema_object # type: ignore

        table_object = TableNames(name=table_name, schema=schema_object)
        new_tables.append(table_object)

        etl_table_rels.append((etl_name, table_name, schema_name))

    breakpoint()

    with transaction.atomic():
        SchemaNames.objects.bulk_create(
            [s for s in schemas_cache.values() if s.pk is None],
            ignore_conflicts=True
        )

        ETLNames.objects.bulk_create(
            [e for e in etls_cache.values() if e.pk is None],
            ignore_conflicts=True
        )

        TableNames.objects.bulk_create(new_tables, ignore_conflicts=True)

        etl_table_objects = []
        for etl_name, table_name, schema_name in etl_table_rels:
            etl_objct = ETLNames.objects.get(name=etl_name)
            schema_object = SchemaNames.objects.get(name=schema_name)
            table_object = TableNames.objects.get(name=table_name, schema=schema_object)
            etl_table_objects.append(
                ETLTableRel(etl=etl_objct, table=table_object)
            )

        ETLTableRel.objects.bulk_create(etl_table_objects, ignore_conflicts=True)

