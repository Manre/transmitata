from django.db import models


class Route(models.Model):
    code = models.CharField(max_length=30)
    identification = models.IntegerField(unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.code} ({self.description})" if self.description else f"{self.code}"


class RouteCollection(models.Model):
    name = models.CharField(max_length=100)
    routes = models.ManyToManyField(Route)

    def __str__(self):
        return f"{self.name}"
