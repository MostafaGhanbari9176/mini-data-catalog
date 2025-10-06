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
    try:
        if file_path.endswith(".csv"):
            process_csv(file_path)
        elif file_path.endswith(".json"):
            process_json(file_path)
    except:
        raise ValidationError("Error in parsing file.")
    finally:
        os.remove(file_path)


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
            chunk = data[i : i + CHUNK_SIZE]
            insert_chunk(chunk)


@transaction.atomic
def insert_chunk(chunk: list[dict]):
    for row in chunk:
        etl_obj, _ = ETLNames.objects.get_or_create(name=row["etl_name"])
        schema_obj, _ = SchemaNames.objects.get_or_create(name=row["schema_name"])
        table_obj, _ = TableNames.objects.get_or_create(
            name=row["table_name"], schema=schema_obj
        )
        ETLTableRel.objects.get_or_create(etl=etl_obj, table=table_obj)
