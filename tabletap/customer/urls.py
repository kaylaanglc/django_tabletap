from django.urls import path
from . import views

urlpatterns = [
    path("table/<int:restaurant_id>/<int:table_number>/", views.table_order_view, name="table_order"),
    path("confirmation/<int:restaurant_id>/<int:table_number>/", views.order_confirmation_view, name="confirmation"),
]