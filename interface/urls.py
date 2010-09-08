from django.conf.urls.defaults import *     # pylint: disable-msg=W0401,W0614
from django.views.generic.simple import direct_to_template

from interface import views

urlpatterns = patterns('',
    ("^$", direct_to_template, {"template": "interface/simple.html",
            "extra_context": {"title": "Imaginary Island Map"}}),
    ("^tracks/$", views.tracks),
    ("^places/$", views.places),
)

