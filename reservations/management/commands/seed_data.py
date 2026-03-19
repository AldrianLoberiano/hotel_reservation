"""
Management command to seed the database with sample data.
Creates admin user, guest user, sample rooms, bookings, and reviews.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from reservations.models import Booking, Review, Room


class Command(BaseCommand):
    help = "Seed the database with sample rooms, users, bookings, and reviews."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ── Users ──────────────────────────────────────────────
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@staysmart.ph", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("  Created admin user (admin / admin123)"))
        else:
            self.stdout.write("  Admin user already exists.")

        guest, created = User.objects.get_or_create(
            username="guest",
            defaults={"email": "guest@example.com"},
        )
        if created:
            guest.set_password("guest123")
            guest.save()
            self.stdout.write(self.style.SUCCESS("  Created guest user (guest / guest123)"))
        else:
            self.stdout.write("  Guest user already exists.")

        # ── Rooms ──────────────────────────────────────────────
        rooms_data = [
            {
                "name": "Ocean View Suite",
                "room_type": Room.SUITE,
                "price": Decimal("299.00"),
                "capacity": 2,
                "description": "Luxurious suite with a breathtaking panoramic ocean view, king-size bed, marble bathroom, and a private balcony. Includes complimentary breakfast.",
            },
            {
                "name": "Deluxe King Room",
                "room_type": Room.DELUXE,
                "price": Decimal("189.00"),
                "capacity": 2,
                "description": "Elegant room featuring a king-size bed, premium linens, work desk, and modern amenities. Perfect for business or leisure travelers.",
            },
            {
                "name": "Standard Twin Room",
                "room_type": Room.STANDARD,
                "price": Decimal("99.00"),
                "capacity": 2,
                "description": "Comfortable room with two single beds, air conditioning, flat-screen TV, and free Wi-Fi. Great value for budget-conscious travelers.",
            },
            {
                "name": "Family Suite",
                "room_type": Room.FAMILY,
                "price": Decimal("349.00"),
                "capacity": 5,
                "description": "Spacious two-bedroom suite designed for families. Features a living area, kitchenette, two bathrooms, and complimentary kids' activities pass.",
            },
            {
                "name": "Deluxe Garden Room",
                "room_type": Room.DELUXE,
                "price": Decimal("159.00"),
                "capacity": 2,
                "description": "Charming room overlooking our tropical garden. Includes queen-size bed, rain shower, minibar, and direct garden access.",
            },
            {
                "name": "Standard Economy Room",
                "room_type": Room.STANDARD,
                "price": Decimal("69.00"),
                "capacity": 1,
                "description": "Cozy single-occupancy room with all essentials: comfortable bed, private bathroom, Wi-Fi, and air conditioning at our best price.",
            },
            {
                "name": "Presidential Suite",
                "room_type": Room.SUITE,
                "price": Decimal("599.00"),
                "capacity": 4,
                "description": "Our finest accommodation featuring a master bedroom, separate living and dining areas, jacuzzi, butler service, and panoramic city views.",
            },
            {
                "name": "Family Bunk Room",
                "room_type": Room.FAMILY,
                "price": Decimal("199.00"),
                "capacity": 4,
                "description": "Fun room with bunk beds and a pull-out sofa, perfect for families with kids. Includes play area access and breakfast for the whole family.",
            },
        ]

        created_rooms = []
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                name=room_data["name"],
                defaults=room_data,
            )
            created_rooms.append(room)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Created room: {room.name}"))
            else:
                self.stdout.write(f"  Room already exists: {room.name}")

        # ── Bookings ───────────────────────────────────────────
        today = timezone.localdate()

        bookings_data = [
            {
                "user": guest,
                "room": created_rooms[0],  # Ocean View Suite
                "check_in": today + timedelta(days=5),
                "check_out": today + timedelta(days=8),
                "payment_method": Booking.PAY_LATER,
            },
            {
                "user": guest,
                "room": created_rooms[1],  # Deluxe King Room
                "check_in": today + timedelta(days=12),
                "check_out": today + timedelta(days=15),
                "payment_method": Booking.GCASH,
            },
            {
                "user": guest,
                "room": created_rooms[3],  # Family Suite
                "check_in": today + timedelta(days=20),
                "check_out": today + timedelta(days=25),
                "payment_method": Booking.PAYMONGO,
            },
        ]

        for bdata in bookings_data:
            existing = Booking.objects.filter(
                user=bdata["user"],
                room=bdata["room"],
                check_in=bdata["check_in"],
            ).exists()
            if not existing:
                try:
                    booking = Booking(
                        user=bdata["user"],
                        room=bdata["room"],
                        check_in=bdata["check_in"],
                        check_out=bdata["check_out"],
                        payment_method=bdata["payment_method"],
                    )
                    booking.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"  Created booking: {booking.booking_reference} for {booking.room.name}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  Skipped booking: {e}"))
            else:
                self.stdout.write(f"  Booking already exists for {bdata['room'].name}")

        # ── Reviews ────────────────────────────────────────────
        reviews_data = [
            {"user": guest, "room": created_rooms[0], "rating": 5, "comment": "Absolutely stunning ocean view! The suite was immaculate and the service was top-notch. Will definitely return."},
            {"user": guest, "room": created_rooms[1], "rating": 4, "comment": "Very comfortable room with great amenities. The bed was incredibly soft. Only wish the minibar had more options."},
            {"user": guest, "room": created_rooms[2], "rating": 4, "comment": "Great value for money. Clean, comfortable, and had everything we needed. Perfect for a short stay."},
            {"user": admin, "room": created_rooms[0], "rating": 5, "comment": "Perfect for a weekend getaway. The balcony view at sunset is unforgettable."},
            {"user": admin, "room": created_rooms[3], "rating": 5, "comment": "Brought the whole family and everyone loved it. The kids area was a lifesaver! Spacious and well-equipped."},
            {"user": admin, "room": created_rooms[4], "rating": 4, "comment": "Beautiful garden setting. Very peaceful and relaxing. The rain shower was a nice touch."},
        ]

        for rdata in reviews_data:
            review, created = Review.objects.get_or_create(
                user=rdata["user"],
                room=rdata["room"],
                defaults={"rating": rdata["rating"], "comment": rdata["comment"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  Created review for {review.room.name} by {review.user.username}"))
            else:
                self.stdout.write(f"  Review already exists for {review.room.name} by {review.user.username}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✓ Seeding complete!"))
        self.stdout.write(self.style.SUCCESS("  Admin login: admin / admin123"))
        self.stdout.write(self.style.SUCCESS("  Guest login: guest / guest123"))
        self.stdout.write(self.style.SUCCESS(f"  {len(created_rooms)} rooms, bookings, and reviews ready."))
