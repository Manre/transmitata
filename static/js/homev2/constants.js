// Application Constants
window.AppConstants = {
    // Map Configuration
    MAP: {
        DEFAULT_ZOOM: 13,
        MAX_ZOOM: 18,
        DEFAULT_LAT: 4.7090,
        DEFAULT_LNG: -74.0649,
        TILE_URL: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        TILE_ATTRIBUTION: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    },
    
    // API Endpoints
    API: {
        BASE_URL: "/api/v1",
        ROUTES: "/api/v1/route",
        STATIONS: "/api/v1/stations", 
        COLLECTIONS: "/api/v1/collections"
    },
    
    // Update Intervals
    INTERVALS: {
        ROUTE_UPDATE: 5000 // 5 seconds
    },
    
    // Map Icons and Styles
    ICONS: {
        BUS: {
            icon: 'bus',
            iconShape: 'marker'
        },
        STATION: {
            icon: 'bus',
            borderColor: '#b3334f',
            textColor: '#b3334f'
        }
    },
    
    // UI Elements IDs
    UI: {
        MAP: "map",
        ROUTE_FORM: "find_route_form",
        ROUTE_NAME_INPUT: "route_name",
        ROUTES_LIST: "routes_list",
        COLLECTIONS_LIST: "route_collections",
        BOOKMARKS_LIST: "bookmarks",
        BUSES_COLLECTIONS: "buses_collections"
    }
};