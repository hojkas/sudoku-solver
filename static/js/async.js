async function update_setting(name_of_setting, value) {
    $.ajax({
        url: '/solver/update_setting',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            setting: name_of_setting,
            value: value.toString()
        },
        cache: false
    }).done(function() {

    });
}