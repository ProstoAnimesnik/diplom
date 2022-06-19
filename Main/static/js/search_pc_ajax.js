$(document).ready(function () {
    // Живой поиск
    var post_query = function () {

        $.ajax({
            url: $("#url_this_page").attr("data-url"), // url текущей странички
            data: {
                gg: $("#search").val(), // значения из инпут поля
            },
            data_type: "html",
            type: "GET",
            // если успешно, то
            success: function (data) {
                $('#aboba').html(data);
            },
            error: function (xhr, errmsg, err) {
                alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    }
    $("#search").keyup(post_query);

});