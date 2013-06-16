package com.mintyfox.doodlearn;

import java.io.IOException;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;

public class WatchActivity extends Activity {
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		Intent intent = getIntent();
		String vid_url = intent.getStringExtra("vid_url");
		String url = "http://doodlearn1.appspot.com/serve/" + vid_url; // your URL here
		try {
			VideoView videoView = new VideoView(this);
			setContentView(videoView);
			//Use a media controller so that you can scroll the video contents
			//and also to pause, start the video.
			MediaController mediaController = new MediaController(this); 
			mediaController.setAnchorView(videoView);
			videoView.setMediaController(mediaController);
			videoView.setVideoURI(Uri.parse(url));
			videoView.start();
			
		} catch (Exception e) {
			e.printStackTrace();
			Toast.makeText(this, e.toString(), Toast.LENGTH_SHORT).show();
		}
	}
}
