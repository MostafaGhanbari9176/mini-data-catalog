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


class DatabaseConnectionSerializer(serializers.Serializer):
    db_type = serializers.ChoiceField(choices=["postgres", "oracle"])
    host = serializers.CharField(max_length=255, required=False, allow_blank=True)
    port = serializers.IntegerField(required=False, default=0)
    dbname = serializers.CharField(max_length=255, required=False, allow_blank=True)
    user = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
    etl_name = serializers.CharField(max_length=255, required=True)
    dsn = serializers.CharField(max_length=1024, required=False, allow_blank=True)

    def validate(self, data):  # type: ignore
        if data["db_type"] == "postgres" and not (
            data.get("dbname") and data.get("host") and data.get("port")
        ):
            raise serializers.ValidationError("Postgres requires 'dbname' field.")
        if data["db_type"] == "oracle" and not (
            data.get("dsn") or (data.get("host") and data.get("port"))
        ):
            raise serializers.ValidationError("Oracle requires 'dsn' or host+port.")
        return data
