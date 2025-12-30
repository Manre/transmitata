from django.test import TestCase
from api.models import Route, RouteCollection


class RouteModelTest(TestCase):
    """Test cases for Route model"""

    def setUp(self):
        """Set up test data"""
        self.route = Route.objects.create(
            code="T1",
            identification=123,
            description="Transmilenio Line 1"
        )

    def test_route_creation(self):
        """Test Route object creation"""
        self.assertIsInstance(self.route, Route)
        self.assertEqual(self.route.code, "T1")
        self.assertEqual(self.route.identification, 123)
        self.assertEqual(self.route.description, "Transmilenio Line 1")

    def test_route_str_representation_with_description(self):
        """Test Route string representation with description"""
        expected_str = "T1 (Transmilenio Line 1)"
        self.assertEqual(str(self.route), expected_str)

    def test_route_str_representation_without_description(self):
        """Test Route string representation without description"""
        route = Route.objects.create(
            code="T2",
            identification=456
        )
        self.assertEqual(str(route), "T2")

    def test_route_unique_identification(self):
        """Test that identification field is unique"""
        # Create first route
        Route.objects.create(code="T3", identification=789)

        # Try to create another route with same identification - should fail
        with self.assertRaises(Exception):
            Route.objects.create(code="T4", identification=789)


class RouteCollectionModelTest(TestCase):
    """Test cases for RouteCollection model"""

    def setUp(self):
        """Set up test data"""
        self.route1 = Route.objects.create(
            code="T1",
            identification=123,
            description="Transmilenio Line 1"
        )
        self.route2 = Route.objects.create(
            code="T2",
            identification=456,
            description="Transmilenio Line 2"
        )
        self.route_collection = RouteCollection.objects.create(
            name="Main Routes"
        )
        self.route_collection.routes.add(self.route1, self.route2)

    def test_route_collection_creation(self):
        """Test RouteCollection object creation"""
        self.assertIsInstance(self.route_collection, RouteCollection)
        self.assertEqual(self.route_collection.name, "Main Routes")
        self.assertEqual(self.route_collection.routes.count(), 2)

    def test_route_collection_str_representation(self):
        """Test RouteCollection string representation"""
        self.assertEqual(str(self.route_collection), "Main Routes")

    def test_route_collection_many_to_many_relationship(self):
        """Test many-to-many relationship with Route model"""
        routes = self.route_collection.routes.all()
        self.assertIn(self.route1, routes)
        self.assertIn(self.route2, routes)

    def test_route_collection_empty_routes(self):
        """Test RouteCollection with no routes"""
        empty_collection = RouteCollection.objects.create(name="Empty Collection")
        self.assertEqual(empty_collection.routes.count(), 0)