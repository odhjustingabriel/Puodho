# Puodho Farm Website

Puodho is a simple Django web application for a rural farm business. It helps customers browse fresh farm produce and submit structured order requests for broiler chickens and eggs without becoming a full e-commerce system.

## Features

- Premium, responsive public website with Home, Products, Order Assistant, About Us, and Contact pages.
- Flexible produce catalog using categories, products, and product options so Puodho can later add goats, sheep, cows, or other farm produce.
- Guided chatbot-style order assistant built with fixed JavaScript steps, not AI.
- Customers can order broiler chickens, eggs, or both in one request.
- Broiler options support Alive and Prepared pricing.
- Server-side order item and total calculations that preserve unit prices at order time.
- Simple order references such as `PUODHO-1001`.
- Protected staff dashboard for viewing, filtering, and managing orders.
- Product management screens for adding/editing products, updating prices, availability, and optional stock quantity.
- Django Admin remains available at `/admin/`.

## Tech Stack

- Django
- SQLite for development
- HTML, CSS, JavaScript
- Django templates

## Intentionally excluded from version 1

Puodho v1 does **not** include online payments, M-Pesa, customer accounts, carts, delivery fee automation, real AI chat, external APIs, Docker, or PostgreSQL.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Optional environment variables:

   ```bash
   export DJANGO_SECRET_KEY="replace-this-in-production"
   export DJANGO_DEBUG=True
   ```

## Database and seed data

Run migrations:

```bash
python manage.py migrate
```

Seed initial Puodho products:

```bash
python manage.py seed_puodho
```

The seed command creates:

- Category: Poultry
- Category: Eggs
- Product: Broiler Chicken
  - Alive, Ksh 650
  - Prepared, Ksh 750
- Product: Eggs, Ksh 450 per tray

## Create a superuser

```bash
python manage.py createsuperuser
```

Use the superuser to log in at `/accounts/login/`, access the custom dashboard at `/dashboard/`, or use Django Admin at `/admin/`.

## Run the development server

```bash
python manage.py runserver
```

Then visit:

- Public website: <http://127.0.0.1:8000/>
- Products: <http://127.0.0.1:8000/products/>
- Order assistant: <http://127.0.0.1:8000/order/>
- Staff dashboard: <http://127.0.0.1:8000/dashboard/>

## Testing

Run the Django test suite:

```bash
python manage.py test
```

The tests cover public pages, valid order submission, order reference creation, order total calculation, dashboard login protection, and staff dashboard access.

## Notes for farm operations

Delivery is mainly for nearby villages, towns, and roughly a 30 km radius. The website does not automatically calculate delivery fees. Customers are told that delivery and availability are subject to confirmation.
