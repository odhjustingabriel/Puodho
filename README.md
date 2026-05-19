# Puodho Farm Website

Puodho is a simple Django web application for a rural farm business. It helps customers browse fresh farm produce and submit structured order requests for broiler chickens and eggs without becoming a full e-commerce system.

## Features

- Premium, responsive public website with Home, Products, Order Assistant, About Us, and Contact pages.
- Flexible produce catalog using categories, products, and product options so Puodho can later add goats, sheep, cows, or other farm produce.
- Guided chatbot-style order assistant built with fixed JavaScript steps, not AI.
- Customers can submit guided requests for broiler chickens, eggs, livestock, milk products, or mixed farm produce in one request.
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

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies, including Django:

   ```bash
   python -m pip install -r requirements.txt
   ```

   If you see `ModuleNotFoundError: No module named 'django'`, it means the active Python environment does not have Django installed yet. Run the install command above inside the activated virtual environment.

4. Optional environment variables:

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

The seed command creates starter catalog data for:

- Poultry: Broiler Chicken
  - Alive, Ksh 650
  - Prepared, Ksh 750
- Eggs: Eggs, Ksh 450 per tray
- Cattle: Friesian/Holstein, Ayrshire, Sahiwal, and Boran options with starter prices and age guidance
- Goats: Galla, Boer, Saanen, and Toggenburg/Alpine options with starter prices and age guidance
- Sheep: Dorper, Red Maasai, Blackhead Persian, and Merino options with starter prices and age guidance
- Milk Products: Cow Milk, Goat Milk, Sheep Milk, and Bulk Milk Order, including quote-on-request options where pricing depends on availability

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

## Security hardening

- Request rate limiting is enabled globally and stricter on authentication routes.
- Login/auth endpoints are limited to 5 attempts per 15 minutes per client IP.
- Upload/request payload limits are configured in Django settings to reduce oversized payload abuse.
- Forms sanitize and validate user input (phone formats, text lengths, required fields).
- Keep `DJANGO_SECRET_KEY` in environment variables for deployment; do not commit production secrets.

## OWASP Top 10 coverage

- **A01 Broken Access Control:** Staff dashboard routes are protected with `login_required` + staff checks; CSRF middleware enabled.
- **A02 Cryptographic Failures:** Secret key is environment-driven for non-debug; secure-cookie and transport-related settings are hardened for production.
- **A03 Injection:** Inputs are validated/sanitized through Django forms and field validators; malformed data is rejected.
- **A04 Insecure Design:** Guided, constrained assistant uses fixed controlled inputs and server-side validation for product/quantity/option logic.
- **A05 Security Misconfiguration:** Added production guardrails for secret key and shared cache requirement, security headers, upload limits, and proxy handling controls.
- **A06 Vulnerable/Outdated Components:** Dependency pinning remains in `requirements.txt`; regularly update Django and run `pip audit` in CI/CD.
- **A07 Identification and Authentication Failures:** Added auth-route rate limiting and username lockout window controls.
- **A08 Software and Data Integrity Failures:** No dynamic code loading; prefer signed releases and lockfiles in deployment pipeline.
- **A09 Security Logging and Monitoring Failures:** Added dedicated `farm.security` logger to capture throttling/security events to `security.log`.
- **A10 SSRF:** No outbound URL fetch features are implemented in the current app; avoid introducing unrestricted server-side URL fetches.

## Full security measures implemented

- Global request rate limiting and stricter auth rate limits (5 attempts / 15 min) including username lockout window controls.
- Trusted-proxy-aware IP extraction logic for throttling; only honors `X-Forwarded-For` from configured proxy IPs.
- Payload hard limits (`DATA_UPLOAD_MAX_*`, `FILE_UPLOAD_MAX_MEMORY_SIZE`) to mitigate oversized/malformed requests.
- Contact form sanitization/validation and stricter order form sanitization (trimmed fields, regex phone validation, bounded lengths).
- Security headers and cookie hardening defaults for production-oriented deployment (`X_FRAME_OPTIONS`, `SECURE_*`, `SESSION_COOKIE_*`, `CSRF_COOKIE_*`).
- Secret handling moved to environment variables for deployment safety; no production secrets are committed.
- Security event logging (`farm.security`) for rate limit and abuse monitoring.

