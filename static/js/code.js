function create_element(element_name, element_text) {
    var element = document.createElement(element_name);
    element.innerHTML = element_text;
    return element.firstChild;
}

function clear_viz() {
    var viz = document.getElementById("viz");
        viz.innerHTML = '';

}

function do_go() {
    $.post('/turn_on_java_server/', {
        text: "hello"
    }).done(function (json) {

        clear_viz();

        for (var region in json['regions']) {
            if (json['regions'].hasOwnProperty(region))
                for (var col in json['regions'][region]['cols']) {
                    var column_str = '<div id="region_" class="thumbnail" style="display: inline-block; overflow-x: auto; overflow-y: hidden; margin: 0; height:50px; width:50px;"></div>';
                    var column = create_element("column_", column_str);
                    document.getElementById("viz").appendChild(column);

                    if (json['regions'][region]['cols'].hasOwnProperty(col))
                        for (var cell in  json['regions'][region]['cols'][col]['cells']) {
                            var cell_str = '<a href="#" class="thumbnail"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';
                            var cell_elem = create_element("cell_", cell_str);
                            column.appendChild(cell_elem);
                        }
                }
        }
    });
}

function do_stop() {
    $.post('/stop_java_server/', {
        text: "hello"
    }).done(function (data) {
        clear_viz();
        debug_add_line('Java машина остановлена');
    });
}

function debug_add_line(line) {
    var li = document.createElement('LI');
    li.innerHTML = line;
    var q = document.getElementById("debugID");
    q.appendChild(li);
}



