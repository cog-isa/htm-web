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
var temporal_error_chart = null;

function draw_input_data() {
    clear_element("input_data");

    for (var i = 0; i < json_store["input"].length; i++) {
        for (var j = 0; j < json_store["input"][i].length; j++) {

            var cell_str1 = '<a class="thumbnail htm_ceil"></a>';
            if (json_store["input"][i][j] == 1)
                cell_str1 = '<a class="thumbnail btn-success htm_ceil"></a>';
            var cell_elem2 = create_element("cell_", cell_str1);

            document.getElementById("input_data").appendChild(cell_elem2);
        }
        var tr1 = '<br>';
        var tr_element1 = create_element("column_", tr1);
        document.getElementById("input_data").appendChild(tr_element1);
    }
}

function draw_compress_data() {
    clear_element("compress_input");

    console.log(json_store["compress_input"]);
    for (var i = 0; i < json_store["compress_input"].length; i++) {
        for (var j = 0; j < json_store["compress_input"][i].length; j++) {

            var cell_str11 = '<a class="thumbnail htm_ceil"></a>';
            if (json_store["compress_input"][i][j] == 1)
                cell_str11 = '<a class="thumbnail btn-success htm_ceil"></a>';
            var cell_elem22 = create_element("cell_", cell_str11);

            document.getElementById("compress_input").appendChild(cell_elem22);
        }
        var tr12 = '<br>';
        var tr_element12 = create_element("column_", tr12);
        document.getElementById("compress_input").appendChild(tr_element12);
    }
}

function draw_temporal_pool() {
    clear_element("viz");
    var region_size = json_store["temporal_pooler"]["region_size"];
    var cells_size = json_store["temporal_pooler"]["columns"][0][0]["cells"].length;
    for (var i = 0; i < region_size; i++) {

        for (var j = 0; j < region_size; j++) {
            var column_str = '<div id="region_" class="thumbnail htm_column" ></div>';
            var column = create_element("column_", column_str);
            document.getElementById("viz").appendChild(column);
            for (var k = 0; k < cells_size; k++) {

                var cell_str = '';
                var id = json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["id"];
                if (json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 1)
                    cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail htm_cell"></a>';
                if (json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 2)
                    cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail htm_cell btn-success"></a>';
                if (json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["state"] == 3)
                    cell_str = '<a onclick="show_dendrites(' + id + ')" id = "' + id + '"class="thumbnail htm_cell btn-warning"></a>';

                var cell_elem = create_element("cell_", cell_str);
                column.appendChild(cell_elem);
            }
        }
        var tr = '<br>';
        var tr_element = create_element("column_", tr);
        document.getElementById("viz").appendChild(tr_element);
    }
}

// получаем текущие данные с сервера
function get_htm_data() {
    $.post('/get_htm_data/', {}).done(function (json) {
            json_store = json;
            console.log(json);
            draw_input_data();
            draw_compress_data();
            draw_temporal_pool();

            draw_temporal_error_chart();
        }
    );
}

// останавливаем htm сервер,но ненадо пользоваться этой штукой, сокет лучше вообще не выключать, если он был запущен...
function stop_htm_server() {
    $.post('/stop_htm_server/', {}).done(function (json) {
            json_store = json;
            draw_input_data();
            draw_compress_data();
            draw_temporal_pool();

            draw_temporal_error_chart();
        }
    );
}

// Запускаем выбранную конфигурацию на исполнение
function move_and_get_htm_data() {
    $.post('/move_and_get_htm_data/', {}).done(function (json) {
            json_store = json;
            draw_input_data();
            draw_compress_data();
            draw_temporal_pool();

            draw_temporal_error_chart();
        }
    );
}


// Делаем 10 шагов
function move10_and_get_htm_data() {
    $.post('/move10_and_get_htm_data/', {}).done(function (json) {
            json_store = json;
            draw_input_data();
            draw_compress_data();
            draw_temporal_pool();

            draw_temporal_error_chart();
        }
    );
}

// Делаем 100 шагов
function move100_and_get_htm_data() {
    $.post('/move100_and_get_htm_data/', {}).done(function (json) {
            json_store = json;
            draw_input_data();
            draw_compress_data();
            draw_temporal_pool();

            draw_temporal_error_chart();
        }
    );
}

function turn_on_htm_server(settings_id) {
    $.post('/turn_on_htm_server/', {
        settings_id: settings_id
    }).done(function (json) {
            console.log("its ok");
            window.location.replace("/htmRun/");

        }
    );
}

function draw_temporal_error_chart() {
    if (temporal_error_chart == null) {
        temporal_error_chart = new google.charts.Line(document.getElementById('linechart_material'));
    }
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Шаг алгоритма');
    data.addColumn('number', 'Корректность предсказания');
    var correctness_data = [];
    var sum = 0;
    var av_cor_size = json_store["temporal_pooler"]["average_correctness_max_size"];
    var current_step = json_store["temporal_pooler"]["correctness_steps"];
    var start = Math.max(0, current_step - av_cor_size);
    debug_add_line(current_step);
    debug_add_line(av_cor_size);
    for (var i in json_store["temporal_pooler"]["average_correctness"]) {
        correctness_data.push([start + parseInt(i), 100 * json_store["temporal_pooler"]["average_correctness"][i]]);
    }
    data.addRows(correctness_data);

    var options = {
        chart: {
            //title: '',
            //subtitle: ''
        },
        width: 700,
        height: 450,
        axes: {
            x: {
                0: {side: 'top'}
            }
        }
    };


    temporal_error_chart.draw(data, options);
}

function get_cell_by_id(id) {
    var region_size = json_store["temporal_pooler"]["region_size"];
    var cells_size = json_store["temporal_pooler"]["columns"][0][0]["cells"].length;
    for (var i = 0; i < region_size; i++)
        for (var j = 0; j < region_size; j++)
            for (var k = 0; k < cells_size; k++)
                if (id == json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["id"])
                    return json_store["temporal_pooler"]["columns"][i][j]["cells"][k];
}

function clear_all_dendrites() {
    var region_size = json_store["temporal_pooler"]["region_size"];
    var cells_size = json_store["temporal_pooler"]["columns"][0][0]["cells"].length;
    for (var i = 0; i < region_size; i++)
        for (var j = 0; j < region_size; j++)
            for (var k = 0; k < cells_size; k++) {
                var id_to = json_store["temporal_pooler"]["columns"][i][j]["cells"][k]["id"];
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

function debug_add_line(line) {
    var li = document.createElement('LI');
    li.innerHTML = line;
    var q = document.getElementById("debugID");
    q.appendChild(li);
}



