========================
Maps of Imaginary Lands
========================

Introduction
=============

Supporting code and slides for a talk introducing customised usage of Django's
GIS components, Mapnik and OpenLayers. Originally presented at DjangoCon-US,
September 2010 (Portland, Oregon, USA) in a short form and then at Kiwi Pycon
(Bay of Islands, New Zealand) in November, 2010 and PyCon-APAC in June, 2012.

Short Description
------------------

The GIS features of Django aren't restricted to being applied to real world
maps and planets. This talk will show how to display and interact with maps of
imaginary lands, such as game maps or lands in science fiction novels. We'll
uncover a bit of how Django GIS works in the process, separating the map
display from the modelling.

Abstract
---------

Whilst ``django.contrib.gis`` isn't particularly difficult to get started with,
particularly if you follow the tutorials, it can sometimes seem a bit
overwhelming in the way it goes from zero to fancy maps in only a couple of
steps. I'd like to demystify some of the pieces of the stack, pulling apart the
modelling support — specifying the data are we trying to work with — from the
display and client-side portion.

To make this more than a dry technical dive, I'll show how to add extras to an
imaginary map, rather than something pulled from Google Maps or Open Street
Map. We'll take on the task of plotting features on a landscape from a
potential role-playing game and show how the GIS data manipulation features,
such as calculating region intersections, nearby points, and Javascript
client-side display work the in a familiar way against this slightly unusual
background.

Some basic familiarity with Django's GIS features would be useful for this
talk, although it might also serve as a motivating introduction to trying
things out.

Aside: Creating map graphics
-----------------------------

Over the years, a number of people have asked how I created the island map
image for this presentation.

The main graphic was done using the Gimp_, following tutorials at `The
Cartographer's Guild`_ website. I have spent hours playing with their
map-making tutorials and trying out different things.

The shapefiles describing the island boundaries and paths and points of
interest were creating in QGis_, a professional level tool that is highly accessible to amateurs and with a very supportive online community of tutorials and tips.

.. _Gimp: http://http://www.gimp.org/
.. _The Cartographer's Guild: http://www.cartographersguild.com/
.. _QGis: http://www.qgis.org/

Setting up
===========

This code is intended as a small self-contained, executable example, written
with reasonably professional coding standards in mind.

All the code here has been verified to run against Django 1.4 (as of June, 2012).

That being said, a few prerequisites need to be installed in order to run the
example. I am assuming you have worked through the ``django.contrib.gis``
tutorial_ and thus have all the necessary prerequisites installed. If you can
view any Django admin page that involves GIS information, you have met the
requirements here.

Secondly, you'll need to have Mapnik_ installed (and Mapnik's Python bindings).
Major Linux distributions will ship these as packages that won't require
anything more than a ``yum install ...`` or ``aptitude install...``. I've been
led to believe it isn't amazingly difficult to get the necessary pieces
installed on a Mac OS X and Windows as well [1]_. If you can run the following
at a Python prompt and no exception is raised, you have the necessary
components installed::

    >>> from mapnik2 import ogcserver

This assumes you are running mapnik-python version 2.0. If you are using an
earlier version (0.7) of mapnik and mapnik-python, you will need to import
``mapnik``, rather than ``mapnik2`` [2]_. There are obviously other differences
between the earlier and later versions of mapnik, however, for the most part,
things are forwards compatible and the code here will work without change once
the import is correct.

.. _tutorial: http://docs.djangoproject.com/en/1.2/ref/contrib/gis/tutorial/
.. _Mapnik: http://mapnik.org/

The included settings file is set up to use Postgis as the database. I don't
believe anything Postgis-specific is used in the code, however, so any spatial
database backend should work (again, being able to work through the Django GIS
tutorial is probably both necessary and sufficient).

To do a setup from scratch (assuming Postgis for the first step), I ran the
following steps, in order:

1. Create the GIS-aware database: ``createdb -T template_postgis
   imaginary_lands``. Assumes you already have ``template_postgis`` created as
   per Geodjango setup instructions.
2. ``python manage.py syncdb --noinput`` to do the basic model creation. This
   will load an initial fixtures file to create an admin user. The username
   and password for this user are both "*admin*" (without the quotes).
3. ``python manage.py import_lands`` and ``python manage.py import_adventures``
   to load initial shape data into the GIS models.
4. Create the GeoTiff version of the base map (only the PNG version is checked
   in)::

        bin/create_tiff.sh

   This is a shell script that uses some GDAL utilities to make the conversion
   (Windows users may need to find an equivalent alternative).

You then need to start both the Django development webserver and a local Mapnik
server. Start the Mapnik server by::

    cd map_server
    python wms.py

That will launch the server on port 8001. Start Django's development server
with the usual::

    python manage.py runserver

You can now browse to http://localhost:8000/ to see the island map with a few
features enabled (try zooming in or panning around), or
http://localhost:8000/admin/ to view the same data in the admin interface, with
the imaginary island base map, instead of the normal world map.

Navigating the code
====================

Hopefully the code is written and commented clearly enough that somebody
familiar with Django can follow along. I have tried to write in a non-throwaway
style, so any code you see here is how I would do something in production.

The standalone Mapnik server configuration is all in the ``map_server/``
directory. The only piece that is particular to a local development
installation is ``wms.py``. Otherwise one would do a normal ``mod_wsgi``
installation (for example) to call ``map_factory.py`` in a production
environment.

The ``lands/`` and ``adventure/`` directories are two small Django apps that
purely manage the GIS data. Have a look at the models there, as well as the
data import scripts in ``lands/management/commands/import_land.py`` and
similarly in the ``adventure/`` directory. Fairly standard GeoDjango import
techniques being used there. Also note the ``admin.py`` files in both
directories and how the overrides to use my imaginary map is set up via
``utils/admin_helper.py``. Each directory contains a ``data/`` subdirectory
that contains the raw shape files that are imported into GeoDjango. You can
inspect those with tools like ``ogrinfo``, as described in the GeoDjango
tutorial.

The ``interface/`` directory contains the main HTML-generating view, as well as
the views that are called by OpenLayers to populate the data (it's the web
interface for the data). These would be a fair bit more fleshed out in a "real
world" application, but they are correct for the small-scale operation here.
The javascript code in ``interface/templates/interface/simple.html`` is also a
key part of this functionality.

Best of luck!

Malcolm Tredinnick
(Sydney, Australia)

.. [1] I have no direct experience with either platform. However, a credible
       source wrote to say that installing Mapnik and Python bindings on
       Windows XP, SP2 was *"a breeze."*

.. [2] In Mapnik 2.1, the Python module will again be called ``mapnik``. Then
       ``mapnik2`` name was to allow 0.7 and 2.0 to be run in parallel for a
       while.

