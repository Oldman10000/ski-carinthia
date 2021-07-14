$(document).ready(function () {

    // checks scroll position and changes navbar colour accordingly
    function checkScrollPosition() {
        var scroll = $(window).scrollTop();
        if (scroll >= 600) {
            $('header').removeClass('bg-transparent').addClass('bg-blue');
        } else {
            $('header').removeClass('bg-blue').addClass('bg-transparent');
        }
    }

    // checks window size and activates navbar colour function for large screens
    function largeOnlyNav() {
        if ($(window).width() > 960) {

            checkScrollPosition();

            $(window).scroll(function () {
                checkScrollPosition();
            });
        }
    }

    largeOnlyNav();

    // checks window size and changes navbar colour accordingly
    function checkNav() {
        if ($(window).width() < 960) {
            $('header').removeClass('bg-transparent').addClass('bg-blue');
            $('nav').removeClass('bg-transparent').addClass('bg-blue');
        } else {
            $('header').addClass('bg-transparent').removeClass('bg-blue');
            $('nav').addClass('bg-transparent').removeClass('bg-blue');
        }
    }

    checkNav();

    // if window size is changed by user
    $(window).resize(function () {
        largeOnlyNav();
        checkNav();
    });

    // button to scroll to next section
    $('.scroll-down').click(function () {
        $('html, body').animate({
            scrollTop: $('#index-main').offset().top
        }, 'slow');
        return false;
    });
});

let mapTileLayers = L.tileLayer(
    "http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
        attribution: "Powered by <a href='https://developers.arcgis.com/terms/attribution/' target='_blank' rel='noopener'>Esri</a>"
    });
let map = L.map("index-map", {
    layers: [mapTileLayers],
    center: [46.787590850347605, 13.87062293485363],
    minZoom: 9,
}).setView([46.79, 13.95], 9);

map.setMaxBounds([
    [47.24078888513102, 11.585583235700277],
    [46.14847360151397, 16.633618011003204]
]);
let skiIcon = new L.Icon({
    iconUrl: "../../../media/ski-icon2.png",
    iconSize: [25, 25],
    iconAnchor: [10, 25]
});

resorts.forEach(resort => {

    let xReference = resort.fields.x_map_reference;
    let yReference = resort.fields.y_map_reference;

    let url = "{% url 'resort_detail' 99998888 %}".replace("99998888", resort.pk);

    let marker = L.marker([xReference, yReference], {
        icon: skiIcon
    }).addTo(map).bindPopup(`
            <h6><a href="${url}">${resort.fields.name}</a></h6>
            <p class="m-0">${resort.fields.street_address_1}</p>
            <p class="m-0">${resort.fields.street_address_2}</p>
            <p class="m-0">${resort.fields.postcode} ${resort.fields.town_or_city}</p>
            <p class="mt-0">${resort.fields.phone_number}</p>
            `);

});