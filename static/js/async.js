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
    let sudoku_json = collect_sudoku_json(); //already stringified
    $.ajax({
        url: '/solver/get_next_step',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            json: sudoku_json
        },
        cache: false
    }).done(function(response_string) {
        let response_json = JSON.parse(response_string);
        if(response_json['success']) {
            // strategy was found
            $('#next-step-next-action-wrapper').show().siblings('div').hide();
            window.candidates_to_be_deleted = response_json['candidates_to_remove'];
            window.number_to_be_solved = response_json['solve_number'];
            mark_successful_strategy(response_json['strategy_applied']);
            apply_highlight_from_list_of_dict(response_json['highlight']);
            change_strategy_description(response_json['text']);
        }
        else {
            // strategy wasn't found!
            $('#next-step-default-button-wrapper').show().siblings('div').hide();
            alert(response_json['text']);
        }
    });
}