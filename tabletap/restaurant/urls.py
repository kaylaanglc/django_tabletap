from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("menu/", views.menu_view, name="menu"),
    path("menu/category/<int:category_id>/edit/", views.edit_category_view, name="edit_category"),
    path("menu/category/<int:category_id>/delete/", views.delete_category_view, name="delete_category"),
    path("add-item/", views.add_item_view, name="add_item"),
    path("edit-item/<int:item_id>/", views.add_item_view, name="edit_item"),
    path("delete-item/<int:item_id>/", views.delete_item_view, name="delete_item"),
    path("orders/", views.orders_view, name="owner_orders"),
    path("orders/<int:order_id>/status/", views.update_order_status, name="update_order_status"),
    path("qrcode/", views.qr_generator_view, name="qr_generator"),
]
