from django.urls import path
from .views import FetchETLTables, UploadDataFile

urlpatterns = [
    path("etl/<str:etl_name>/tables/", FetchETLTables.as_view(), name="etl-tables"),
    path("data/file/", UploadDataFile.as_view(), name="upload-file")
]