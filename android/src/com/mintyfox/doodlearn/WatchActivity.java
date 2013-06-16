package com.mintyfox.doodlearn;

import java.io.IOException;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Bundle;
import android.view.*;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;

public class WatchActivity extends Activity {
	VideoView videoView;
	int savedLocation;
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, 
                                WindowManager.LayoutParams.FLAG_FULLSCREEN);
		savedLocation = 0;
		Intent intent = getIntent();
		String vid_url = intent.getStringExtra("vid_url");
		String url = "http://doodlearn1.appspot.com/serve/" + vid_url; // your URL here
		setContentView(R.layout.activity_watch);
		videoView = (VideoView) findViewById(R.id.videoView);
		try {
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
	public void onResume() {
		super.onResume();
		videoView.seekTo(savedLocation);
	}
	public void onPause() {
		super.onPause();
		savedLocation = videoView.getCurrentPosition();
		if (videoView.isPlaying()) {
			videoView.pause();
		}
	}
	
}
