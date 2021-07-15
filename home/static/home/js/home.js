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
