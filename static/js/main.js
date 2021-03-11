$(document).ready(function()
{
    let selected_cell = -1;

    $('.sudoku-cell').on('click', function () {
        if (selected_cell !== -1) {
            $('#' + selected_cell).css({'backgroundColor':'transparent'});
        }
        selected_cell = $(this).attr('id');
        $(this).css({'backgroundColor':'lightskyblue'});
    });

    $('#changeDivButton').on('click', function () {
        if ($('#divToChange1').css('display') !== 'none') {
            $('#divToChange2').show().siblings('div').hide();
        } else if ($('#divToChange2').css('display') !== 'none') {
            $('#divToChange1').show().siblings('div').hide();
        }
    });

    $('.test').on('click', function () {
        alert($(this).attr('title'));
    });

    $('.switch').on('click', function() {
        let notes = '#notes' + $(this).attr('title');
        let solved = '#solved' + $(this).attr('title');

        if ($(solved).css('display') != 'none') {
            $(notes).show().siblings('div').hide();
        } else if ($(notes).css('display') != 'none') {
            $(solved).show().siblings('div').hide();
        }
    });
});
