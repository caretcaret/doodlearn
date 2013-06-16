package com.mintyfox.doodlearn;

import java.util.List;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

public class RecordFragment extends Fragment {
	public int LOAD_VIDEO = 42;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
        Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.record_view, container, false);
        Button b1 = (Button) v.findViewById(R.id.button1);
        Button b2 = (Button) v.findViewById(R.id.button2);
        b1.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// open file storage
				Intent chooseVideoIntent = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI);
				//Intent chooseVideoIntent = new Intent(Intent.ACTION_GET_CONTENT);
				chooseVideoIntent.setType("video/*");
				startActivityForResult(chooseVideoIntent, LOAD_VIDEO);
			}
        });
        b2.setOnClickListener(new OnClickListener() {
        	@Override
        	public void onClick(View v) {
        		// open camera app
        		Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        		PackageManager packageManager = v.getContext().getPackageManager();
        		List<ResolveInfo> activities = packageManager.queryIntentActivities(takeVideoIntent, 0);
        		boolean isIntentSafe = activities.size() > 0;
        		if (isIntentSafe)
        			startActivityForResult(takeVideoIntent, LOAD_VIDEO);
        		else {
        			Context context = v.getContext();
        			Toast.makeText(context, "You do not have a video recording application!", Toast.LENGTH_SHORT).show();
        		}
        			
        	}
        });
        return v;
    }
    
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
    	if (requestCode == LOAD_VIDEO) {
    		if (resultCode == Activity.RESULT_OK) {
    			// TODO
    			Uri videoUri = intent.getData();
    			Context context = getActivity();
    			Toast.makeText(context, "Not implemented: " + videoUri.toString(), Toast.LENGTH_SHORT).show();
    		} else {
    			// do nothing
    		}
    	}
    }
}