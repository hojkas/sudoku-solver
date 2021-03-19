window.custom_highlight_red = []
window.custom_highlight_green = []
window.custom_highlight_yellow = []

window.selected_highlight_name = 'off';

$(document).ready(function() {
    // registering click functions from all
    $('#custom-highlight-red').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'red');
        window.selected_highlight_name = 'red';
    });

    $('#custom-highlight-limegreen').on('click', function() {
        custom_highlight_buttons_change(window.selected_highlight_name, 'limegreen');
        window.selected_highlight_name = 'limegreen';
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
            $(this).css({'background-color': window.selected_highlight_name});
        }
    })

    $('.sudoku-note-num').on('click', function() {
        if(window.selected_highlight_name !== 'off') {
            $(this).css({'background-color': window.selected_highlight_name});
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

function remove_all_custom_highlight() {
    for(let x = 0; x < max_sudoku_number; x++) {
        for(let y = 0; y < max_sudoku_number; y++) {
            let cell_id = x * max_sudoku_number + y;
            let solved_target_ref = $('#solved' + cell_id);
            if(solved_target_ref.css('background-color') !== 'pink')
                solved_target_ref.css({'background-color': 'transparent'});
            for(let i = 1; i <= max_sudoku_number; i++) {
                let note_target_ref = $('#note' + cell_id + '-' + i);
                if(note_target_ref.css('background-color') !== 'pink')
                    note_target_ref.css({'background-color': 'transparent'});
            }
        }
    }
}

function test() {
    alert(developers_tools + '<');
}