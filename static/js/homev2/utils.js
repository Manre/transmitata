function build_url_from_dictionary(elements) {
    const toUrlEncoded = obj => Object.keys(obj).map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])).join('&');
    return toUrlEncoded(elements);
}

function get_params_as_json_from_url(){
    var params_as_url = Object.fromEntries(new URLSearchParams(location.search));
    return params_as_url;
};