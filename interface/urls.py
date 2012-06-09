from django.conf.urls.defaults import patterns, url
from django.views import generic

from interface import views


class TemplateView(generic.TemplateView):
    template_name = "interface/simple.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context["title"] = "Imaginary Island Map"
        return context


urlpatterns = patterns('',
    url("^$", TemplateView.as_view()),
    url("^tracks/$", views.tracks),
    url("^places/$", views.places),
)

