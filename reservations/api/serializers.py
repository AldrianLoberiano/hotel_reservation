from rest_framework import serializers

from reservations.models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "room_type",
            "price",
            "capacity",
            "availability",
            "description",
            "image",
        ]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_reference",
            "user",
            "room",
            "room_name",
            "check_in",
            "check_out",
            "total_price",
            "status",
            "payment_method",
            "created_at",
        ]
        read_only_fields = ["booking_reference", "total_price", "status", "created_at"]
