let BasemapAT_basemap = L.tileLayer('https://maps{s}.wien.gv.at/basemap/geolandbasemap/{type}/google3857/{z}/{y}/{x}.{format}', {
	attribution: 'Datenquelle: <a href="https://www.basemap.at">basemap.at</a>',
	subdomains: ["", "1", "2", "3", "4"],
	type: 'normal',
	format: 'png',
});

let map = L.map("resort-map", {
    layers: [BasemapAT_basemap],
    center: [lat, lon],
    minZoom: 9,
}).setView([lat, lon], 14);

map.setMaxBounds([
    [47.24078888513102, 11.585583235700277],
    [46.14847360151397, 16.633618011003204]
]);

let skiIcon = new L.Icon({
    iconUrl: "../../../media/ski-icon2.png",
    iconSize: [25, 25],
    iconAnchor: [10, 25]
});

let marker = L.marker([lat, lon], {
    icon: skiIcon
}).addTo(map);