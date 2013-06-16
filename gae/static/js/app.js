var myPlayer = "";
$(document).ready(function(){
    myPlayer = videojs("video",{"controls":true, "autoplay":true, "preload":true});
    myPlayer.dimensions(800,480);
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";
    var dynamicCount = -1;
    var coId = 0;
    var cuId = 0;
    var prId = 0;
    $("#upload-confused").hide();
    $("#upload-curious").hide();
    $("#upload-practice").hide();

    //var dynamicTimer = setInterval(dynamicUpload, 1000);

    $("#tag-confused").click(function(){
        var time = myPlayer.currentTime();
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "confused"
<<<<<<< Updated upstream
        }, function(data) { 
            console.log(data);
            if (data.url) {
		button.popover({
                placement: 'bottom',
                trigger: 'manual',
                title: 'Need some help? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });
		}
	     else {
		button.popover({
                placement: 'bottom',
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
=======
        }).always(function(data){ alert(data);});
>>>>>>> Stashed changes
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
                placement: 'bottom',
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

    function dynamicUpload() {
        dynamicCount++;
        if (dynamicCount == confused_vpgs[coId].time){
            $("#upload-confused").show();
            $("#upload-confused").data("vpg", confused_vpgs[coId].id);
        } else if (dynamicCount == (confused_vpgs[coId].time + 30)){
            coId++;
            $("#upload-confused").hide();
        }
        if (dynamicCount == curious_vpgs[cuId].time){
            $("#upload-curious").show();
            $("#upload-curious").data("vpg", curious_vpgs[cuId].id);
        } else if (dynamicCount == (confused_vpgs[cuId].time + 30)){
            cuId++;
            $("#upload-curious").hide();
        }

        if (dynamicCount == practice_vpgs[prId].time){
            $("#upload-practice").show();
            $("#upload-practice").data("vpg", practice_vpgs[prId].id);
        } else if (dynamicCount == (practice_vpgs[prId].time + 30)){
            $("#upload-practice").hide();
        }
    }

    $("#upload-confused").click(function () {
        $('#upload-confused').modal({
                                    backdrop:true,
                                    keyboard:true,
                                    show:true,
        });
    });
});
