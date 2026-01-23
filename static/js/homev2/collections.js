function get_list_of_route_collections() {
    var settings = {
        "url": window.AppConstants.API.COLLECTIONS + "/",
        "method": "GET",
    };

    $.ajax(settings).done(function (route_collections) {
        display_list_of_route_collections(route_collections);
    });
};

function get_routes_for_bookmark(bookmark) {
    var settings = {
        "url": window.AppConstants.API.COLLECTIONS + `/${bookmark}/`,
        "method": "GET",
    };

    $.ajax(settings).done(function (routes) {
        display_routes_from_bookmark(routes);
    });
};

function display_list_of_route_collections(route_collections) {
    $("#" + window.AppConstants.UI.COLLECTIONS_LIST).empty();

    for (let i = 0; i < route_collections.length; i++) {
        var route_collection_id = route_collections[i]['id'];
        var route_collection_name = route_collections[i]['name'];

        a_text = `<a href='/?bookmark=${route_collection_id}#SHOW_MAP'>${route_collection_name}</a>`;
        li_text = `<li> ${a_text} </li>`;

        $('#' + window.AppConstants.UI.COLLECTIONS_LIST).append(li_text);
    }
};

function display_routes_from_bookmark(response) {
    $("#" + window.AppConstants.UI.BOOKMARKS_LIST).empty();
    var routes = response["routes"];
    var response_length = Object.keys(response).length;

    if (response_length > 0){
        $("#" + window.AppConstants.UI.BUSES_COLLECTIONS).show();
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

        $('#' + window.AppConstants.UI.BOOKMARKS_LIST).append(li_text);
    }
};