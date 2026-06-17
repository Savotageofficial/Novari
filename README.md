# Novari — E-Commerce Backend API

A Django-based REST API backend for the Novari e-commerce platform. Built with Django REST Framework, PostgreSQL, and token-based admin authentication.

---

## Tech Stack

- **Backend:** Python, Django 6.x
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Auth:** Custom token-based authentication
- **Package Manager:** Pipenv

---

## Project Structure

```
Novari/
├── Novari/               # Project settings, root URLs, WSGI
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── novari_base/          # Main app — models, views, URLs
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── Pipfile
├── Pipfile.lock
└── manage.py
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Pipenv

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Savotageofficial/Novari.git
cd Novari
```

2. Install dependencies:

```bash
pipenv install
pipenv shell
```

3. Set up the database — create a PostgreSQL database and user, then update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'novari_db',
        'USER': 'novari_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

---

## API Endpoints

All endpoints require a trailing slash.

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List products with optional filters |
| GET | `/products/<id>/` | Get a single product by ID |
| POST | `/orders/` | Submit a new order |

#### Product Filter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `color` | string | Filter by color |
| `min_price` | integer | Minimum price |
| `max_price` | integer | Maximum price |

### Admin

All admin endpoints require an `Authorization` header with a valid token.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/login/` | Authenticate and receive a token |
| GET | `/admin/products/` | List all products |
| POST | `/admin/products/` | Create a new product |
| PATCH | `/admin/products/<id>/` | Update a product |
| DELETE | `/admin/products/<id>/` | Delete a product |

#### Authentication

```
Authorization: <your_token>
```

---

## Environment & Security

- Never commit your `SECRET_KEY` or database password to version control
- Set `DEBUG = False` in production
- Use environment variables for sensitive settings in production

---

## License

This project is proprietary. See [LICENSE](./LICENSE) for full terms.

---

## Author

**Mohamed Safwat Mahdy** — [Savotageofficial](https://github.com/Savotageofficial)
