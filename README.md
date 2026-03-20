# CozyStay Hotel Reservation System

Web-based hotel reservation platform built with Django, Bootstrap, and Django REST Framework.

## What Is Included

- Public room browsing page with hero carousel background
- About and Services sections on the homepage
- Room filtering by room type, max price, and capacity
- Room details page with booking form and reviews
- Booking overlap validation and booking status flow
- User dashboard and booking cancellation flow
- Admin dashboard, booking management, room management, and reports
- Calendar availability view
- REST API for rooms and bookings

## Authentication Behavior

- Regular users are redirected to `room_list` after login.
- Staff/admin users are redirected directly to `admin_dashboard` after login.
- If a `next` query param is present, it is respected.

## Demo Credentials (Seed Data)

### Admin account

- Username: `admin`
- Password: `admin123`
- Admin dashboard: `http://127.0.0.1:8000/admin-dashboard/`
- Django admin: `http://127.0.0.1:8000/django-admin/`

### Regular user account

- Username: `guest`
- Password: `guest123`

## Tech Stack

- Python
- Django
- Django REST Framework
- Bootstrap 5 + custom CSS
- SQLite (default)

## Project Setup (Windows PowerShell)

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Apply migrations.

```powershell
python manage.py migrate
```

4. Seed sample data (users, rooms, bookings, reviews).

```powershell
python manage.py seed_data
```

5. Run the development server.

```powershell
python manage.py runserver
```

## Main Routes

- Home: `http://127.0.0.1:8000/`
- Rooms: `http://127.0.0.1:8000/rooms/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- User dashboard: `http://127.0.0.1:8000/dashboard/`
- Admin dashboard: `http://127.0.0.1:8000/admin-dashboard/`
- API root: `http://127.0.0.1:8000/api/`

## API Endpoints

- `GET /api/rooms/` - List available rooms
- `GET /api/rooms/{id}/` - Room details
- `GET /api/bookings/` - List user bookings (staff sees all)
- `POST /api/bookings/` - Create booking
- `PATCH /api/bookings/{id}/` - Update booking
