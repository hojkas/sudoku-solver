// ==============================
// startup variables and settings
// ==============================

// number of cell that is currently selected = highlighted
window.selected_cell_id = -1;

// value of number to be highlighter wherever it's, for the purpose of restoring highlighted cells
// after user changes it
window.highlighted_num = -1;

// on shift_is_toggle == true, this variable sets if the filled in numbers from user are solved
// or notes (solved on true, notes on false)
window.fill_in_solved = false;

// variable to hold dictionary with information about candidates to be delted if step is applied
window.candidates_to_be_deleted = null;
// variable to hold number to be solved after applying of next step
window.number_to_be_solved = null;

let number_to_hexa_mapping = {
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    '10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G'
}

let hexa_to_number_mapping = {
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15', 'G': '16'
}

let custom_highlight_color_mapping = {
    'red': '#FF4136',
    'yellow': '#FFDC00',
    'green': '#2ECC40',
    'transparent': 'transparent'
}

$(document).ready(function()
{
    if (setting_shift_is_toggle) $('#settings-shift-toggle-on').prop('checked', true);
    else $('#settings-shift-toggle-off').prop('checked', true);

    if (setting_sudoku_full_size) $('#settings-sudoku-full-size-on').prop('checked', true);
    else $('#settings-sudoku-full-size-off').prop('checked', true);

    // ==============================
    // registering handling functions
    // ==============================

    // Selecting cell by click
    $('.sudoku-cell').on('click', function () {
        // if developer tools are on and custom highlight is set to something else than "off",
        // selection clicks are ignored
        if(developers_tools) {
            if(window.selected_highlight_name !== 'off') {
                return;
            }
        }
        // "vanilla" functionality
        let new_id = $(this).attr('id').split('-')[1];
        change_selected(new_id);

        if(developers_tools) {
            if(window.fill_in_candidates_by_click && (window.selected_cell_id !== -1)) {
                fill_all_candidates_in_cell(window.selected_cell_id);
            }
        }
    });

    $('#clear_sudoku').on('click', function() {
       clear_sudoku();
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
        if(setting_shift_is_toggle) {
            highlight_selected_controls_button($(this), $('#controls_fill_notes'));
            window.fill_in_solved = true;
        }
    });

    $('#controls_fill_notes').on('click', function() {
        if(setting_shift_is_toggle) {
            highlight_selected_controls_button($(this), $('#controls_fill_solved'));
            window.fill_in_solved = false;
        }
    });

    $('#settings-shift-toggle-on').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-off').prop('checked', false);
            setting_shift_is_toggle = true;
            update_setting('setting_shift_is_toggle', true);
        }
    });

    $('#settings-shift-toggle-off').change(function () {
        if ($(this).is(':checked')) {
            $('#settings-shift-toggle-on').prop('checked', false);
            setting_shift_is_toggle = false;
            update_setting('setting_shift_is_toggle', false);
            // setting default values
            highlight_selected_controls_button($('#controls_fill_notes'), $('#controls_fill_solved'));
        }
    });

    $('#settings-sudoku-full-size-off').change(function() {
        if ($(this).is(':checked')) {
            $('#settings-sudoku-full-size-on').prop('checked', false);
            update_setting('setting_sudoku_full_size', false);
            change_sudoku_strategy_position(false);
        }
    });

    $('#settings-sudoku-full-size-on').change(function() {
        if ($(this).is(':checked')) {
            $('#settings-sudoku-full-size-off').prop('checked', false);
            update_setting('setting_sudoku_full_size', true);
            change_sudoku_strategy_position(true);
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

    $('#generate_sudoku').on('click', function() {
        $('#generate_sudoku_alt').show();
        $('#generate_sudoku').hide();
        generate_sudoku($('generate_difficulty').val());
    });

    $('#get-next-step').on('click', function() {
        $('#next-step-loading').show().siblings('div').hide();
        count_next_step();
    });

    $('#apply-next-step').on('click', function () {
        apply_prepared_step();
        reset_strategy_icons();
        show_default_strategy_description();
        remove_all_custom_highlight();
        $('#next-step-default-button-wrapper').show().siblings('div').hide();
        window.candidates_to_be_deleted = null;
        window.number_to_be_solved = null;
    });

    $('#cancel-next-step').on('click', function() {
        reset_strategy_icons();
        show_default_strategy_description();
        remove_all_custom_highlight();
        $('#next-step-default-button-wrapper').show().siblings('div').hide();
        window.candidates_to_be_deleted = null;
        window.number_to_be_solved = null;
    });

    $('#fill_candidates_everywhere').on('click', function() {
        let text_ref = $('#automatic-candidates-default');
        let loading_ref = $('#automatic-candidates-loading');
        loading_ref.show().siblings('div').hide();
        setTimeout(function() {
            for(let x = 0; x < max_sudoku_number; x++) {
                for(let y = 0; y < max_sudoku_number; y++) {
                   let cell_id = x * max_sudoku_number + y;

                   if(!is_solved_visible(cell_id)) {
                       fill_all_candidates_in_cell(cell_id);
                   }
                }
            }
            text_ref.show().siblings('div').hide();
        }, 0);
    });
});