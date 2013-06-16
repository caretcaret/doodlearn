package com.mintyfox.doodlearn;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.FormBodyPart;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class RecordFragment extends Fragment {
	public int LOAD_VIDEO = 42;
	public EditText titleView;
	public EditText descriptionView;
	public String formTitle = "";
	public String formDesc = "";
	public String formVidURI = "";
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, 
        Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.record_view, container, false);
        Button b1 = (Button) v.findViewById(R.id.button1);
        Button b2 = (Button) v.findViewById(R.id.button2);
        titleView = (EditText) v.findViewById(R.id.editText1);
        descriptionView = (EditText) v.findViewById(R.id.editText2);
        
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
    			formTitle = titleView.getText().toString();
    			formDesc = descriptionView.getText().toString();
    			formVidURI = videoUri.toString();
    			new UploadVideoTask().execute(formTitle, formDesc, formVidURI);
    			Toast.makeText(context, "Uploading...", Toast.LENGTH_LONG).show();
    		} else {
    			// do nothing
    		}
    	}
    }
	public static String readStream(InputStream in) {
		  BufferedReader reader = null;
		  StringBuilder out = new StringBuilder();
		  try {
		    reader = new BufferedReader(new InputStreamReader(in));
		    String line = "";
		    while ((line = reader.readLine()) != null) {
		      out.append(line);
		    }
		  } catch (IOException e) {
		    e.printStackTrace();
		  } finally {
		    if (reader != null) {
		      try {
		        reader.close();
		      } catch (IOException e) {
		        e.printStackTrace();
		        }
		    }
		  }
		 return out.toString();
		} 
	public String getPath(Uri contentUri) {
	    String res = null;
	    String[] proj = { MediaStore.Images.Media.DATA };
	    Cursor cursor = getActivity().getContentResolver().query(contentUri, proj, null, null, null);
	    if(cursor.moveToFirst()){;
	       int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
	       res = cursor.getString(column_index);
	    }
	    cursor.close();
	    return res;
	}
    
    public class UploadVideoTask extends AsyncTask<String, Void, JSONObject> {

		@Override
		protected JSONObject doInBackground(String... data) {
			JSONObject jo = new JSONObject();
			try {
				jo = new JSONObject("{'video_id': \"\", 'video_url': ''}");
			} catch (JSONException e1) {
				Log.e("jsonexception", e1.toString());
			}
			String urlgetter = "http://doodlearn1.appspot.com/api/get_upload_url";
			
			try {
			// get upload url for video
			URL url = new URL(urlgetter);
		    HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
		    InputStream in = new BufferedInputStream(urlConnection.getInputStream());
		    String uploadURL = readStream(in);
		    /*if (uploadURL.substring(uploadURL.length() - 1).equals("/")) {
		    	uploadURL = uploadURL.substring(0, uploadURL.length() - 1);
		    }*/
		    //uploadURL += "?noredirect=true";
		    urlConnection.disconnect();
		    
		    Log.e("Upload url", uploadURL);
			
		    // upload data
			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(uploadURL);
			String title = data[0];
			String desc = data[1];
			String vidURI = data[2];
			Log.e("video uri", vidURI);
			MultipartEntity entity = new MultipartEntity();
			entity.addPart("name", new StringBody(title));
			entity.addPart("description", new StringBody(desc));
			entity.addPart("category", new StringBody("Fun"));
			entity.addPart("noredirect", new StringBody("true"));
			Log.e("video path", getPath(Uri.parse(vidURI)));
			File videoFile = new File(getPath(Uri.parse(vidURI)));
			entity.addPart("video", new FileBody(videoFile));
			
			httppost.setEntity(entity);
			HttpResponse response = httpclient.execute(httppost);
			
			// get string content
			HttpEntity responseEntity = response.getEntity();
			String responseString = EntityUtils.toString(responseEntity, "UTF-8");
			
			// json decode response
			Log.e("response string", responseString);
			jo = new JSONObject(responseString);
			} catch (Exception e) {
				Log.e("uploadvideotask", e.toString());
				e.printStackTrace();
			}
			return jo;
		}
		
		@Override
		protected void onPostExecute(JSONObject jo) {
			Context context = getActivity();
			try {
				String videoID = jo.getString("video_id");
				String videoURL = jo.getString("video_url");
				if (videoID != "") {
					Intent intent = new Intent(context, WatchActivity.class);
					intent.putExtra("vid_url", "http://doodlearn1.appspot.com" + videoURL);
					startActivity(intent);
				}
			} catch (Exception e) {
				Toast.makeText(context, "There was an error uploading! " + e.toString(), Toast.LENGTH_LONG).show();
			}
		}
		
	}
    

}