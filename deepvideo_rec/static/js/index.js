$(function()
{
    // sync the file input and text input
    $("#local_image").change(function () {
        $("#local_image_path").val($(this).val());
    });

    // bind click to submit online image detect
    $("#online_image_submit").click(function()
    {
        $.post("/rec/online", {"online_image_url": $("#online_image_url").val()}, function(data, status, xhr){
            $("#json_result").text(JSON.stringify(data, null, 4))
            $("#json_text").text(JSON.stringify(data["result_data"], null, 4));
                $("#image_result").attr("src","data:image/jpeg;base64,"+data["image"]);
                $("#image_result").before("<div class='image_a'></div>");
        }, "json");
    });

    // bind click to submit local image detect
    $("#local_image_submit").click(function()
    {
        $("#local_image_form").ajaxSubmit({
            success: function(data) {
                console.log(data)
                result=data["data"];
                $("#json_result").text(JSON.stringify(data["data"], null, 4));
                $("#json_text").text(JSON.stringify(data["result_data"], null, 4));
                $("#image_result").attr("src","data:image/jpeg;base64,"+data["image"]);
                $("#image_result").before("<div class='image_a'></div>");
            },
            url: "/rec/local",
            type: "post",
            dataType: "json"
        });

    });
})
