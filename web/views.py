from django.views.generic.base import TemplateView

from transmitata.__version__ import VERSION


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = VERSION
        return context
