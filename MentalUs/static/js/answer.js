var scale_content;
var question_id = 0;
var auto_next = false;
var sumbit_choice = function () {
    $.ajax({
        url: '/answer/' + $("#scale_id").val(),
        type: 'POST',
        data: 'q=' + $("#question_id").val() + '&a=' + $("#answer_table input:checked").val(),
        async: false,
        dataType: 'json',
        success: function (data) {
            return data['result'];
        }
    });
};
var update_process = function () {
    var s_now = $("#sub_now").text();
    var s_total = $("#sub_total").text();
    var c_width = parseInt((s_now / s_total) * 100) + "%";
    var s_progress = $("#sub_progress");
    s_progress.attr("aria-valuemax", s_total);
    s_progress.attr("aria-valuenow", s_now);
    s_progress.children("span").text(c_width);
    s_progress.css("width", c_width);
};
var generate_choice = function (choices) {
    $("#answer_table tr:eq(0)").html('');
    choices.forEach(function (choice, index) {
        var td = '<td><label for="' + index + '"><input type="radio" value="' + index + '" id="' + index + '" name="answer"/>' + choice + '</label></td>';
        $("#answer_table tr:eq(0)").append(td);
    });
    $("#answer_table input").click(function () {
        if (auto_next) {
            go_next();
        }
    });
};
var show_question = function () {
    var next = $("#next");
    var prev = $("#prev");
    var submit = $("#submit_all");
    $("#question_id").val(question_id);
    switch (question_id) {
        case scale_content.length - 1:
            next.addClass("disabled");
            submit.removeClass("disabled");
            break;
        case 0:
            prev.addClass("disabled");
            break;
        default:
            submit.addClass("disabled");
            prev.removeClass("disabled");
            next.removeClass("disabled");
    }
    var que_str = question_id + 1 + '. ' + scale_content[question_id]['q'];
    $("#question").text(que_str);
    $("#sub_now").text(question_id + 1);
    generate_choice(scale_content[question_id]['a']);
    update_process();
};
var go_next = function () {
    sumbit_choice();
    show_question(++question_id);
};
var go_prev = function () {
    show_question(--question_id);
};
$(document).ready(function () {
    $("#auto_next").click(function () {
        auto_next = !auto_next;
    });
    scale_content = $.parseJSON($("#scale_json").val());
    $("#sub_total").text(scale_content.length);
    show_question();
});