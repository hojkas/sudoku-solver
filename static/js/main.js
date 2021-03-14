$(document).ready(function()
{
    // ==============================
    // startup variables and settings
    // ==============================

    let selected_cell_id = -1;
    let shift_is_toggle = true;
    let fill_in_solved = false;

    $('#settings-shift-toggle-on').prop('checked', true);

    // ==============================
    // registering handling functions
    // ==============================

    // Selecting cell by click
    $('.sudoku-cell').on('click', function () {
        let new_id = $(this).attr('id').split('-')[1];
        change_selected(new_id);
    });

    function change_selected(new_cell) {
        if (selected_cell_id !== -1) {
            $('#cell-' + selected_cell_id).css({'backgroundColor':'transparent'});
        }
        $('#cell-' + new_cell).css({'backgroundColor':'lightskyblue'});
        selected_cell_id = new_cell;
    }

    $(window).keyup(function (event) {
        if(event.keyCode === 16 && !shift_is_toggle) { //shift used as hold down for solved
            highlight_selected_fill_in_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });

    $(window).keydown(function (event) {
        let key = event.keyCode;
        if(key === 16) {
            //shift was pressed
            if(shift_is_toggle) { //setting to use shift as toggle
                if(fill_in_solved) {
                    fill_in_solved = false;
                    highlight_selected_fill_in_button($('#controls_fill_notes'), $('#controls_fill_solved'));
                }
                else {
                    fill_in_solved = true;
                    highlight_selected_fill_in_button($('#controls_fill_solved'), $('#controls_fill_notes'));
                }
            }
            else { //shift is used as hold for solved, only change appearance
                highlight_selected_fill_in_button($('#controls_fill_solved'), $('#controls_fill_notes'));
            }
        }

        if(selected_cell_id !== -1) {
            // backspace or delete indicates reseting cell
            if (key === 8 || key === 46) {
                clear_notes(selected_cell_id);
                clear_solved(selected_cell_id);
            }
            //key arrow
            else if (key >= 37 && key <= 40) {
                event.preventDefault();
                let n = count_new_selected_cell(key, selected_cell_id, max_sudoku_number);
                change_selected(n);
            }
            // test if key pressed is one of possible numbers/letters for this sudoku
            else if ((max_sudoku_number === 4 && key >= 49 && key <= 52) ||
               (max_sudoku_number === 6 && key >= 49 && key <= 54) ||
               (max_sudoku_number === 9 && key >= 49 && key <= 57) ||
               (max_sudoku_number === 16 && ((key >= 49 && key <= 57) || (key >= 65 && key <= 70)))) {
                    let num;
                    if(key <= 57) num = key - 48; //for nums 1-9
                    else num = key - 55; //for hexa
                    //if shift is toggle in settings, note/solve is filled in decided by fill_in_solved bool
                    if(shift_is_toggle && fill_in_solved) fill_number(num, selected_cell_id);
                    else if(shift_is_toggle) change_number(num, selected_cell_id);
                    //if shift needs to be held to change note/solve, it is decided by shift held
                    else if(event.shiftKey) fill_number(num, selected_cell_id);
                    else change_number(num, selected_cell_id);
            }
        }
    });

    $('#controls_fill_solved').on('click', function() {
        if(shift_is_toggle) {
            highlight_selected_fill_in_button($(this), $('#controls_fill_notes'));
            fill_in_solved = true;
        }
    });

    $('#controls_fill_notes').on('click', function() {
        if(shift_is_toggle) {
            highlight_selected_fill_in_button($(this), $('#controls_fill_solved'));
            fill_in_solved = false;
        }
    });

    $('#settings-shift-toggle-on').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-off').prop('checked', false);
            shift_is_toggle = true;
        }
    });

    $('#settings-shift-toggle-off').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-on').prop('checked', false);
            shift_is_toggle = false;
            // setting default values
            highlight_selected_fill_in_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });
});