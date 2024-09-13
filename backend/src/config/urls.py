from django.urls import path

from .views import get_data

urlpatterns = [
    # TODO - excluir esse path (apenas para fins de exemplo)
    path("api/data/", get_data, name="get_data"),
]
