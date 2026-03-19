from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingCreateForm, BookingStatusForm, RegisterForm, ReviewForm, RoomFilterForm, RoomForm
from .models import Booking, Room


def home(request):
    return redirect("room_list")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("room_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def room_list(request):
    form = RoomFilterForm(request.GET or None)
    rooms = Room.objects.filter(availability=True).annotate(avg_rating=Avg("reviews__rating"))

    if form.is_valid():
        room_type = form.cleaned_data.get("room_type")
        max_price = form.cleaned_data.get("max_price")
        capacity = form.cleaned_data.get("capacity")

        if room_type:
            rooms = rooms.filter(room_type=room_type)
        if max_price is not None:
            rooms = rooms.filter(price__lte=max_price)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)

    return render(request, "reservations/room_list.html", {"rooms": rooms, "filter_form": form})


def room_detail(request, room_id):
    room = get_object_or_404(Room.objects.annotate(avg_rating=Avg("reviews__rating")), pk=room_id)
    review_form = ReviewForm()
    booking_form = BookingCreateForm()
    return render(
        request,
        "reservations/room_detail.html",
        {
            "room": room,
            "booking_form": booking_form,
            "review_form": review_form,
            "reviews": room.reviews.select_related("user"),
        },
    )


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method != "POST":
        return redirect("room_detail", room_id=room.id)

    form = BookingCreateForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.room = room

        try:
            booking.save()
        except Exception as exc:
            messages.error(request, str(exc))
            return redirect("room_detail", room_id=room.id)

        messages.success(request, f"Booking confirmed! Reference: {booking.booking_reference}")
        return redirect("user_dashboard")

    messages.error(request, "Please correct the booking form.")
    return redirect("room_detail", room_id=room.id)


@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.room = room
        review.save()
        messages.success(request, "Review submitted.")
    else:
        messages.error(request, "Unable to submit review.")
    return redirect("room_detail", room_id=room.id)


@login_required
def user_dashboard(request):
    bookings = request.user.bookings.select_related("room")
    stats = {
        "total": bookings.count(),
        "upcoming": bookings.filter(check_in__gte=date.today(), status__in=[Booking.PENDING, Booking.CONFIRMED]).count(),
        "spent": bookings.filter(status=Booking.CONFIRMED).aggregate(total=Sum("total_price"))["total"] or 0,
    }
    return render(request, "reservations/user_dashboard.html", {"bookings": bookings, "stats": stats})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status == Booking.CONFIRMED:
        messages.error(request, "Confirmed bookings can only be cancelled by admin.")
    else:
        booking.status = Booking.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
        messages.success(request, "Booking cancelled.")
    return redirect("user_dashboard")


@staff_member_required
def admin_dashboard(request):
    bookings = Booking.objects.select_related("room", "user")
    stats = {
        "rooms": Room.objects.count(),
        "bookings": bookings.count(),
        "pending": bookings.filter(status=Booking.PENDING).count(),
        "confirmed": bookings.filter(status=Booking.CONFIRMED).count(),
        "revenue": bookings.filter(status=Booking.CONFIRMED).aggregate(total=Sum("total_price"))["total"] or 0,
    }
    recent_bookings = bookings[:10]
    return render(request, "reservations/admin/dashboard.html", {"stats": stats, "recent_bookings": recent_bookings})


@staff_member_required
def admin_room_list(request):
    rooms = Room.objects.all()
    return render(request, "reservations/admin/room_list.html", {"rooms": rooms})


@staff_member_required
def admin_room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added.")
            return redirect("admin_room_list")
    else:
        form = RoomForm()
    return render(request, "reservations/admin/room_form.html", {"form": form, "title": "Add Room"})


@staff_member_required
def admin_room_update(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated.")
            return redirect("admin_room_list")
    else:
        form = RoomForm(instance=room)
    return render(request, "reservations/admin/room_form.html", {"form": form, "title": "Edit Room"})


@staff_member_required
def admin_room_delete(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deleted.")
        return redirect("admin_room_list")
    return render(request, "reservations/admin/room_delete_confirm.html", {"room": room})


@staff_member_required
def admin_booking_list(request):
    status = request.GET.get("status")
    bookings = Booking.objects.select_related("room", "user")
    if status:
        bookings = bookings.filter(status=status)
    return render(request, "reservations/admin/booking_list.html", {"bookings": bookings})


@staff_member_required
def admin_booking_update_status(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == "POST":
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking status updated.")
            return redirect("admin_booking_list")
    else:
        form = BookingStatusForm(instance=booking)
    return render(
        request,
        "reservations/admin/booking_status_form.html",
        {"form": form, "booking": booking},
    )


@staff_member_required
def admin_reports(request):
    bookings = Booking.objects.select_related("room")
    room_summary = (
        bookings.values("room__name")
        .annotate(total_bookings=Count("id"), revenue=Sum("total_price"))
        .order_by("-revenue")
    )
    totals = {
        "all_bookings": bookings.count(),
        "confirmed_revenue": bookings.filter(status=Booking.CONFIRMED).aggregate(total=Sum("total_price"))["total"] or 0,
        "cancelled": bookings.filter(status=Booking.CANCELLED).count(),
    }
    return render(request, "reservations/admin/reports.html", {"room_summary": room_summary, "totals": totals})


@login_required
def availability_calendar(request):
    return render(request, "reservations/calendar.html")


@login_required
def availability_events(request):
    room_id = request.GET.get("room")
    filters = Q(status__in=[Booking.PENDING, Booking.CONFIRMED])
    if room_id:
        filters &= Q(room_id=room_id)

    bookings = Booking.objects.filter(filters).select_related("room")
    events = [
        {
            "title": f"{booking.room.name} ({booking.get_status_display()})",
            "start": booking.check_in.isoformat(),
            "end": booking.check_out.isoformat(),
            "color": "#16a34a" if booking.status == Booking.CONFIRMED else "#f59e0b",
        }
        for booking in bookings
    ]
    return JsonResponse(events, safe=False)
