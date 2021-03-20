function on_shift_key_down() {
    if(setting_shift_is_toggle) { //setting to use shift as toggle
        if(window.fill_in_solved) {
            window.fill_in_solved = false;
            highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
        else {
            window.fill_in_solved = true;
            highlight_selected_controls_button($('#controls_fill_solved'), $('#controls_fill_notes'));
        }
    }
    else { //shift is used as hold for solved, only change appearance
        highlight_selected_controls_button($('#controls_fill_solved'), $('#controls_fill_notes'));
    }
}

function on_shift_key_up() {
    if(!setting_shift_is_toggle) { //shift used as hold down for solved
        highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
    }
}

function on_delete_key_down() {
    clear_selected_notes();
    clear_selected_solved();
}

function on_arrow_key_down(key) {
    let n = count_new_selected_cell(key);
    change_selected(n);
}

function on_number_input(key, shiftIsPressed) {
    let num;
    if(key <= 57) num = key - 48; //for nums 1-9
    else num = key - 55; //for hexa
    //if shift is toggle in settings, note/solve is filled in decided by window.fill_in_solved bool
    if(setting_shift_is_toggle && window.fill_in_solved) fill_number(num);
    else if(setting_shift_is_toggle) change_number_among_notes(num);
    //if shift needs to be held to change note/solve, it is decided by shift held
    else if(shiftIsPressed) fill_number(num);
    else change_number_among_notes(num);
}
