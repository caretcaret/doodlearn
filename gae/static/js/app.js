$(document).ready(function(){
    var myPlayer = videojs("video",{"controls":true, "autoplay":true, "preload":true});
    myPlayer.dimensions(800,480);
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";

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
