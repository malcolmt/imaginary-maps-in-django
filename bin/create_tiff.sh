#!/bin/bash

# Creates the island-base.tiff file that is used by Mapnik as a base layer. The
# resulting file is ~20M in size (compared to 4.5M source PNG), so checking it
# into the version repo isn't very practical.

here=$(dirname $0)
cd $here/../media/maps

ULLR="150 0 150.11498435636727 -0.086819436124827731"
gdal_translate -a_srs epsg:4326 -a_ullr $ULLR island-base.png island-base.tiff

