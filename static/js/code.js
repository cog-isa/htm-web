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
            debug_add_line(json["temporal_pooler"]);
            //console.log(json["temporal_pooler"]);
            debug_add_line(json["temporal_pooler"]["columns"]);
            var region_size = json["temporal_pooler"]["region_size"];
            //debug_add_line(region_size);
            var cells_size = json["temporal_pooler"]["columns"][0][0]["cells"].length;
            for (var i = 0; i < region_size; i++) {

                for (var j = 0; j < region_size; j++) {
                    //debug_add_line(json["temporal_pooler"]["columns"][i][j]);
                    var column_str = '<div id="region_" class="thumbnail" style="display: inline-block; overflow-x: auto; overflow-y: hidden; margin: 0; height:50px; width:50px;"></div>';
                    var column = create_element("column_", column_str);
                    document.getElementById("viz").appendChild(column);
                    for(var k = 0; k < cells_size; k++) {

                        var cell_str = '';
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 1)
                            cell_str = '<a href="PASSIVE" class="thumbnail"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 2)
                            cell_str = '<a href="ACTIVE" class="thumbnail btn-success"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 3)
                            cell_str = '<a href="PREDICTION" class="thumbnail btn-warning"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';

                        var cell_elem = create_element("cell_", cell_str);
                        column.appendChild(cell_elem);
                    }
                }
                var tr = '<br>';
                var tr_element = create_element("column_", tr);
                document.getElementById("viz").appendChild(tr_element);
            }
        }
    )
    ;
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



