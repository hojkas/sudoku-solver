window.custom_highlight_red = []
window.custom_highlight_green = []
window.custom_highlight_yellow = []

window.selected_highlight_name = 'off';
window.fill_in_candidates_by_click = false;

$(document).ready(function() {
    // registering click functions from all
    $('#custom-highlight-red').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'red');
        window.selected_highlight_name = 'red';
    });

    $('#custom-highlight-green').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'green');
        window.selected_highlight_name = 'green';
    });

    $('#custom-highlight-yellow').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'yellow');
        window.selected_highlight_name = 'yellow';
    });

    $('#custom-highlight-off').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'off');
        window.selected_highlight_name = 'off';
    });

    $('#custom-highlight-transparent').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'transparent');
        window.selected_highlight_name = 'transparent';
    });

    $('#custom-highlight-remove-all').on('click', function() {
        remove_all_custom_highlight();
    });

    //register actions on click for custom highlight
    $('.sudoku-solved-num').on('click', function () {
        if(window.selected_highlight_name !== 'off') {
            $(this).css({'background-color': custom_highlight_color_mapping[window.selected_highlight_name]});
        }
    })

    $('.sudoku-note-num').on('click', function() {
        if(window.selected_highlight_name !== 'off') {
            $(this).css({'background-color': custom_highlight_color_mapping[window.selected_highlight_name]});
        }
    });

    $('#fill_all_candidates_on_click').change(function() {
        window.fill_in_candidates_by_click = $(this).is(':checked');
    });

    $('#remove_candidates_everywhere').on('click', function() {
        for(let x = 0; x < max_sudoku_number; x++) {
            for(let y = 0; y < max_sudoku_number; y++) {
                let cell_id = x * max_sudoku_number + y;
                if(!is_solved_visible(cell_id)) {
                    clear_notes(cell_id);
                }
            }
        }
    });
});

function custom_highlight_buttons_change(former_button_name, current_button_name) {
    let former_button_ref = $('#custom-highlight-' + former_button_name);
    let current_button_ref = $('#custom-highlight-' + current_button_name);
    former_button_ref.css({'background-color': 'lightgrey', 'border-color': 'grey'});
    current_button_ref.css({'background-color': 'dodgerblue', 'border-color': 'black'});
    if(current_button_name !== 'off') {
        change_selected(-1);
    }
}

function fill_all_candidates_in_cell(cell_id) {
    for(let x = 1; x <= max_sudoku_number; x++) {
        add_number_to_div($('#note' + cell_id + '-' + x), x);
        clear_solved(cell_id);
        snap_visibility_to_notes(cell_id);
    }
}

function load_test_sudoku(num) {
    let sudoku = [[
            5, 3, null, null, 7, null, null, null, null,
            6, null, null, 1, 9, 5, null, null, null,
            null, 9, 8, null, null, null, null, 6, null,
            8, null, null, null, 6, null, null, null, 3,
            4, null, null, 8, null, 3, null, null, 1,
            7, null, null, null, 2, null, null, null, 6,
            null, 6, null, null, null, null, 2, 8, null,
            null, null, null, 4, 1, 9, null, null, 5,
            null, null, null, null, 8, null, null, 7, 9
        ],
        [
            5, null, null, 6, 2, null, null, 3, 7,
            null, null, 4, 8, 9, null, null, null, null,
            null, null, null, null, 5, null, null, null, null,
            9, 3, null, null, null, null, null, null, null,
            null, 2, null, null, null, null, 6, null, 5,
            7, null, null, null, null, null, null, null, 3,
            null, null, null, null, null, 9, null, null, null,
            null, null, null, null, null, null, 7, null, null,
            6, 8, null, 5, 7, null, null, null, 2
        ]];

    load_sudoku_from_list(sudoku[num]);
}

