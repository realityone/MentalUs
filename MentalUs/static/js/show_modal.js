/**
 * Created by realityone on 15-6-3.
 */
var set_modal = function (announcement_id) {
    $.ajax({
        url: "/announcement/"+announcement_id,
        type: "GET",
        dataType: "json",
        async: false,
        success: function (data) {
            $("#detail_title").text(data['title']);
            $("#detail_content").text(data['content']);
            return true;
        },
        error: function (xo, e, eo) {
            alert(e);
            return false;
        }
    })
};