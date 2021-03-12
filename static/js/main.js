$(document).ready(function()
{
    let selected_cell_id = -1;

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

    // If num key is hit
    $(window).keydown(function (event) {
        if(selected_cell_id !== -1) {
            let key = event.keyCode;
            // backspace or delete indicates reseting cell
            if (key === 8 || key === 46) {
                clear_notes(selected_cell_id);
                clear_solved(selected_cell_id);
            }
            //key arrow
            else if (key >= 37 && key <= 40) {
                change_selected(count_new_selected_cell(key, selected_cell_id, max_sudoku_number));
            }
            // test if key pressed is one of possible numbers/letters for this sudoku
            else if ((max_sudoku_number === 4 && key >= 49 && key <= 52) ||
               (max_sudoku_number === 6 && key >= 49 && key <= 54) ||
               (max_sudoku_number === 9 && key >= 49 && key <= 57) ||
               (max_sudoku_number === 16 && ((key >= 49 && key <= 57) || (key >= 65 && key <= 70)))) {
                    let num;
                    if(key <= 57) num = key - 48; //for nums 1-9
                    else num = key - 55; //for hexa
                    if(event.shiftKey) fill_number(num, selected_cell_id);
                    else change_number(num, selected_cell_id);
            }
        }
    });
});