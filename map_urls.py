import os

from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    ("", include("interface.urls")),
)

if settings.DEV_MODE:
    from django.views.static import serve

    static_path = os.path.join(settings.PROJ_ROOT, "media")
    urlpatterns += patterns("",
        ("^static_data/(.*)$", serve, {"document_root": static_path}),
        ('^(favicon.ico)$', serve, {"document_root": static_path}),
    )

