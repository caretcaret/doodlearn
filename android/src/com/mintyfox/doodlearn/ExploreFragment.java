package com.mintyfox.doodlearn;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.view.*;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class ExploreFragment extends ListFragment {
	public final String VID_LISTING_URL = "http://doodlearn1.appspot.com/api/list";
	public ArrayList<String> vid_titles;
	public ArrayList<Long> vid_ids;
	public ArrayList<String> vid_urls;
	
	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
	  super.onActivityCreated(savedInstanceState);
	  String[] values = new String[] {};
	  new GetListTask().execute(VID_LISTING_URL);
	  ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActivity(),
	      android.R.layout.simple_list_item_1, values);
	  setListAdapter(adapter);
	}

	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
	  // Do something with the data
		Context context = getActivity();
		Intent intent = new Intent(context, WatchActivity.class);
		intent.putExtra("vid_url", "http://doodlearn1.appspot.com/serve/" + vid_urls.get(position));
		startActivity(intent);
		//Toast.makeText(context, vid_ids.get(position).toString()
		//		+ vid_urls.get(position), Toast.LENGTH_SHORT).show();
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
	
	public class GetListTask extends AsyncTask<String, Void, String> {

		@Override
		protected String doInBackground(String... urls) {
			String output = "";
			Context context = getActivity();
			try {
			   URL url = new URL(urls[0]);
			   HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
			   InputStream in = new BufferedInputStream(urlConnection.getInputStream());
			   output = readStream(in);
			   urlConnection.disconnect();
			} catch (Exception e) {
			  Toast.makeText(context, e.toString(), Toast.LENGTH_SHORT).show();
			}
			return output;
		}
		
		@Override
		protected void onPostExecute(String result) {
			Context context = getActivity();
			ArrayList<String> titles = new ArrayList<String>();
			ArrayList<Long> ids = new ArrayList<Long>();
			ArrayList<String> urls = new ArrayList<String>();
			JSONArray ja;
			try {
				ja = new JSONArray(result);
			   int len = ja.length();
			   for (int i=0;i<len;i++){ 
				JSONArray ja_inner = ja.getJSONArray(i);
			    titles.add(ja_inner.get(0).toString());
			    ids.add(ja_inner.getLong(1));
			    urls.add(ja_inner.get(2).toString());
			   }
			} catch (JSONException e) {
				Toast.makeText(context, e.toString(), Toast.LENGTH_SHORT).show();
			}
			ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActivity(),
				  android.R.layout.simple_list_item_1, titles);
				  setListAdapter(adapter);
			vid_titles = titles;
			vid_ids = ids;
			vid_urls = urls;
		}
		
	}

}
