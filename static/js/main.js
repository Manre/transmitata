// Global variables
window.bus_routes_path = {};
window.map = null;
window.markerGroup = null;
window.stationsGroup = null;
window.arrowsGroup = null;

$(document).ready(function() {
    initializeMap();
    setupEventListeners();
    
    if (document.readyState === 'complete') {
        check_for_route_in_url();
        get_list_of_route_collections();
    } else {
        window.addEventListener('load', function() { check_for_route_in_url(); });
    }
});

function initializeMap() {
    let config = {
        maxZoom: 18,
    };
    const zoom = 13;
    const lat = 4.7090;
    const lng = -74.0649;

    window.map = L.map("map", config).setView([lat, lng], zoom);

    L.control.locate({
        setView: false,
        flyTo: true,
        keepCurrentZoomLevel: true,
    }).addTo(map);

    var loadingControl = L.Control.loading({
        separate: true
    });
    map.addControl(loadingControl);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
    
    window.markerGroup = L.layerGroup().addTo(map);
    window.stationsGroup = L.layerGroup().addTo(map);
    window.arrowsGroup = L.layerGroup().addTo(map);
}

function setupEventListeners() {
    $("#find_route_form").submit(function(e){
        e.preventDefault(e);
        var route_name = $("#route_name").val();
        find_route(route_name);
    });
}

function check_for_route_in_url(){
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });

    let route_code = params.route_code;
    let route_id = params.route_id;
    let bookmark = params.bookmark;

    if (bookmark !== null){
        get_routes_for_bookmark(bookmark);
    }

    if (route_code !== null && route_id !== null){
        $("#route_name").val(route_code);
        get_route(route_code);
        get_stations(route_id);
    }
};