$(document).ready(function () {

    // checks scroll position and changes navbar colour accordingly
    function checkScrollPosition() {
        var scroll = $(window).scrollTop();
        if (scroll >= 600) {
            $('header').removeClass('bg-transparent').addClass('bg-blue');
        } else {
            $('header').addClass('bg-transparent').removeClass('bg-blue');
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
        } else {
            $('header').addClass('bg-transparent').removeClass('bg-blue');
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

    var mapTileLayers = L.tileLayer(
        "http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
            attribution: "Powered by <a href='https://developers.arcgis.com/terms/attribution/' target='_blank' rel='noopener'>Esri</a>"
        });

    var map = L.map("index-map", {
        layers: [mapTileLayers],
        center: [23.5, 12],
        zoom: 2
    }).setView([46.79, 13.95], 9);

    var skiIcon = new L.Icon({
        iconUrl: "../../../media/ski-icon2.png",
        iconSize: [25, 25],
        iconAnchor: [10, 25]
    })

    var heiligenBlut = L.marker([47.04, 12.85], {
        icon: skiIcon
    }).addTo(map).bindPopup("Heiligenblut");
    var moelltallerGletscher = L.marker([46.98, 13.05], {
        icon: skiIcon
    }).addTo(map);
});