$(document).ready(function(){
    var myPlayer = document.getElementById("video");
    var user = $("#tags").data("user");
    var video = $("#tags").data("video");
    var tag_url = "/";

    //temp
    var d = new Date();

    $("#tag-confused").click(function(){
        var time = d.getSeconds();//myPlayer.currentTime();
        $.ajax({
            type: "POST",
            url: tag_url,
            dataType: "json",
            async: false,
            data:JSON.stringify({'user':user,
                                 'video':video,
                                 'time':time,
                                 'point_type':"confused"}),
            success: function(data){
                alert("done");
            },
            failure: function(data){
                alert("fail");
            }
        });
    });

    $("#tag-curious").click(function(){
        var time = d.getSeconds();//myPlayer.currentTime();
        $.ajax({
            type: "POST",
            url: tag_url,
            dataType: "json",
            async: false,
            data:JSON.stringify({'user':user,
                                 'video':video,
                                 'time':time,
                                 'point_type':"curious"}),
            success: function(data){
                alert("done");
            },
            failure: function(data){
                alert("fail");
            }
        });
    });

    $("#tag-practice").click(function(){
        var time = d.getSeconds();//myPlayer.currentTime();
        $.ajax({
            type: "POST",
            url: tag_url,
            dataType: "json",
            async: false,
            data:JSON.stringify({'user':user,
                                 'video':video,
                                 'time':time,
                                 'point_type':"practice"}),
            success: function(data){
                alert("done");
            },
            failure: function(data){
                alert("fail");
            }
        });
    });

});