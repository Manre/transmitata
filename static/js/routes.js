function get_route(route_code){
    var settings = {
        "url": "/api/v1/route/" + route_code,
        "method": "GET",
    };

    window.map.fireEvent('dataloading');
    $.ajax(settings).done(function (points) {
        window.map.fireEvent('dataload');
        if (points.length > 0){
            display_map(points);
        }
    });

    setTimeout(
        function(){
            get_route(route_code);
        },
        5 * 1000  // 5 seconds
    );
};

function display_map(points) {
    window.markerGroup.clearLayers()
    var options = {
      icon: 'bus',
      iconShape: 'marker'
    };

    for (var i = 0; i < points.length; i++) {
        var latitude = points[i]["latitude"];
        var longitude = points[i]["longitude"];
        var route_name = points[i]["route_name"];
        var bus_id = points[i]["bus_id"];
        var title = bus_id + ' - ' + route_name;

        marker = new L.marker([latitude,longitude], {
            icon: L.BeautifyIcon.icon(options),
            draggable: false
        }).bindPopup(title).addTo(window.markerGroup);

        update_bus_path(bus_id, latitude, longitude);
    }
}

function update_bus_path(bus_id, latitude, longitude) {
    var old_path = {
        "lat": (
            window.bus_routes_path.hasOwnProperty(bus_id) ? (
                window.bus_routes_path[bus_id].hasOwnProperty("new_path") ? (
                    window.bus_routes_path[bus_id]["new_path"].hasOwnProperty("lat") ? window.bus_routes_path[bus_id]["new_path"]["lat"] : null
                ) : null
            ) : null
        ),
        "lon": (
            window.bus_routes_path.hasOwnProperty(bus_id) ? (
                window.bus_routes_path[bus_id].hasOwnProperty("new_path") ? (
                    window.bus_routes_path[bus_id]["new_path"].hasOwnProperty("lon") ? window.bus_routes_path[bus_id]["new_path"]["lon"] : null
                ) : null
            ) : null
        )
    };

    var new_path = {
        "lat": latitude,
        "lon": longitude,
    };

    if (old_path["lat"] === null){
        window.bus_routes_path[bus_id] = {
            "new_path": new_path,
            "old_path": new_path,
            "vector": null,
        };
    }

    if (old_path["lat"] !== null && old_path["lat"] !== new_path["lat"]){
        if (window.bus_routes_path[bus_id].hasOwnProperty("vector") && window.bus_routes_path[bus_id]["vector"] !== null){
            window.arrowsGroup.removeLayer(window.bus_routes_path[bus_id]["vector"]);
        };

        vector_coordinates = [
            [old_path["lat"], old_path["lon"]],
            [new_path["lat"], new_path["lon"]]
        ]

        var arrow = L.polyline([vector_coordinates]);
        var arrowHead = L.polylineDecorator(arrow, {
            patterns: [
                {
                    offset: '100%',
                    symbol: L.Symbol.arrowHead({pixelSize: 10, polygon: false, pathOptions: {stroke: true}})
                }
            ]
        });
        var myVector = L.layerGroup([arrow, arrowHead]);
        window.arrowsGroup.addLayer(myVector);

        window.bus_routes_path[bus_id] = {
            "new_path": new_path,
            "old_path": old_path,
            "vector": myVector,
        };
    }
}

function find_route(route_name) {
    var settings = {
        "url": "/api/v1/route/" + route_name + "/find",
        "method": "GET",
    };

    $.ajax(settings).done(function (response) {
        var routes = [];
        for (let i = 0; i < response.length; i++) {
            var route_code = response[i]["route_code"];
            var route_id = response[i]["route_id"];
            var route_name = response[i]["route_name"];
            var display_name = route_code + ', ' + route_name;
            var route = {"display_name": display_name, "route_code": route_code, "route_id": route_id};

            routes.push(route);
        };
        display_routes(routes);
    });
};

function display_routes(routes) {
    $("#routes_list").empty();

    var params_from_url_as_dict = get_params_as_json_from_url();
    for (let i = 0; i < routes.length; i++) {
        var route_code = routes[i]['route_code'];
        var route_id = routes[i]['route_id'];
        var display_name = routes[i]['display_name'];

        var url_params_dict = {"route_code": route_code, "route_id": route_id}
        var merged_dictionaries = Object.assign({}, params_from_url_as_dict, url_params_dict);
        var url_params_text = build_url_from_dictionary(merged_dictionaries);

        a_text = `<a href='?${url_params_text}'>${display_name}</a>`;
        li_text = `<li>${a_text}</li>`;

        $('#routes_list').append(li_text);
    }
};