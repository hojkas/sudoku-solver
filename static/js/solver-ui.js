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

function fill_number(key, cell_id) {
    const target_solved = '#solved' + cell_id;
    $(target_solved).html(key.toString());
    snap_visibility_to_solved(cell_id);
    clear_notes(cell_id);
}

function clear_notes(cell_id) {
    let i;
    const targetNote = '#note' + cell_id + '-';
    for(i = 1; i <= max_sudoku_number; i++) $(targetNote + i).html('&nbsp;');
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

}