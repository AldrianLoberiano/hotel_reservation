from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Review, Room


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RoomFilterForm(forms.Form):
    room_type = forms.ChoiceField(choices=[("", "All Types")] + Room.ROOM_TYPES, required=False)
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    capacity = forms.IntegerField(required=False, min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room_type"].widget.attrs.update({"class": "form-select"})
        self.fields["max_price"].widget.attrs.update({"class": "form-control", "placeholder": "e.g. 200"})
        self.fields["capacity"].widget.attrs.update({"class": "form-control", "placeholder": "e.g. 2"})


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["check_in", "check_out", "payment_method"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "check_out": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "room_type", "price", "capacity", "availability", "image", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "room_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "availability": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
