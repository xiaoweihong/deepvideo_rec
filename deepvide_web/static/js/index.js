$(function()
{
    // sync the file input and text input
    $("#local_image").change(function () {
        $("#local_image_path").val($(this).val());
    });

    // bind click to submit online image detect
    $("#online_image_submit").click(function()
    {
        $.post("/detect/online", {"online_image_url": $("#online_image_url").val()}, function(data, status, xhr){
            $("#json_result").text(JSON.stringify(data, null, 4))
            $("#image_result").attr("src", data["image"])
        }, "json");
    });

    // bind click to submit local image detect
    $("#local_image_submit").click(function()
    {
        $("#local_image_form").ajaxSubmit({
            success: function(data) {
                // console.log(data)
                result=data["data"];
                console.log(result["Result"]);
                console.log(result["Result"]["Vehicles"][0]);
                v1=result["Result"]["Vehicles"][0];

                pic_width=result["Result"]["Image"]["Data"]["Width"];
                pic_height=result["Result"]["Image"]["Data"]["Height"];

                v_x=v1["Img"]["Cutboard"]["X"];
                v_y=v1["Img"]["Cutboard"]["Y"];
                v_width=v1["Img"]["Cutboard"]["Width"];
                v_height=v1["Img"]["Cutboard"]["Height"];
                $("#json_result").text(JSON.stringify(data["data"], null, 4));
                $("#image_result").attr("src","data:image/jpeg;base64,"+data["image"]);
                $("#image_result").before("<div class='image_a'></div>");
                console.log('height',v_height)
                console.log('width',v_width)
                console.log('x',v_x)
                console.log('y',v_y)

                 $(".image_a").css({
                        "top":(v_x/pic_width)*100+'%',
                        "left":(v_y/pic_height)*100+'%',
                        "width":(v_width/pic_width)*100+'%',
                        "height":(v_height/pic_height)*100+'%',
                        "position":'absolute',
                        "border":"1px solid red"
                     })

            },
            url: "/local/",
            type: "post",
            dataType: "json"
        });

    });
})
