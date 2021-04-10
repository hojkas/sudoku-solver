function change_number_among_notes(key) {
    const target_note = $('#note' + window.selected_cell_id + '-' + key);
    //if there was solved key, it is kept as a note
    const solved_num = $('#solved' + window.selected_cell_id).text();
    if(solved_num !== '\xa0') {
        add_number_to_div($('#note' + window.selected_cell_id + '-' + solved_num), solved_num);
        clear_selected_solved();
    }

    if(target_note.text() === '\xa0') {
        //is empty and num should be added
        add_number_to_div(target_note, key.toString());
    }
    else {
        //has num note and should be erased
        remove_number_from_div(target_note)
    }
    snap_selected_visibility_to_notes();
}

function remove_number_from_div(div) {
    div.html('&nbsp;');
    div.css({'background-color': 'transparent'});
}

function add_number_to_div(div, number_to_add) {
    div.html(number_to_hexa_mapping[number_to_add.toString()]);
    if(number_to_add === window.highlighted_num) div.css({'background-color': 'pink'});
    else div.css({'background-color': 'transparent'});
}

function fill_number(key) {
    const target_solved = $('#solved' + window.selected_cell_id);
    add_number_to_div(target_solved, key.toString());
    snap_selected_visibility_to_solved();
    clear_selected_notes();
}

function fill_cell_with_number(cell_id, num) {
    const target_solved = $('#solved' + cell_id);
    add_number_to_div(target_solved, num);
    snap_visibility_to_solved(cell_id);
    clear_notes(cell_id);
}

function clear_selected_notes() {
    let i;
    const targetNote = '#note' + window.selected_cell_id + '-';
    for(i = 1; i <= max_sudoku_number; i++) {
        let target_div_in_note = $(targetNote + i);
        target_div_in_note.html('&nbsp;');
        target_div_in_note.css({'background-color': 'transparent'});
    }
}

function clear_selected_solved() {
    const targetSolved = $('#solved' + window.selected_cell_id);
    targetSolved.html('&nbsp;');
    targetSolved.css({'background-color': 'transparent'});
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
    const targetSolved = $('#solved' + cell_id);
    targetSolved.html('&nbsp;');
    targetSolved.css({'background-color': 'transparent'});
}

