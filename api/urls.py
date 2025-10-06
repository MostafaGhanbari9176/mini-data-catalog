from django.urls import path
from .views import FetchETLTables

urlpatterns = [
    path("etl/<str:etl_name>/tables/", FetchETLTables.as_view(), name="etl-tables"),
]