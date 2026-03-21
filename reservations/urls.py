from django.urls import path

from . import views

urlpatterns = [
    path("", views.room_list, name="home"),
    path("register/", views.register_view, name="register"),
    path("rooms/", views.room_list, name="room_list"),
    path("rooms/<int:room_id>/", views.room_detail, name="room_detail"),
    path("rooms/<int:room_id>/book/", views.create_booking, name="create_booking"),
    path("rooms/<int:room_id>/review/", views.add_review, name="add_review"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("bookings/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("calendar/", views.availability_calendar, name="availability_calendar"),
    path("calendar/events/", views.availability_events, name="availability_events"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/rooms/", views.admin_room_list, name="admin_room_list"),
    path("admin-dashboard/rooms/add/", views.admin_room_create, name="admin_room_create"),
    path("admin-dashboard/rooms/<int:room_id>/edit/", views.admin_room_update, name="admin_room_update"),
    path("admin-dashboard/rooms/<int:room_id>/delete/", views.admin_room_delete, name="admin_room_delete"),
    path("admin-dashboard/bookings/", views.admin_booking_list, name="admin_booking_list"),
    path(
        "admin-dashboard/bookings/<int:booking_id>/status/",
        views.admin_booking_update_status,
        name="admin_booking_update_status",
    ),
    path("admin-dashboard/reports/", views.admin_reports, name="admin_reports"),
]
