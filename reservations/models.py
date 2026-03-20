from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Room(models.Model):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"
    FAMILY = "family"

    ROOM_TYPES = [
        (STANDARD, "Standard"),
        (DELUXE, "Deluxe"),
        (SUITE, "Suite"),
        (FAMILY, "Family"),
    ]

    name = models.CharField(max_length=120)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=1)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to="rooms/", blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_room_type_display()})"


class Booking(models.Model):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
    ]

    PAY_LATER = "pay_later"
    GCASH = "gcash"
    PAYMONGO = "paymongo"

    PAYMENT_METHODS = [
        (PAY_LATER, "Pay at Hotel"),
        (GCASH, "GCash"),
        (PAYMONGO, "PayMongo"),
    ]

    booking_reference = models.CharField(max_length=40, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default=PAY_LATER)
    payment_transaction_id = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.booking_reference} - {self.user} - {self.room}"

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    def clean(self) -> None:
        # ModelForm validation can run before related objects are assigned.
        if not self.room_id or not self.check_in or not self.check_out:
            return

        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")

        if self._state.adding and self.check_in < timezone.localdate():
            raise ValidationError("Check-in date cannot be in the past.")

        if not self.room.availability:
            raise ValidationError("This room is currently marked unavailable.")

        overlapping = Booking.objects.filter(
            room=self.room,
            status__in=[Booking.PENDING, Booking.CONFIRMED],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This room is not available for the selected dates.")

    def calculate_total(self) -> Decimal:
        days = self.nights
        if days <= 0:
            raise ValidationError("Booking must be at least 1 night.")
        return Decimal(days) * self.room.price

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"BK-{uuid4().hex[:10].upper()}"
        self.full_clean()
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "room")

    def __str__(self) -> str:
        return f"{self.room.name} - {self.rating}/5"
