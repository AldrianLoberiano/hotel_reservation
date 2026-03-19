from django.contrib import admin

from .models import Booking, Review, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "room_type", "price", "capacity", "availability")
    list_filter = ("room_type", "availability")
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_reference", "user", "room", "check_in", "check_out", "total_price", "status")
    list_filter = ("status", "payment_method")
    search_fields = ("booking_reference", "user__username", "room__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "rating", "created_at")
    list_filter = ("rating",)
