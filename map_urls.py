import os

from django.conf import settings
from django.conf.urls.defaults import *     # pylint: disable-msg=W0401,W0614
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    ("", include("interface.urls")),
)

if settings.DEV_MODE:
    static_path = os.path.join(settings.PROJ_ROOT, "media")
    urlpatterns += patterns("",
        ("^static/(.*)$", serve, {"document_root": static_path}),
        ('^(favicon.ico)$', serve, {"document_root": static_path}),
    )

