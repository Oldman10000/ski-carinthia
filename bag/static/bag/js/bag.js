$(document).ready(function () {
    // update quantity on click
    $('.update-link').click(function (e) {
        var form = $(this).prev('.update-form');
        form.submit();
    });

    // remove item
    $('.remove-item').click(function (e) {
        var csrfToken = "{{ csrf_token }}";
        var itemId = $(this).attr('id').split('remove_')[1];
        var type = $(this).data('type');
        var url = `/bag/remove/${itemId}/`;
        var data = {
            'csrfmiddlewaretoken': csrfToken,
            'type': type
        };

        $.post(url, data)
            .done(function () {
                location.reload();
            });
    });
});