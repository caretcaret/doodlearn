$(document).ready(function(){
    var myPlayer = videojs("video",{"controls":true, "autoplay":true, "preload":true});
    myPlayer.dimensions(800,480);
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";

    $("#tag-confused").click(function(){
        var time = myPlayer.currentTime();
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "confused"
        }, function(data) { 
            console.log(data);
            if (data.url) {
		button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Need some help? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });
		}
	     else {
		button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Need some help? <button type="button" class="close">×</button>',
                content: 'No video is availible yet on this issue :( We will inform you when someone posts a video',
		html: true});
		}
            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
            });
        });
    });

    $("#tag-curious").click(function(){
        var time = myPlayer.currentTime();
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "curious"
        }, function(data) { 
            console.log(data);
	    if(data.url) {
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Are you curious? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });
	    } else {
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Are you curious? <button type="button" class="close">×</button>',
                content: 'No video is availible yet on this issue :( We will inform you when someone posts a video',
                html: true
            })};
            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
            });
        });
    });

    $("#tag-practice").click(function(){
        var time = myPlayer.currentTime();
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "practice"
        }, function(data) { 
            console.log(data);
	   if(data.url) {
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Need some practice? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });
	  } else {
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Need some practice? <button type="button" class="close">×</button>',
                content: 'No video is availible yet on this issue :( We will inform you when someone posts a video',
                html: true
		}); }
            button.popover('show');
            $('.close').click(function() {
                button.popover('hide');
            });
        });
    });

});
