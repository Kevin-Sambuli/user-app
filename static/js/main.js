var map;

const basemaps = {
            "OpenStreetMaps": L.tileLayer(
                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
                    minZoom: 2,
                    maxZoom: 19,
                    id: "osm.streets"
                }
            ),
        };


// Map Options
var mapOptions = {
    zoomControl: false,
    attributionControl: false,
    center: [-1.22488, 36.827164],
    minZoom: 6.2,
    zoom: 6.2,
    layers: [basemaps.OpenStreetMaps],
};


//create the map object
map = L.map('map', mapOptions);

// scale control layer
L.control.scale({
    metric: true,
    imperial: false,
    updateWhenIdle: true,
    maxWidth: 200
}).addTo(map);


L.control.zoom({position: "topleft"}).addTo(map);

// Creating an attribution with an Attribution options
var attrOptions = {
    prefix: 'Made by Kevin Sambuli'
};


var attr = L.control.attribution(attrOptions).addTo(map);

