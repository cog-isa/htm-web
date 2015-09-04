$('#myButton').on('click', function () {
        $.post('/add_new_conf/', {
            text: "hello"
        }).done(function (json) {

        }).fail(function () {
            alert("error");
        })
    },
    dataType = "json");