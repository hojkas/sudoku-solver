$(document).ready(function()
{
    // ==============================
    // startup variables and settings
    // ==============================

    // number of cell that is currently selected = highlighted
    let selected_cell_id = -1;

    // value of number to be highlighter wherever it's, for the purpose of restoring highlighted cells
    // after user changes it
    let highlighted_num = -1;

    // setting to set if shift click toggles between solved and notes
    // (on false, held down shift is solved, without shift is notes)
    let shift_is_toggle = true;

    // on shift_is_toggle == true, this variable sets if the filled in numbers from user are solved
    // or notes (solved on true, notes on false)
    let fill_in_solved = false;

    // on true, obvious mistakes (same numbers twice in row/col/sector) are highlighted
    let show_obvious_mistakes = false

    // TODO more

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
            highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });

    $(window).keydown(function (event) {
        let key = event.keyCode;
        if(key === 16) {
            //shift was pressed
            if(shift_is_toggle) { //setting to use shift as toggle
                if(fill_in_solved) {
                    fill_in_solved = false;
                    highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
                }
                else {
                    fill_in_solved = true;
                    highlight_selected_controls_button($('#controls_fill_solved'), $('#controls_fill_notes'));
                }
            }
            else { //shift is used as hold for solved, only change appearance
                highlight_selected_controls_button($('#controls_fill_solved'), $('#controls_fill_notes'));
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
               (max_sudoku_number === 16 && ((key >= 49 && key <= 57) || (key >= 65 && key <= 71)))) {
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
            highlight_selected_controls_button($(this), $('#controls_fill_notes'));
            fill_in_solved = true;
        }
    });

    $('#controls_fill_notes').on('click', function() {
        if(shift_is_toggle) {
            highlight_selected_controls_button($(this), $('#controls_fill_solved'));
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
            highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });

    // Code snippet from https://stackoverflow.com/questions/38425931/download-table-as-png-using-jquery/40644383,
    // answered on Nov 16 2016 by Christos Lytra; with small changes to work with html2canvas v1.0.0 and
    // to scale for higher resolution
    $('#export-sudoku').on('click', function() {
        remove_highlight_for_download(selected_cell_id);
        html2canvas(document.getElementById('sudoku-table'), {scale: 5}).then(function(canvas) {
            let saveAs = function(uri, filename) {
                let link = document.createElement('a');
                if (typeof link.download === 'string') {
                    document.body.appendChild(link); // Firefox requires the link to be in the body
                    link.download = filename;
                    link.href = uri;
                    link.click();
                    document.body.removeChild(link); // remove the link when done
                } else {
                    location.replace(uri);
                }
            };

            let img = canvas.toDataURL(),
                uri = img.replace(/^data:image\/[^;]/, 'data:application/octet-stream');

            saveAs(uri, 'sudokuExport.png');
        });
        restore_highlight_for_download(selected_cell_id);
    });

    $('.highlight-button').on('click', function() {
        let number_id = $(this).attr('id').split('_')[2];
        highlight_selected_controls_button($('#highlight_number_' + number_id), $('#highlight_number_' + highlighted_num));
        change_numbers_highlight(number_id, highlighted_num);
        highlighted_num = number_id;
    });
});