# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TransmiTata is a Django-based web application for tracking Transmilenio bus routes in Bogotá, Colombia. It integrates with external transportation APIs to provide real-time bus locations and route information through REST APIs and web interfaces.

## Commands

### Testing
```bash
make tests                                    # Run all Django tests (api + web apps)
python manage.py test api.tests              # Run API tests only
python manage.py test web.tests              # Run web tests only
python manage.py test api.tests.test_models.RouteModelTest  # Run specific test class
pytest api/tests/test_services.py::TestGetRoutes::test_success  # Run specific test with pytest
```

### Development
```bash
python manage.py runserver                   # Start development server (localhost:8000)
python manage.py migrate                     # Apply database migrations
python manage.py makemigrations              # Create new migrations
python manage.py shell_plus                  # Enhanced Django shell (via django-extensions)
```

### Docker
```bash
make start                                   # Start docker-compose services
make shell                                   # Open bash in transmitata-web-1 container
```

## Architecture

### Django Apps

**`api/`** - REST API for transportation data
- `services.py` - External API integrations (Transmilenio APIs)
- `views.py` - API views: RoutesView, FindRoutesView, FindStationsForRoute, RouteCollectionViewSet
- `models.py` - Route and RouteCollection models
- `serializers.py` - DRF serializers

**`web/`** - Web interface with template-based views (HomeView, HomeV2View)

**`transmitata/`** - Django project configuration

### External API Services (api/services.py)

Three main functions integrate with Transmilenio APIs:
- `get_routes(route_name)` - Fetches real-time bus locations
- `find_route_by_name(route_name)` - Searches routes by name
- `find_stations_for_route(route_id)` - Gets stations/coordinates for a route

All service functions return empty lists on errors (timeouts, connection errors, invalid responses) with logging.

### API Endpoints

```
GET /api/v1/route/<route_name>         - Get real-time bus locations for a route
GET /api/v1/route/<route_name>/find    - Search routes by name
GET /api/v1/stations/<route_id>/find   - Get stations for a route
GET /api/v1/collections/               - List route collections
GET /api/v1/collections/<id>           - Get specific collection with routes
```

### Data Models

- **Route**: `code` (CharField), `identification` (IntegerField, unique), `description` (optional)
- **RouteCollection**: `name` (CharField), `routes` (ManyToMany to Route)

## Testing

Tests use Django's test framework with pytest integration. Pytest markers: `unit`, `integration`, `slow`.

Test structure mirrors app structure:
- `api/tests/test_models.py` - Model tests
- `api/tests/test_views.py` - API view tests
- `api/tests/test_services.py` - Service tests (mocked external APIs)
- `web/tests/test_views.py` - Web view tests

External API calls in tests are mocked using `unittest.mock.patch`.
