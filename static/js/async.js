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

async function count_next_step() {
    let sudoku_json = collect_sudoku_json();
    $.ajax({
        url: '/solver/get_next_step',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: sudoku_json,
        cache: false
    }).done(function(response_string) {
        let response_json = JSON.parse(response_string);

    });
}