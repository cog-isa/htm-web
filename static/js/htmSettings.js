
// Добавляет новую настройку запуска HTM в БД на сервере для данного пользователя
function addNewConf()
{
   $.post('/add_new_conf/', {text: "hello"},"json")
            .done(function (json) {
                location.reload();
            }).fail(function() {
                alert( "add_new_conf error" );
            })

}


// Удаляет настройку запуска HTM в БД на сервере для данного пользователя
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

