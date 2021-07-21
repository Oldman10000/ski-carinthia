// sort selector

$('#sort-selector').change(function () {
    let selector = $(this);
    let currentUrl = new URL(window.location);

    let selectedVal = selector.val();
    if (selectedVal != "reset") {
        let sort = selectedVal.split("_")[0];
        let direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
});

// filters

$('#filter-form').submit(function (e) {
    e.preventDefault();

    let currentUrl = new URL(window.location);

    let filters = ''

    $('.filter-checkbox').each(function() {
        if ($(this).prop('checked')) {
            filters += $(this).val()
            filters += '+'
            console.log($(this).val())
        }
    });

    if (filters && filters != 'every+') {
        currentUrl.searchParams.set("filters", filters);
        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("filters");
        window.location.replace(currentUrl);
    }
});