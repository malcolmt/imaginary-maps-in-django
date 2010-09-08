from django.contrib.gis import admin

from lands import models
from utils.admin_helper import AdminBase

admin.site.register(models.Land, AdminBase)

