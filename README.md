# TransmiTata

A Django-based web application for tracking and managing transportation routes.

## Overview

TransmiTata is a web application built with Django and Django REST Framework that provides APIs and web interfaces for managing transportation routes, routes collections, and viewing route information.

## Features

- **API Services**: Search and retrieve route information from external sources
- **Route Management**: Create and manage transportation routes and collections
- **Web Interface**: Simple web templates for viewing routes information
- **Comprehensive Testing**: Full test coverage with Django's test framework

## Project Structure

```
transmitata/
├── api/                    # Django API app
│   ├── models.py          # Route and RouteCollection models
│   ├── views.py           # API views and ViewSets
│   ├── services.py        # External API services
│   ├── tests/             # API tests (models, views, services)
│   └── urls.py            # API URL routing
├── web/                   # Django web app
│   ├── views.py           # Template views
│   ├── tests/             # Web tests
│   ├── templates/         # HTML templates
│   └── urls.py            # Web URL routing
├── static/                # Static files (CSS, JS)
├── manage.py              # Django management script
├── pytest.ini             # Pytest configuration
├── Makefile               # Make commands for development
└── requirements.txt       # Python dependencies
```

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd transmitata
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Run the development server:**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `GET /api/v1/route/<route_name>` - Get routes by name
- `GET /api/v1/route/<route_name>/find` - Search routes by name
- `GET /api/v1/stations/<route_id>/find` - Get stations for a route
- `GET /api/v1/collections/` - List all route collections
- `GET /api/v1/collections/<id>` - Get a specific collection with detail

## Running Tests

### Run all Django tests:
```bash
make tests
```

### Run specific test modules:
```bash
# API tests
python manage.py test api.tests

# Web tests
python manage.py test web.tests

# Specific test class
python manage.py test api.tests.models.RouteModelTest
```

### Run with pytest:
```bash
# Run a single test
make test

# Run specific test file
make test-file FILE=test_single.py

# Run specific test function
make test-file FILE=test_single.py::test_example
```

## Development Commands

```bash
# Start Docker services (if using Docker)
make start

# Access Docker container shell
make shell

# Show all available commands
make help
```

## Dependencies

- Django 4.2.27
- Django REST Framework 3.16.1
- pytest-django 4.11.1
- requests 2.32.3

## License

This project is for demonstration purposes.