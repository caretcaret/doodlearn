$(document).ready(function(){
    var myPlayer = _V_("video");
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";

    //temp
    var d = new Date();

    $("#tag-confused").click(function(){
        var time = myPlayer.currentTime();
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "confused"
        }, function(data) { 
            console.log(data);
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Need some help? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });

            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
            });
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
