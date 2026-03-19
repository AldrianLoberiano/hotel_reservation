from rest_framework import permissions, viewsets

from reservations.models import Booking, Room

from .serializers import BookingSerializer, RoomSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.filter(availability=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related("room", "user").all()
        return Booking.objects.select_related("room", "user").filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
