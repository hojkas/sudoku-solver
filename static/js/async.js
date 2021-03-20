async function update_setting(name_of_setting, value) {
    let data = {name_of_setting: value};
    $.post('/solver/update_setting', function (data) {
        alert(data);
    });
}