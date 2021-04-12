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
    let sectors_ids = [];
    for(let i = 0; i < 9; i++) sectors_ids.push([]);
    for(let i = 0; i < 81; i++) sectors_ids[cell_sector[i]].push(i);
    let is_correct = true;
    sectors_ids.forEach(function(one_sector_ids) {
        if(!(check_connected_sector(one_sector_ids))) is_correct = false;
    });
    return is_correct;
}

function check_connected_sector(sector_ids) {
    let current_cell = sector_ids[0];
    let found_cells = crawl_from_cell(current_cell, sector_ids.slice(1));
    let distinct_found_cells = [];
    found_cells.forEach(function (num) {
        if(!distinct_found_cells.includes(num)) distinct_found_cells.push(num);
    })
    return distinct_found_cells.length === 9;
}

function crawl_from_cell(current_cell, non_explored_ids) {
    let found_cells = [current_cell];

    let can_move_to = get_possible_moves(current_cell, non_explored_ids);

    let new_nonexplored = non_explored_ids.filter(function(item) {
       if(!(can_move_to.includes(item))) return item;
    });

    can_move_to.forEach(function(cell_move) {
        found_cells = found_cells.concat(crawl_from_cell(cell_move, new_nonexplored));
    });

    return found_cells;
}

function get_possible_moves(current_cell, non_explored_ids) {
    let can_move_to = [];

    let up_cell = cell_in_direction(current_cell, 'up');
    if (up_cell !== null) if(non_explored_ids.includes(up_cell)) can_move_to.push(up_cell);
    let down_cell = cell_in_direction(current_cell, 'down');
    if (down_cell !== null) if(non_explored_ids.includes(down_cell)) can_move_to.push(down_cell);
    let right_cell = cell_in_direction(current_cell, 'right');
    if (right_cell !== null) if(non_explored_ids.includes(right_cell)) can_move_to.push(right_cell);
    let left_cell = cell_in_direction(current_cell, 'left');
    if (left_cell !== null) if(non_explored_ids.includes(left_cell)) can_move_to.push(left_cell);

    return can_move_to;
}

function cell_in_direction(cell_id, direction) {
    let row = parseInt(cell_id/9);
    let col = cell_id % 9;
    if(direction === 'up') row--;
    else if(direction === 'right') col++;
    else if(direction === 'left') col--;
    else if(direction === 'down') row++;

    if(col >= 0 && col < 9 && row >= 0 && row < 9) return row * 9 + col;
    else return null;
}
