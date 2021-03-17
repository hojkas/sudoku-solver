// ==============================
// startup variables and settings
// ==============================

window.test_variable = 5;

// number of cell that is currently selected = highlighted
window.selected_cell_id = -1;

// value of number to be highlighter wherever it's, for the purpose of restoring highlighted cells
// after user changes it
window.highlighted_num = -1;

// setting to set if shift click toggles between solved and notes
// (on false, held down shift is solved, without shift is notes)
window.shift_is_toggle = true;

// on shift_is_toggle == true, this variable sets if the filled in numbers from user are solved
// or notes (solved on true, notes on false)
window.fill_in_solved = false;

// on true, obvious mistakes (same numbers twice in row/col/sector) are highlighted
window.show_obvious_mistakes = false;

// arrays to hold ids of currently highlighted cell ids for easiers clearing
window.obvious_mistakes_solved_colored = [];
window.obvious_mistakes_notes_colored = [];

$(document).ready(function()
{
    $('#settings-shift-toggle-on').prop('checked', true);
    $('#settings-highlight-mistakes-off').prop('checked', true);

    // ==============================
    // registering handling functions
    // ==============================

    // Selecting cell by click
    $('.sudoku-cell').on('click', function () {
        let new_id = $(this).attr('id').split('-')[1];
        change_selected(new_id);
    });

    $(window).keyup(function (event) {
        if(event.keyCode === 16) on_shift_key_up();
    });

    $(window).keydown(function (event) {
        let key = event.keyCode;
        if(key === 16) {
            //shift was pressed
            on_shift_key_down();
        }

        if(window.selected_cell_id !== -1) {
            // backspace or delete indicates reseting cell
            if (key === 8 || key === 46) {
                on_delete_key_down();
            }
            //key arrow
            else if (key >= 37 && key <= 40) {
                on_arrow_key_down(key);
                event.preventDefault();
            }
            // test if key pressed is one of possible numbers/letters for this sudoku
            else if ((max_sudoku_number === 4 && key >= 49 && key <= 52) ||
               (max_sudoku_number === 6 && key >= 49 && key <= 54) ||
               (max_sudoku_number === 9 && key >= 49 && key <= 57) ||
               (max_sudoku_number === 16 && ((key >= 49 && key <= 57) || (key >= 65 && key <= 71)))) {
                    on_number_input(key, event.shiftKey);
            }
        }
    });

    $('#controls_fill_solved').on('click', function() {
        if(window.shift_is_toggle) {
            highlight_selected_controls_button($(this), $('#controls_fill_notes'));
            window.fill_in_solved = true;
        }
    });

    $('#controls_fill_notes').on('click', function() {
        if(window.shift_is_toggle) {
            highlight_selected_controls_button($(this), $('#controls_fill_solved'));
            window.fill_in_solved = false;
        }
    });

    $('#settings-shift-toggle-on').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-off').prop('checked', false);
            window.shift_is_toggle = true;
        }
    });

    $('#settings-shift-toggle-off').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-on').prop('checked', false);
            window.shift_is_toggle = false;
            // setting default values
            highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });

    $('#settings-highlight-mistakes-off').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-highlight-mistakes-on').prop('checked', false);
            window.show_obvioius_mistakes = false;
        }
    });

    $('#settings-highlight-mistakes-on').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-highlight-mistakes-off').prop('checked', false);
            window.show_obvioius_mistakes = true;
        }
    });

    // Code snippet from https://stackoverflow.com/questions/38425931/download-table-as-png-using-jquery/40644383,
    // answered on Nov 16 2016 by Christos Lytra; with small changes to work with html2canvas v1.0.0 and
    // to scale for higher resolution
    $('#export-sudoku').on('click', function() {
        remove_highlight_for_download();
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
        restore_highlight_for_download();
    });

    $('.highlight-button').on('click', function() {
        let number_id = $(this).attr('id').split('_')[2];
        if(number_id !== window.highlighted_num) {
            highlight_selected_controls_button($('#highlight_number_' + number_id), $('#highlight_number_' + window.highlighted_num));
            change_numbers_highlight(number_id, window.highlighted_num);
            window.highlighted_num = number_id;
        }
    });
});