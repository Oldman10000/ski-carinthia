// preloader
$(window).on("load", function() {
    $("#loading-overlay").fadeOut();
});

$(document).ready(function() {
    // preloader
    $("#loading-overlay").fadeIn();
    $("#loading-overlay").fadeOut(500);

    // toasts
    $('.toast').toast('show');
});
