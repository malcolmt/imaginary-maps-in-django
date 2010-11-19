var map;
// The bounding box and centre of the region we're interested in displaying.
var ul_lon = 150.0;
var ul_lat = 0.0;
var lr_lon = 150.114984356;
var lr_lat = -0.0868194361248;
var center_lon = 150.057492178;
var center_lat = -0.0434097180624;

function init() {
    var layer, options;
    var base = (lr_lon - ul_lon) / 800.0;

    options = {
        tileSize: new OpenLayers.Size(400, 300),
        resolutions: [base, base/2, base/4, base/8]
    };
    map = new OpenLayers.Map("map", options);
    layer = new OpenLayers.Layer.WMS("Imaginary World",
            "http://127.0.0.1:8001/",
            {layers: "base", format: "image/png"});
    map.addLayer(layer);
    map.setCenter(new OpenLayers.LonLat(center_lon, center_lat));
    map.addControl(new OpenLayers.Control.LayerSwitcher());

    layer = new OpenLayers.Layer.WFS("Tracks", "/tracks/", {},
            {format: OpenLayers.Format.KML});
    map.addLayer(layer);
    layer = new OpenLayers.Layer.WFS("Notable points", "/places/", {},
            {format: OpenLayers.Format.KML});
    map.addLayer(layer);
}

