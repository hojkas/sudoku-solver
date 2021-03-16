function change_number(key, cell_id) {
    const target_note = '#note' + cell_id + '-' + key;
    //if there was solved key, it is kept as a note
    const solved_num = $('#solved' + cell_id).text();
    if(solved_num !== '\xa0') {
        $('#note' + cell_id + '-' + solved_num).html(solved_num);
        clear_solved(cell_id);
    }

    if($(target_note).text() === '\xa0') {
        //is empty and num should be added
        $(target_note).html(key.toString());
    }
    else {
        //has num note and should be erased
        $(target_note).html('&nbsp;');
    }
    snap_visibility_to_notes(cell_id);
}

function remove_number_from_div(div) {
    //TODO remove num and all highlights
}

function test() {
    alert(window.test_variable);
}

function add_number_to_div(div, number_to_add) {

}

function fill_number(key, cell_id) {
    const target_solved = $('#solved' + cell_id);
    target_solved.html(key.toString());
    target_solved.css({'background-color': 'transparent'});
    snap_visibility_to_solved(cell_id);
    clear_notes(cell_id);
}

function clear_notes(cell_id) {
    let i;
    const targetNote = '#note' + cell_id + '-';
    for(i = 1; i <= max_sudoku_number; i++) {
        let target_div_in_note = $(targetNote + i);
        target_div_in_note.html('&nbsp;');
        target_div_in_note.css({'background-color': 'transparent'});
    }
}

function clear_solved(cell_id) {
    $('#solved' + cell_id).html('&nbsp;');
}

function snap_visibility_to_solved(cell_id) {
    const targetDiv = '#solved' + cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function snap_visibility_to_notes(cell_id) {
    const targetDiv = '#notes' + cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function count_new_selected_cell(pressed_key, current_selected_cell, max_sudoku_number) {
    let col = current_selected_cell % max_sudoku_number;
    let row = (current_selected_cell - col) / max_sudoku_number;
    if(pressed_key === 37) {
        // LEFT
        if (col === 0) col = max_sudoku_number - 1;
        else col -= 1;
    }
    else if(pressed_key === 38) {
        // UP
        if (row === 0) row = max_sudoku_number - 1;
        else row -= 1;
    }
    else if(pressed_key === 39) {
        // RIGHT
        col = (col + 1) % max_sudoku_number;
    }
    else if(pressed_key === 40) {
        // DOWN
        row = (row + 1) % max_sudoku_number;
    }
    return (row * max_sudoku_number) + col;
}

function highlight_selected_controls_button(selected_button, other_button) {
    selected_button.css({'background-color': 'dodgerblue', 'color': 'black', 'border-color': 'black'});
    other_button.css({'background-color': 'lightgrey', 'color': 'grey', 'border-color': 'grey'});
}

function remove_highlight_for_download(cell_id) {
    $('#cell-' + cell_id).css({'backgroundColor':'transparent'});
}

function restore_highlight_for_download(cell_id) {
    $('#cell-' + cell_id).css({'backgroundColor':'lightskyblue'});
}

function change_numbers_highlight(new_highlight, old_hightlight) {
    for(let x = 0; x < max_sudoku_number; x++) {
        for (let y = 0; y < max_sudoku_number; y++) {
            let cell_id = x * max_sudoku_number + y;
            // for each possible cell id in the sudoku
            alter_highlight(new_highlight, old_hightlight, cell_id);
        }
    }
}

function alter_highlight(number_to_highlight, number_to_unhighlight, cell_id) {
    if(is_solved_visible(cell_id)) {
        // solved is currently visible
        let solved_ref = $('#solved' + cell_id);
        if(solved_ref.text() === number_to_highlight) {
            solved_ref.css({'background-color': 'lightpink'});
        }
        if(solved_ref.text() === number_to_unhighlight) {
            solved_ref.css({'background-color': 'transparent'});
        }
    }
    else {
        // notes are currently visible
        let note_to_highlight_ref = $('#note' + cell_id + '-' + number_to_highlight);
        let note_to_unhighlight_ref = $('#note' + cell_id + '-' + number_to_unhighlight);
        if(note_to_highlight_ref.text() === number_to_highlight) {
            note_to_highlight_ref.css({'background-color': 'lightpink'});
        }
        if(note_to_unhighlight_ref.text() === number_to_unhighlight) {
            note_to_unhighlight_ref.css({'background-color': 'transparent'});
        }
    }
}

// returns true if the cell currently has "solved" num visible, false if it has the "notes"
function is_solved_visible(cell_id) {
    return $('#solved' + cell_id).is(':visible');
}