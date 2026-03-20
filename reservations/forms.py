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
    delete_image = forms.BooleanField(required=False, label="Delete current photo")

    FIELD_ORDER = ["name", "room_type", "price", "capacity", "availability", "image", "delete_image", "description"]

    class Meta:
        model = Room
        fields = ["name", "room_type", "price", "capacity", "availability", "image", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "room_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "availability": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["delete_image"].widget.attrs.update({"class": "btn-check"})

        if not self.instance.pk or not self.instance.image:
            self.fields.pop("delete_image")

        self.order_fields([name for name in self.FIELD_ORDER if name in self.fields])

    def save(self, commit=True):
        existing_image = None
        if self.instance.pk:
            existing_image = Room.objects.filter(pk=self.instance.pk).values_list("image", flat=True).first()

        room = super().save(commit=False)
        delete_requested = self.cleaned_data.get("delete_image", False)
        replaced_image = bool(existing_image and self.cleaned_data.get("image") and str(existing_image) != str(room.image.name))
        image_storage = room._meta.get_field("image").storage

        if delete_requested:
            if existing_image:
                image_storage.delete(existing_image)
            room.image = None

        if commit:
            room.save()
            self.save_m2m()

        if replaced_image:
            image_storage.delete(existing_image)

        return room


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
