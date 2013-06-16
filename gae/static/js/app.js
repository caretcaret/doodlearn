var myPlayer = "";
$(document).ready(function(){
    myPlayer = videojs("video",{"controls":true, "autoplay":true, "preload":true});
    myPlayer.dimensions(800,480);
    var video = $("#tags-app").data("video");
    var tag_url = "/parsevp";
    var upload_url = "/api/get_upload_url?json=true";

    var dynamicCount = -1;
    var coId = 0;
    var cuId = 0;
    var prId = 0;

    var player = $('video');
    var player_elem = player.get(0)

    $("#upload-confused").hide();
    $("#upload-curious").hide();
    $("#upload-practice").hide();

    var dynamicTimer = setInterval(dynamicUpload, 1000);

    $("#tag-confused").click(function(){
        var time = player_elem.currentTime;
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "confused"
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
    });

    $("#tag-curious").click(function(){
        var time = player_elem.currentTime;
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
                placement: 'bottom',
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
        var time = player_elem.currentTime;
        var button = $(this);
        $.getJSON(tag_url, {
                                video: video,
                                time: time,
                                point_type: "practice"
        }, function(data) { 
            console.log(data);
	   if(data.url) {
            button.popover({
                placement: 'bottom',
                trigger: 'manual',
                title: 'Need some practice? <button type="button" class="close">×</button>',
                content: 'Click for a more detailed explanation: <a href="' + data.url + '"><img src="' + data.thumbnail + '"/></a>',
                html: true
            });
	  } else {
            button.popover({
                placement: 'bottom',
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

        if (coId < confused_vpgs.length) {
            if (dynamicCount == confused_vpgs[coId].time){
                $("#upload-confused").show();
                $("#upload-confused").data("vpg", confused_vpgs[coId].id);
            } else if (dynamicCount == (confused_vpgs[coId].time + 30)){
                coId++;
                $("#upload-confused").hide();
            }
        }
        if (cuId < curious_vpgs.length) {
            if (dynamicCount == curious_vpgs[cuId].time){
                $("#upload-curious").show();
                $("#upload-curious").data("vpg", curious_vpgs[cuId].id);
            } else if (dynamicCount == (curious_vpgs[cuId].time + 30)){
                cuId++;
                $("#upload-curious").hide();
            }
        }

        if (prId < practice_vpgs.length) {
            if (dynamicCount == practice_vpgs[prId].time){
                $("#upload-practice").show();
                $("#upload-practice").data("vpg", practice_vpgs[prId].id);
            } else if (dynamicCount == (practice_vpgs[prId].time + 30)){
                prId++;
                $("#upload-practice").hide();
            }
        }
    }

    $("#upload-curious").click(function () {
        player_elem.pause();
        var button = $(this);
        var vpg = $("#upload-curious").data("vpg")

        $.getJSON(upload_url, function(data) {
            console.log(data);
            var header = '<form action="' + data + '" method="POST" enctype="multipart/form-data"';
            var name = '<div> <label> <div class="field-p"> Video Name: </div></label><input type="text" name="name"></div><br>';
            var description = '<div><label><div class="field-p"> Description: </div></label> <textarea name="description" rows="3"></textarea></div><br>';
            var file = '<div><label><div class="field-p"> Upload File </div></label>';
            var file_1 = '<span><input type="file" style="visibility:hidden; width: 1px;" id=' + "'${multipartFilePath}'" + ' name="video" onchange="$(this).parent().find('+ "'span'" +').html($(this).val().replace('+ "'C:\\fakepath\\'" + ', '+ "''" + '))"  />'; 
            var file_2 = '<input class="btn btn-small" type="button" value="Upload Video.." name="video" onclick="$(this).parent().find('+ "'input[type=file]'" + ').click();" accept="video/*;capture=camcorder"/>';
            var file_3 = '&nbsp;<span class="badge badge-important" ></span></span></div><br>';
            var vpg_f = '<input type="hidden" name="vpg_id" value="' + vpg + '"><br>';
            var parent_f = '<input type="hidden" name="parent_video" value="' + video + '"><br>';
            var submit_f = '<div><input type="submit" name="submit" class="btn btn-primary btn-large" value="Submit"/>';
            var form = header + name + description + file + file_1 + file_2 + file_3 + vpg_f + parent_f + submit_f;
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Want to help? <button type="button" class="close">×</button>',
                content: form,
                html: true
            });

            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
                player_elem.play();
            });
        });
    });

    
    $("#upload-confused").click(function () {
        player_elem.pause();
        var button = $(this);
        var vpg = $("#upload-confused").data("vpg")

        $.getJSON(upload_url, function(data) {
            console.log(data);
            var header = '<form action="' + data + '" method="POST" enctype="multipart/form-data"';
            var name = '<div> <label> <div class="field-p"> Video Name: </div></label><input type="text" name="name"></div><br>';
            var description = '<div><label><div class="field-p"> Description: </div></label> <textarea name="description" rows="3"></textarea></div><br>';
            var file = '<div><label><div class="field-p"> Upload File </div></label>';
            var file_1 = '<span><input type="file" style="visibility:hidden; width: 1px;" id=' + "'${multipartFilePath}'" + ' name="video" onchange="$(this).parent().find('+ "'span'" +').html($(this).val().replace('+ "'C:\\fakepath\\'" + ', '+ "''" + '))"  />'; 
            var file_2 = '<input class="btn btn-small" type="button" value="Upload Video.." name="video" onclick="$(this).parent().find('+ "'input[type=file]'" + ').click();" accept="video/*;capture=camcorder"/>';
            var file_3 = '&nbsp;<span class="badge badge-important" ></span></span></div><br>';
            var vpg_f = '<input type="hidden" name="vpg_id" value="' + vpg + '"><br>';
            var parent_f = '<input type="hidden" name="parent_video" value="' + video + '"><br>';
            var submit_f = '<div><input type="submit" name="submit" class="btn btn-primary btn-large" value="Submit"/>';
            var form = header + name + description + file + file_1 + file_2 + file_3 + vpg_f + parent_f + submit_f;
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Want to help? <button type="button" class="close">×</button>',
                content: form,
                html: true
            });

            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
                player_elem.play();
            });
        });
    });

    $("#upload-practice").click(function () {
        player_elem.pause();
        var button = $(this);
        var vpg = $("#upload-practice").data("vpg")

        $.getJSON(upload_url, function(data) {
            console.log(data);
            var header = '<form action="' + data + '" method="POST" enctype="multipart/form-data"';
            var name = '<div> <label> <div class="field-p"> Video Name: </div></label><input type="text" name="name"></div><br>';
            var description = '<div><label><div class="field-p"> Description: </div></label> <textarea name="description" rows="3"></textarea></div><br>';
            var file = '<div><label><div class="field-p"> Upload File: </div></label>';
            var file_1 = '<span><input type="file" style="visibility:hidden; width: 1px;" id=' + "'${multipartFilePath}'" + ' name="video" onchange="$(this).parent().find('+ "'span'" +').html($(this).val().replace('+ "'C:\\fakepath\\'" + ', '+ "''" + '))"  />'; 
            var file_2 = '<input class="btn btn-small" type="button" value="Upload Video.." name="video" onclick="$(this).parent().find('+ "'input[type=file]'" + ').click();" accept="video/*;capture=camcorder"/>';
            var file_3 = '&nbsp;<span class="badge badge-important" ></span></span></div><br>';
            var vpg_f = '<input type="hidden" name="vpg_id" value="' + vpg + '"><br>';
            var parent_f = '<input type="hidden" name="parent_video" value="' + video + '">';
            var submit_f = '<div><input type="submit" name="submit" class="btn btn-primary btn-large" value="Submit"/>';
            var form = header + name + description + file + file_1 + file_2 + file_3 + vpg_f + parent_f + submit_f;
            button.popover({
                placement: 'left',
                trigger: 'manual',
                title: 'Want to help? <button type="button" class="close">×</button>',
                content: form,
                html: true
            });

            button.popover('show');

            $('.close').click(function() {
                button.popover('hide');
                player_elem.play();
            });
        });
    });

});
