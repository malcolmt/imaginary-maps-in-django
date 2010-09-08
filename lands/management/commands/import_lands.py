#!/usr/bin/env python
"""
Loads land outline data into the Land model.
"""

import os

from django.contrib.gis import utils
from django.core.management import base
from django.db.models import F
from django.db.models.expressions import ExpressionNode

from lands import models


FILE = "../../data/land.shp"

class Command(base.NoArgsCommand):
    def handle_noargs(self, **options):
        verbosity = bool(int(options.get("verbosity", 1)))

        filename = os.path.join(os.path.dirname(__file__), FILE)
        layermapping = utils.LayerMapping(models.Land, filename,
                models.land_layermap)
        layermapping.save(strict=True, verbose=verbosity)

        # Many of the names of these lands will be the empty string, so lets
        # tweak that slightly (call them Unknown-1, Unknown-2, etc).
        models.Land.objects.filter(name="").update(
                name=Concat("Unknown-").concat(F("id")))


class Concat(ExpressionNode):
    """
    Append a string prefix to another value as the RHS of an update set.
    """
    def __init__(self, prefix):
        super(Concat, self).__init__(None, None, False)
        self.prefix = prefix

    def concat(self, other):
        return self._combine(other, "||", False)

    def evaluate(self, evaluator, qn, connection):
        return u"%s", (self.prefix,)

