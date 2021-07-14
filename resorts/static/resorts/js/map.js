let mapTileLayers = L.tileLayer(
    "http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
        attribution: "Powered by <a href='https://developers.arcgis.com/terms/attribution/' target='_blank' rel='noopener'>Esri</a>"
    });

const map = L.map("resort-map", {
    layers: [mapTileLayers],
    center: [lat, lon],
    zoom: 2
}).setView([lat, lon], 11);

const skiIcon = new L.Icon({
    iconUrl: "../../../media/ski-icon2.png",
    iconSize: [25, 25],
    iconAnchor: [10, 25]
});

let marker = L.marker([lat, lon], {
    icon: skiIcon
}).addTo(map);