from django.db import models


class SchemaNames(models.Model):
    name = models.CharField(max_length=255, unique=True)


class ETLNames(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TableNames(models.Model):
    name = models.CharField(max_length=255)
    schema = models.ForeignKey(SchemaNames, on_delete=models.CASCADE)
    etls = models.ManyToManyField(ETLNames, through="ETLTableRel")

    class Meta:
        unique_together = (
            "name",
            "schema",
        )  # table name must be unique per each schema


class ETLTableRel(models.Model):
    etl = models.ForeignKey(ETLNames, on_delete=models.CASCADE)
    table = models.ForeignKey(TableNames, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("etl", "table")  # unique relations
