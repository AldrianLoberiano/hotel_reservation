# Hotel Reservation System (Django)

A full-stack web-based Hotel Reservation System built with Django.

## Features

- User registration and authentication (Django auth)
- Room browsing with filters: type, max price, capacity
- Room details with image, rating/reviews, and booking form
- Booking flow with:
  - check-in/check-out date selection
  - automatic total cost calculation by nights x room price
  - overlap validation for the same room
  - booking statuses (`pending`, `confirmed`, `cancelled`)
  - confirmation email (console backend by default)
- User dashboard with booking history and status
- Admin dashboard with:
  - room CRUD (add/edit/delete)
  - room availability management
  - booking status management (approve/cancel)
  - reports (total bookings and confirmed revenue)
- Calendar view for room availability (FullCalendar)
- Optional payment hook fields (`pay_later`, `gcash`, `paymongo`)
- REST API via Django REST Framework for rooms and bookings

## Tech Stack

- Python + Django
- Django REST Framework
- SQLite (default, easy local setup)
- Bootstrap 5 + custom CSS

## Project Structure

```text
hotel_reservation/
  hotel_reservation/
    settings.py
    urls.py
    templates/
    static/
  reservations/
    api/
    migrations/
    models.py
    views.py
    forms.py
    urls.py
  manage.py
  requirements.txt
```

## Setup (Windows PowerShell)

1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Create admin user:

```powershell
python manage.py createsuperuser
```

5. Start the server:

```powershell
python manage.py runserver
```

6. Open in browser:

- User app: `http://127.0.0.1:8000/rooms/`
- Django admin: `http://127.0.0.1:8000/django-admin/`
- Custom admin dashboard: `http://127.0.0.1:8000/admin-dashboard/`
- API root: `http://127.0.0.1:8000/api/`

## Media and Images

Room images are uploaded to `media/rooms/` and served in development mode.

## Email Confirmation

This project uses Django's console email backend. Booking confirmations are printed in the server console.

To send real emails, update in `hotel_reservation/settings.py`:

- `EMAIL_BACKEND`
- SMTP host/port/user/password settings

## Payment Integration Note

`GCash` and `PayMongo` are implemented as integration hooks with simulated transaction IDs.

To connect a real gateway:

1. Add a payment service module in `reservations/services/`.
2. Call API SDK from `create_booking` view.
3. Store real transaction ID and payment status.
4. Add webhook endpoint for payment confirmation.

## API Endpoints

- `GET /api/rooms/` list available rooms
- `GET /api/rooms/{id}/` room details
- `GET /api/bookings/` list user bookings (staff sees all)
- `POST /api/bookings/` create booking
- `PATCH /api/bookings/{id}/` update booking (staff/use policy as needed)

## Optional Enhancements You Can Add Next

- PDF invoice generation (e.g., WeasyPrint)
- Django Channels for real-time booking updates
- Production-ready payment processing and webhooks
- Deployment with PostgreSQL + cloud object storage
