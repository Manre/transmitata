function get_stations(route_id){
    var settings = {
        "url": window.AppConstants.API.STATIONS + "/" + route_id + '/find',
        "method": "GET",
    };

    $.ajax(settings).done(function (stations) {
        if (stations.length > 0){
            display_stations_in_map(stations);
        }
    });
};

function display_stations_in_map(stations) {
    var options = window.AppConstants.ICONS.STATION;

    for (var i = 0; i < stations.length; i++) {
        var latitude = stations[i]["lat"];
        var longitude = stations[i]["lon"];
        var title = 'Estación';

        marker = new L.marker([latitude,longitude], {
            icon: L.BeautifyIcon.icon(options),
            draggable: false
        }).bindPopup(title).addTo(window.stationsGroup);
    }
}