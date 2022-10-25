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
    "Dark": L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        {maxZoom: 20}
    ),
    "OpenTopoMap": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        {maxZoom: 17}
    ),
};


// Map Options
var mapOptions = {
    zoomControl: false,
    attributionControl: false,
    center: [-1.22488, 36.827164],
    minZoom: 6.2,
    zoom: 6.2,
    layers: [basemaps.Dark],
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

