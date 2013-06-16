$(document).ready(function(){
    var myPlayer = _V_("video");
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";

    //temp
    var d = new Date();

    $("#tag-confused").click(function(){
        var time = myPlayer.currentTime();
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "confused"
        }, function(data) { 
            console.log(data);
        });
    });

    $("#tag-curious").click(function(){
        var time = myPlayer.currentTime();
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "curious"
        })
        .done(function(data) {
            console.log(data);
        });
    });

    $("#tag-practice").click(function(){
        var time = myPlayer.currentTime();
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "practice"
        }, function(data) { 
            console.log(data);
        });
    });

});
