$(document).ready(function() {
    var bus_routes_path = {};
    let config = {
        maxZoom: 18,
    };
    const zoom = 13;
    const lat = 4.7090;
    const lng = -74.0649;

    const map = L.map("map", config).setView([lat, lng], zoom);

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
    var markerGroup = L.layerGroup().addTo(map);
    var stationsGroup = L.layerGroup().addTo(map);
    var arrowsGroup = L.layerGroup().addTo(map);

    if (document.readyState === 'complete') {
      check_for_route_in_url();
      get_list_of_route_collections();
    } else {
      window.addEventListener('load', function() { check_for_route_in_url(); });
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

    function get_route(route_code){
        var settings = {
            "url": "api/v1/route/" + route_code,
            "method": "GET",
        };

        map.fireEvent('dataloading');
        $.ajax(settings).done(function (points) {
            map.fireEvent('dataload');
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
        markerGroup.clearLayers()
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
            }).bindPopup(title).addTo(markerGroup);

            var old_path = {
                "lat": (
                    bus_routes_path.hasOwnProperty(bus_id) ? (
                        bus_routes_path[bus_id].hasOwnProperty("new_path") ? (
                            bus_routes_path[bus_id]["new_path"].hasOwnProperty("lat") ? bus_routes_path[bus_id]["new_path"]["lat"] : null
                        ) : null
                    ) : null
                ),
                "lon": (
                    bus_routes_path.hasOwnProperty(bus_id) ? (
                        bus_routes_path[bus_id].hasOwnProperty("new_path") ? (
                            bus_routes_path[bus_id]["new_path"].hasOwnProperty("lon") ? bus_routes_path[bus_id]["new_path"]["lon"] : null
                        ) : null
                    ) : null
                )
            };

            var new_path = {
                "lat": latitude,
                "lon": longitude,
            };

            if (old_path["lat"] === null){
                bus_routes_path[bus_id] = {
                    "new_path": new_path,
                    "old_path": new_path,
                    "vector": null,
                };
            }

            if (old_path["lat"] !== null && old_path["lat"] !== new_path["lat"]){
                if (bus_routes_path[bus_id].hasOwnProperty("vector") && bus_routes_path[bus_id]["vector"] !== null){
                    arrowsGroup.removeLayer(bus_routes_path[bus_id]["vector"]);
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
                arrowsGroup.addLayer(myVector);

                bus_routes_path[bus_id] = {
                    "new_path": new_path,
                    "old_path": old_path,
                    "vector": myVector,
                };
            }

        }
    }

    // Find route

    $("#find_route_form").submit(function(e){
        e.preventDefault(e);

        var route_name = $("#route_name").val();

        routes = find_route(route_name);
    });

    function get_list_of_route_collections() {
        var settings = {
            "url": "api/v1/collections/",
            "method": "GET",
        };

        $.ajax(settings).done(function (route_collections) {
            display_list_of_route_collections(route_collections);
        });
    };

    function get_routes_for_bookmark(bookmark) {
        var settings = {
            "url": `api/v1/collections/${bookmark}/`,
            "method": "GET",
        };

        $.ajax(settings).done(function (routes) {
            display_routes_from_bookmark(routes);
        });
    };

    function find_route(route_name) {
        var settings = {
            "url": "api/v1/route/" + route_name + "/find",
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

    function display_list_of_route_collections(route_collections) {
        $("#route_collections").empty();

        for (let i = 0; i < route_collections.length; i++) {
            var route_collection_id = route_collections[i]['id'];
            var route_collection_name = route_collections[i]['name'];

            a_text = `<a href='/?bookmark=${route_collection_id}#SHOW_MAP'>${route_collection_name}</a>`;
            li_text = `<li> ${a_text} </li>`;

            $('#route_collections').append(li_text);
        }
    };

    function display_routes_from_bookmark(response) {
        $("#bookmarks").empty();
        var routes = response["routes"];
        var response_length = Object.keys(response).length;

        if (response_length > 0){
            $("#buses_collections").show();
        }

        var params_from_url_as_dict = get_params_as_json_from_url();
        for (let i = 0; i < routes.length; i++) {
            var route_code = routes[i]['code'];
            var route_identification = routes[i]['identification'];

            var url_params_dict = {"route_code": route_code, "route_id": route_identification}
            var merged_dictionaries = Object.assign({}, params_from_url_as_dict, url_params_dict);
            var url_params_text = build_url_from_dictionary(merged_dictionaries);

            a_text = `<a href='?${url_params_text}#SHOW_MAP'>${route_code}</a>`;
            li_text = `<li style='display: inline;'> ${a_text} </li>`;

            $('#bookmarks').append(li_text);
        }
    };

    // Stations

    function get_stations(route_id){
        var settings = {
            "url": "api/v1/stations/" + route_id + '/find',
            "method": "GET",
        };

        $.ajax(settings).done(function (stations) {
            if (stations.length > 0){
                display_stations_in_map(stations);
            }
        });
    };

    function display_stations_in_map(stations) {
        var options = {
          icon: 'bus',
          borderColor: '#b3334f',
          textColor: '#b3334f'
        };

        for (var i = 0; i < stations.length; i++) {
            var latitude = stations[i]["lat"];
            var longitude = stations[i]["lon"];
            var title = 'Estación';

            marker = new L.marker([latitude,longitude], {
                icon: L.BeautifyIcon.icon(options),
                draggable: false
            }).bindPopup(title).addTo(stationsGroup);
        }
    }

    // Utils

    function build_url_from_dictionary(elements) {
        const toUrlEncoded = obj => Object.keys(obj).map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])).join('&');
        return toUrlEncoded(elements);
    }

    function get_params_as_json_from_url(){
        var params_as_url = Object.fromEntries(new URLSearchParams(location.search));
        return params_as_url;
    };

});