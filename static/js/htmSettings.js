
// ��������� ����� ��������� ������� HTM � �� �� ������� ��� ������� ������������
function addNewConf()
{
   $.post('/add_new_conf/', {text: "hello"},"json")
            .done(function (json) {
                location.reload();
            }).fail(function() {
                alert( "add_new_conf error" );
            })

}


// ������� ��������� ������� HTM � �� �� ������� ��� ������� ������������
function removeConf(id)
{
   $.post('/remove_conf/', {ident:id},"json")
            .done(function (json) {
                location.reload();
            }).fail(function() {
                alert( "remove_conf error" );
            })

}
/*
$( document ).ready(function() {
    $('.panel-collapse').collapse("hide");
});
*/


$('#myButton').on('click', function () {
 $.post('/add_new_conf/', {
        text: "hello"
    }).done(function (json) {

    }).fail(function() {
        alert( "error" );
    })
},
dataType="json")