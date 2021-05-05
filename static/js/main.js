// ===================================
// Author: Iveta Strnadová (xstrna14)
// startup variables and settings
// ===================================

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

        // alter number from numpad to imitate number from keyboard the script counts with
        if(key >= 97 && key <= 105) key = key - (97 - 49);
        if(window.selected_cell_id !== -1) {
            // backspace or delete indicates reseting cell
            if (key === 8 || key === 46) {
                on_delete_key_down();
            }
            // TAB moves select onto next cell_id
            else if (key === 9) {
                let new_selected = parseInt(window.selected_cell_id) + 1;
                if (new_selected === max_sudoku_number * max_sudoku_number) change_selected('0');
                else change_selected(new_selected.toString());
                event.preventDefault();
            }
            //key arrow
            else if ((key >= 37 && key <= 40)) {
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

    $('#settings_show_keyboard_on').change(function () {
        if ($(this).is(':checked')) {
            $('#settings_show_keyboard_off').prop('checked', false);
            update_setting('setting_show_keyboard', true);
            $('#keyboard_footer').show();
            $('#compensate-for-keyboard').css({'height': $('#keyboard_footer').height()});
        }
    });

    $('#settings_show_keyboard_off').change(function() {
        if ($(this).is(':checked')) {
            $('#settings_show_keyboard_on').prop('checked', false);
            update_setting('setting_show_keyboard', false);
            $('#keyboard_footer').hide();
            $('#compensate-for-keyboard').css({'height': $('#keyboard_footer').height()});
        }
    });

    // Code snippet from https://stackoverflow.com/questions/38425931/download-table-as-png-using-jquery/40644383,
    // answered on Nov 16 2016 by Christos Lytra (https://stackoverflow.com/users/1889685/christos-lytras);
    // with small changes to work with html2canvas v1.0.0 and
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
        let chosen_sudoku = $('generate_difficulty').val();
        $('#generate_sudoku_alt').show();
        $('#generate_sudoku').hide();
        generate_sudoku(chosen_sudoku);
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
        remove_chain_lines();
        $('#next-step-default-button-wrapper').show().siblings('div').hide();
        window.candidates_to_be_deleted = null;
        window.number_to_be_solved = null;
    });

    $('#cancel-next-step').on('click', function() {
        reset_strategy_icons();
        show_default_strategy_description();
        remove_all_custom_highlight();
        remove_chain_lines();
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

    $('#check-solvability').on('click', function() {
        $('#check-solvability-text').hide();
        $('#check-solvability-loading').show();
        check_solvability();
    });

    $('#hide_keyboard_button').on('click', function() {
       $('#hide_keyboard_div').show();
       $('#show_keyboard_div').hide();
       $('#compensate-for-keyboard').css({'height': $('#keyboard_footer').height()});
    });

    $('#show_keyboard_button').on('click', function() {
       $('#hide_keyboard_div').hide();
       $('#show_keyboard_div').show();
       $('#compensate-for-keyboard').css({'height': $('#keyboard_footer').height()});
    });

    $('.keyboard-button').on('click', function() {
        let num = $(this).attr('id').split('-')[1];
        on_number_input(num);
    });

    $('#sudoku9x9-expand-links').on('click', function() {
       $('#sudoku9x9-collapsed-links-div').hide();
       $('#sudoku9x9-expanded-links-div').show();
    });

    $('#sudoku9x9-hide-links').on('click', function() {
       $('#sudoku9x9-collapsed-links-div').show();
       $('#sudoku9x9-expanded-links-div').hide();
    });
});

// function from user Michael Zaporozhets (https://stackoverflow.com/users/1061967/michael-zaporozhets)
// on StackOverflow, answered on 8.7.2012
// from https://stackoverflow.com/questions/11381673/detecting-a-mobile-browser
window.mobileCheck = function() {
  let check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};