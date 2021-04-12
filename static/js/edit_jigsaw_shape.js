let selected_sector = 0;

let custom_sector_to_color_mapping = {
    0: '#ff4500',
    1: '#ffff00',
    2: '#7cfc00',
    3: '#00ffff',
    4: '#a020f0',
    5: '#2f4f4f',
    6: '#1e90ff',
    7: '#ee1493',
    8: '#ffdead'
}

let mouse_down = false;

$(document).mousedown(function() {
    mouse_down = true;
})

$(document).mouseup(function () {
    mouse_down = false;
})

$(document).ready(function() {
    $('.sector_color_button').on('click', function() {
        let former_button_ref = $('#sector_color_' + selected_sector);
        former_button_ref.css({'background-color': 'lightgrey', 'border-color': 'grey'});
        $(this).css({'background-color': 'dodgerblue', 'border-color': 'black'});
        selected_sector = parseInt($(this).attr('id').split('_')[2]);
    });

    $('.edit-jigsaw-shape-cell').on('click', function() {
        color_sector_on_cell($(this));
    });

    $('.edit-jigsaw-shape-cell').mousedown(function() {
       color_sector_on_cell($(this));
    });

    $('.edit-jigsaw-shape-cell').mouseenter(function () {
        if(mouse_down) color_sector_on_cell($(this));
    });

    $('#edit-jigsaw-submit').on('click', function() {
       for(let i = 0; i < 81; i++)
       {
           if(cell_sector[i] === -1) {
               alert(cell_left_without_sector_msg);
               return;
           }
       }
       for(let i = 0; i < 9; i++) {
           if($('#sector_color_status_' + i).text() !== '9') {
               alert(wrong_sector_count_msg);
               return;
           }
       }
       if(!check_connected_sectors()) {
           alert(sectors_cells_not_touching);
       }
       // TODO actually send it
    });
});

function color_sector_on_cell(cell) {
    let cell_id = cell.attr('id').split('-')[1];
    if(cell_sector[cell_id] !== -1) {
        // cell was colored in different color
        let former_sector_count = $('#sector_color_status_' + cell_sector[cell_id]);
        former_sector_count.html(parseInt(former_sector_count.text()) - 1);
        if(former_sector_count.text() === '9') former_sector_count.css({'color': 'green'});
        else former_sector_count.css({'color': 'red'});
    }
    cell_sector[cell_id] = selected_sector;
    cell.css({'background-color': custom_sector_to_color_mapping[selected_sector]});
    let sector_count = $('#sector_color_status_' + selected_sector);
    sector_count.html(parseInt(sector_count.text()) + 1);
    if(sector_count.text() === '9') sector_count.css({'color': 'green'});
    else sector_count.css({'color': 'red'});
}

function check_connected_sectors() {
    for(let i = 0; i < 9; i++) check_connected_sector(i);
}

function check_connected_sector(sector_id) {

}
