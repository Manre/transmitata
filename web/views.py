from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class HomeV2View(TemplateView):
    template_name = "homev2.html"
