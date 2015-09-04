function create_element(element_name, element_text) {
    var element = document.createElement(element_name);
    element.innerHTML = element_text;
    return element.firstChild;
}

function clear_element(element_id) {
    var element = document.getElementById(element_id);
    element.innerHTML = '';
}

// хранит полученный json
var json_store;


function do_go() {
    $.post('/turn_on_java_server/', {
        text: "hello"
    }).done(function (json) {
            json_store = json;
            clear_element("viz");
            //console.log(json["temporal_pooler"]);
            var region_size = json["temporal_pooler"]["region_size"];
            var cells_size = json["temporal_pooler"]["columns"][0][0]["cells"].length;
            for (var i = 0; i < region_size; i++) {

                for (var j = 0; j < region_size; j++) {
                    //debug_add_line(json["temporal_pooler"]["columns"][i][j]);
                    var column_str = '<div id="region_" class="thumbnail" style="display: inline-block; overflow-x: auto; overflow-y: hidden; margin: 0; height:50px; width:50px;"></div>';
                    var column = create_element("column_", column_str);
                    document.getElementById("viz").appendChild(column);
                    for (var k = 0; k < cells_size; k++) {

                        var cell_str = '';
                        var id = json["temporal_pooler"]["columns"][i][j]["cells"][k]["id"];
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 1)
                            cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 2)
                            cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail btn-success"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';
                        if (json["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 3)
                            cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail btn-warning"style="display: inline-flex; overflow-x: auto;  margin: 0"></a>';

                        var cell_elem = create_element("cell_", cell_str);
                        column.appendChild(cell_elem);
                    }
                }
                var tr = '<br>';
                var tr_element = create_element("column_", tr);
                document.getElementById("viz").appendChild(tr_element);
            }

            clear_element("input_data");

            console.log(json["input"]);
            for (var i = 0; i < json["input"].length; i++) {
                for (var j = 0; j < json["input"][i].length; j++) {

                    var cell_str1 = '<a href="PASSIVE" class="thumbnail"style="display: inline-flex; overflow-x: auto;  margin: 2px"></a>';
                    if (json["input"][i][j] == 1)
                        cell_str1 = '<a href="ACTIVE" class="thumbnail btn-success"style="display: inline-flex; overflow-x: auto;  margin: 2px"></a>';
                    var cell_elem2 = create_element("cell_", cell_str1);

                    document.getElementById("input_data").appendChild(cell_elem2);
                }
                var tr1 = '<br>';
                var tr_element1 = create_element("column_", tr1);
                document.getElementById("input_data").appendChild(tr_element1);
            }


            clear_element("compress_input");

            console.log(json["compress_input"]);
            for (var i = 0; i < json["compress_input"].length; i++) {
                for (var j = 0; j < json["compress_input"][i].length; j++) {

                    var cell_str11 = '<a href="PASSIVE" class="thumbnail"style="display: inline-flex; overflow-x: auto;  margin: 2px"></a>';
                    if (json["compress_input"][i][j] == 1)
                        cell_str11 = '<a href="ACTIVE" class="thumbnail btn-success"style="display: inline-flex; overflow-x: auto;  margin: 2px"></a>';
                    var cell_elem22 = create_element("cell_", cell_str11);

                    document.getElementById("compress_input").appendChild(cell_elem22);
                }
                var tr12 = '<br>';
                var tr_element12 = create_element("column_", tr12);
                document.getElementById("compress_input").appendChild(tr_element12);
            }

        }
    )
    ;
}

function get_cell_by_id(id) {
    var json = json_store;
    var region_size = json["temporal_pooler"]["region_size"];
    var cells_size = json["temporal_pooler"]["columns"][0][0]["cells"].length;
    for (var i = 0; i < region_size; i++)
        for (var j = 0; j < region_size; j++)
            for (var k = 0; k < cells_size; k++)
                if (id == json["temporal_pooler"]["columns"][i][j]["cells"][k]["id"])
                    return json["temporal_pooler"]["columns"][i][j]["cells"][k];
}

function clear_all_dendrites() {
    var json = json_store;
    var region_size = json["temporal_pooler"]["region_size"];
    var cells_size = json["temporal_pooler"]["columns"][0][0]["cells"].length;
    for (var i = 0; i < region_size; i++)
        for (var j = 0; j < region_size; j++)
            for (var k = 0; k < cells_size; k++) {
                var id_to = json["temporal_pooler"]["columns"][i][j]["cells"][k]["id"];
                document.getElementById(id_to).style.border = "1px solid #ddd";
            }
}

function show_dendrites(id) {
    clear_all_dendrites();
    var cell = get_cell_by_id(id);
    for (var i = 0; i < cell["dendrites"].length; i++) {
        if (cell["dendrites"][i]["was_active"]) {
            for (var j = 0; j < cell["dendrites"][i]["synapses"].length; j++) {
                var id_to = cell["dendrites"][i]["synapses"][j]["id_to"];
                document.getElementById(id_to).style.borderColor = "red";
            }
        }
    }
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



