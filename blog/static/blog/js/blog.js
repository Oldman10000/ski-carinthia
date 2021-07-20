// sort selector function
$('#sort-selector').change(function () {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if (selectedVal != "reset") {
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
});

// hover effects for point up/down buttons
$(".point-up").hover(
    function () {
        $(this).removeClass("grey");
        $(this).addClass("green");
    },
    function () {
        $(this).removeClass("green");
        $(this).addClass("grey");
    }
);

$(".point-down").hover(
    function () {
        $(this).removeClass("grey");
        $(this).addClass("red");
    },
    function () {
        $(this).removeClass("red");
        $(this).addClass("grey");
    }
);