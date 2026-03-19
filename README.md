# Hotel Reservation System (Django)

A full-stack web-based Hotel Reservation System built with Django.

## Login Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- Admin Dashboard: `http://127.0.0.1:8000/admin-dashboard/`
- Django Admin: `http://127.0.0.1:8000/django-admin/`

### Regular User Account
- **Username:** `guest`
- **Password:** `guest123`

> To seed sample data (rooms, bookings, reviews), run:
> ```powershell
> .\.venv\Scripts\Activate.ps1
> python manage.py seed_data
> ```

## Features

- User registration and authentication
- Room browsing with filters: type, max price, capacity
- Room details with image, rating/reviews, and booking form
- Live price preview (auto-calculates total as you pick dates)
- Booking with check-in/check-out, overlap validation, status tracking
- User dashboard with booking history
- Admin dashboard with room CRUD, booking management, and revenue reports
- Calendar view for room availability (FullCalendar)
- Payment method selection (Pay at Hotel, GCash, PayMongo)
- REST API for rooms and bookings

## Tech Stack

- Python + Django
- Django REST Framework
- SQLite (default)
- Bootstrap 5 + custom CSS

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
python manage.py migrate
```

4. Seed sample data (creates admin, guest user, rooms, bookings, reviews):

```powershell
python manage.py seed_data
```

5. Start the server:

```powershell
python manage.py runserver
```

6. Open in browser:

- Browse Rooms: `http://127.0.0.1:8000/rooms/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- User Dashboard: `http://127.0.0.1:8000/dashboard/`
- Admin Dashboard: `http://127.0.0.1:8000/admin-dashboard/`
- API Root: `http://127.0.0.1:8000/api/`

## API Endpoints

- `GET /api/rooms/` — list available rooms
- `GET /api/rooms/{id}/` — room details
- `GET /api/bookings/` — list user bookings (staff sees all)
- `POST /api/bookings/` — create booking
- `PATCH /api/bookings/{id}/` — update booking
