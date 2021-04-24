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
        cache: false,
        error: function (xhr, err) {
            alert("error: " + xhr.status);
            $('#next-step-default-button-wrapper').show().siblings('div').hide();
        }
    }).done(function (response_string) {
        let response_json = JSON.parse(response_string);
        if (response_json['success']) {
            // strategy was found
            $('#next-step-next-action-wrapper').show().siblings('div').hide();
            window.candidates_to_be_deleted = response_json['candidates_to_remove'];
            window.number_to_be_solved = response_json['solve_number'];
            mark_successful_strategy(response_json['strategy_applied']);
            apply_highlight_from_list_of_dict(response_json['highlight']);
            try {
                let text = '[' + $('#' + response_json['strategy_applied']).text() + '] ' + response_json['text'];
                change_strategy_description(text);
            } catch {
                let text = response_json['text'];
                change_strategy_description(text);
            }
        } else {
            // strategy wasn't found!
            $('#next-step-default-button-wrapper').show().siblings('div').hide();
            alert(response_json['text']);
        }
    });
}

async function generate_sudoku(difficulty) {
    $.ajax({
        url: '/solver/generate_sudoku',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            difficulty: difficulty,
            sudoku_name: sudoku_name
        },
        cache: false,
        error: function (xhr, err) {
            alert("error: " + xhr.status);
            $('#generate_sudoku').show();
            $('#generate_sudoku_alt').hide();
        }
    }).done(function(response_string) {
        let response_json = JSON.parse(response_string);
        if(response_json['success']) {
            load_sudoku_from_list(response_json['sudoku']);
        }
        else {
            alert(response_json['text']);
        }
        $('#generate_sudoku').show();
        $('#generate_sudoku_alt').hide();
    });
}

async function check_solvability() {
    let sudoku_json = collect_sudoku_json(); //already stringified
    $.ajax({
        url: '/solver/check_solvability',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            json: sudoku_json
        },
        cache: false
    }).done(function(response_string) {
        $('#check-solvability-text').show();
        $('#check-solvability-loading').hide();
        let response = JSON.parse(response_string);
        alert(response['result']);
    });
}

async function get_brute_force_solution() {
    let sudoku_json = collect_sudoku_json(); //already stringified
    $.ajax({
        url: '/solver/get_brute_force_solution',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            json: sudoku_json
        },
        cache: false
    }).done(function(response_string) {
        $('#get-brute-force-solution-loading').hide();
        $('#get-brute-force-solution-text').show();
        let response_json = JSON.parse(response_string);
        if (response_json['success']) load_sudoku_from_list(response_json['sudoku']);
        else alert(response_json['text']);
        // TODO is broken
    });
}

async function submit_jigsaw_shape(sector_ids, cell_sectors) {
    $.ajax({
        url: '/solver/edit_jigsaw_shape',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrf_token
        },
        data: {
            sector_ids: JSON.stringify(sector_ids),
            cell_sectors: JSON.stringify(cell_sectors)
        },
        cache: false
    }).done(function(response_string) {
        hide_loading();
        window.location.replace('/solver/jigsaw');
    });
}