function snap_selected_visibility_to_solved() {
    const targetDiv = '#solved' + window.selected_cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function snap_selected_visibility_to_notes() {
    const targetDiv = '#notes' + window.selected_cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function snap_visibility_to_solved(cell_id) {
    const targetDiv = '#solved' + cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function snap_visibility_to_notes(cell_id) {
    const targetDiv = '#notes' + cell_id;
    $(targetDiv).show().siblings('div').hide();
}

function count_new_selected_cell(pressed_key) {
    let col = window.selected_cell_id % max_sudoku_number;
    let row = (window.selected_cell_id - col) / max_sudoku_number;
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

function is_special_cell(target_cell) {
    if(target_cell.hasClass('special-sudoku-cell')) return true;
    else return false;
}

function remove_highlight_for_download() {
    let target_cell = $('#cell-' + window.selected_cell_id);

    if(is_special_cell(target_cell)) target_cell.css({'background-color': '#bde6ff'});
    else target_cell.css({'backgroundColor':'transparent'});
}

function restore_highlight_for_download() {
    $('#cell-' + window.selected_cell_id).css({'backgroundColor':'lightskyblue'});
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
    let hexified_number_to_highlight = number_to_hexa_mapping[number_to_highlight];
    let hexified_number_to_unhighlight = number_to_hexa_mapping[number_to_unhighlight];
    if(is_solved_visible(cell_id)) {
        // solved is currently visible
        let solved_ref = $('#solved' + cell_id);
        if(solved_ref.text() === hexified_number_to_highlight) {
            solved_ref.css({'background-color': 'lightpink'});
        }
        if(solved_ref.text() === hexified_number_to_unhighlight) {
            solved_ref.css({'background-color': 'transparent'});
        }
    }
    else {
        // notes are currently visible
        let note_to_highlight_ref = $('#note' + cell_id + '-' + number_to_highlight);
        let note_to_unhighlight_ref = $('#note' + cell_id + '-' + number_to_unhighlight);
        if(note_to_highlight_ref.text() === hexified_number_to_highlight) {
            note_to_highlight_ref.css({'background-color': 'lightpink'});
        }
        if(note_to_unhighlight_ref.text() === hexified_number_to_unhighlight) {
            note_to_unhighlight_ref.css({'background-color': 'transparent'});
        }
    }
}

// returns true if the cell currently has "solved" num visible, false if it has the "notes"
function is_solved_visible(cell_id) {
    return $('#solved' + cell_id).is(':visible');
}

function change_selected(new_cell) {
    if (window.selected_cell_id !== -1) {
        let target_cell = $('#cell-' + window.selected_cell_id);
        if(is_special_cell(target_cell)) target_cell.css({'background-color': '#bde6ff'});
        else target_cell.css({'backgroundColor':'transparent'});
    }
    $('#cell-' + new_cell).css({'backgroundColor':'lightskyblue'});
    window.selected_cell_id = new_cell;
}

function mark_successful_strategy(strategy_name) {
    let el_classes = $('#icon-before-' + strategy_name).attr('class').split(/\s+/);
    let pos = -1;

    el_classes.forEach(function(el_class) {
        if(el_class.includes('strategy_list_icon_')) pos = parseInt(el_class.split('_')[3]);
    });

    for(let i = 0; i < pos; i++) {
        let strategy_ref = $('.strategy_list_icon_' + i);
        strategy_ref.removeClass('fa-minus');
        strategy_ref.addClass('fa-times');
        strategy_ref.css({'color': 'red'});
        strategy_ref.siblings('a').css({'color': 'grey'});
    }
    let strategy_ref = $('.strategy_list_icon_' + pos);
    strategy_ref.removeClass('fa-minus');
    strategy_ref.addClass('fa-check');
    strategy_ref.css({'color': 'green'});
    strategy_ref.siblings('a').css({'color': 'green', 'font-weight': 'bold'});
}

function mark_all_strategies_as_failed() {
    let strategy_icon_ref = $('.strategy_list_icon')
    strategy_icon_ref.removeClass('fa-minus');
    strategy_icon_ref.addClass('fa-times');
    strategy_icon_ref.css({'color': 'red'});
    strategy_icon_ref.siblings('a').css({'color': 'grey'});
}

function reset_strategy_icons() {
    let strategy_icon_ref = $('.strategy_list_icon')
    strategy_icon_ref.removeClass('fa-times');
    strategy_icon_ref.removeClass('fa-check');
    strategy_icon_ref.addClass('fa-minus');
    strategy_icon_ref.css({'color': 'grey'});
    strategy_icon_ref.siblings('a').css({'color': 'blue', 'font-weight': 'normal'});
}

function change_sudoku_strategy_position(to_full) {
    let sudoku_wrapper_ref = $('#sudoku-solver-wrapper-col');
    let strategy_wrapper_ref = $('#strategy-list-wrapper-col');
    if(to_full) {
        sudoku_wrapper_ref.removeClass('col-md-8');
        strategy_wrapper_ref.removeClass('col-md-4');
        sudoku_wrapper_ref.addClass('col-md-12');
        strategy_wrapper_ref.addClass('col-md-12');
    }
    else {
        sudoku_wrapper_ref.removeClass('col-md-12');
        strategy_wrapper_ref.removeClass('col-md-12');
        sudoku_wrapper_ref.addClass('col-md-8');
        strategy_wrapper_ref.addClass('col-md-4');
    }
}

function clear_sudoku() {
    for(let x = 0; x < max_sudoku_number; x++) {
        for (let y = 0; y < max_sudoku_number; y++) {
            let cell_id = x * max_sudoku_number + y;
            clear_solved(cell_id);
            clear_notes(cell_id);
            snap_visibility_to_notes(cell_id);
        }
    }
}

function change_strategy_description(new_description) {
    let expl_ref = $('#strategy_explanation_custom');
    expl_ref.html(new_description);
    expl_ref.show().siblings('div').hide();
}

function show_default_strategy_description() {
    $('#strategy_explanation_default').show().siblings('div').hide();
}

function collect_sudoku_json() {
    let sudoku_d = {
        "max_sudoku_number": max_sudoku_number,
        "board": []
    }
    for(let x = 0; x < max_sudoku_number; x++) {
        for (let y = 0; y < max_sudoku_number; y++) {
            let cell_id = x * max_sudoku_number + y;
            let cell_d = {
                "cell_id": cell_id,
                "notes": []
            }
            if (is_solved_visible(cell_id)) {
                cell_d["solved"] = parseInt(hexa_to_number_mapping[$('#solved' + cell_id).text()]);
            } else {
                cell_d["solved"] = null;
                for (let i = 1; i <= max_sudoku_number; i++) {
                    let note_ref = $('#note' + cell_id + '-' + i);
                    if (parseInt(hexa_to_number_mapping[note_ref.text()]) === i) cell_d["notes"].push(i);
                }
            }
            sudoku_d["board"].push(cell_d);
        }
    }
    return JSON.stringify(sudoku_d);
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
    change_numbers_highlight(window.highlighted_num, -1);
}

function apply_highlight_from_list_of_dict(list_of_dict) {
    list_of_dict.forEach(function(highlight_d) {
       let highlight_ref;
       if(highlight_d['is_solved']) {
           highlight_ref = $('#solved' + highlight_d['cell_id']);
       }
       else {
           highlight_ref = $('#note' + highlight_d['cell_id'] + '-' + highlight_d['note_id']);
       }
       highlight_ref.css({'background-color': custom_highlight_color_mapping[highlight_d['color']]});
    });
}

function apply_prepared_step() {
    window.candidates_to_be_deleted.forEach(function(candidate_d) {
        let note_cell_ref = $('#note' + candidate_d['cell_id'] + '-' + candidate_d['note_id']);
        note_cell_ref.html('&nbsp;');
        note_cell_ref.css({'background-color': 'transparent'});
    });
    if(window.number_to_be_solved != null) {
        fill_cell_with_number(window.number_to_be_solved['cell_id'], window.number_to_be_solved['number']);
    }
}

function load_sudoku_from_list(sudoku) {
    if(sudoku.length === (max_sudoku_number * max_sudoku_number)) {
        for(let x = 0; x < max_sudoku_number; x++) {
            for (let y = 0; y < max_sudoku_number; y++) {
                let cell_id = x * max_sudoku_number + y;
                if(sudoku[cell_id] != null) fill_cell_with_number(cell_id, sudoku[cell_id]);
                else {
                        clear_notes(cell_id);
                        clear_solved(cell_id);
                        snap_visibility_to_notes(cell_id);
                }
            }
        }
    }
}