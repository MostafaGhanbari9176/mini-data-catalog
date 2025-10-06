from rest_framework import serializers
from .models import ETLNames, TableNames


class TableSerializer(serializers.ModelSerializer):
    schema = serializers.CharField(source="schema.name")

    class Meta:
        model = TableNames
        fields = ["name", "schema"]


class ETLTablesSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True)

    class Meta:
        model = ETLNames
        fields = ["name", "tables"]
