from django.urls import path
from .views import *

urlpatterns = [
    path("etl/<str:etl_name>/tables/", fetch_etl_tables, name="etl-tables"),
    path("data/file/", upload_data_file, name="upload-file"),
    path("data/database/", data_source, name="data-source"),
]
