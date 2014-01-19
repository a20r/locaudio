package com.locaudio.net;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.CharBuffer;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

public class Requests {

	private String ipAddress = null;
	private int port = 80;
	private String url = null;
	private static final int CHAR_BUFFER_SIZE = 256;

	public Requests() {
		this.ipAddress = "localhost";
		this.port = 8000;
		this.url = this.ipAddress + ":" + this.port;
	}

	public Requests(String ipAddress, int port) {
		this.ipAddress = ipAddress;
		this.port = port;
		this.url = this.ipAddress + ":" + this.port;
	}

	public JSONObject post(Map<String, String> paramMap)
			throws ClientProtocolException, IOException, JSONException {
		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost(this.url);

		// Request parameters and other properties.
		List<BasicNameValuePair> params = new ArrayList<BasicNameValuePair>();

		Iterator<Entry<String, String>> it = paramMap.entrySet().iterator();
		Entry<String, String> pair = null;

		while (it.hasNext()) {
			pair = (Entry<String, String>) it.next();
			params.add(new BasicNameValuePair(pair.getKey(), pair.getValue()));
		}

		httppost.setEntity(new UrlEncodedFormEntity(params, "UTF-8"));

		// Execute and get the response.
		HttpResponse response = httpclient.execute(httppost);
		HttpEntity entity = response.getEntity();

		if (entity != null) {
			InputStreamReader reader = new InputStreamReader(
					entity.getContent());
			try {
				CharBuffer target = CharBuffer.allocate(CHAR_BUFFER_SIZE);
				reader.read(target);
				return new JSONObject(target.toString());
			} finally {
				reader.close();
			}
		} else {
			return new JSONObject();
		}
	}
	
	public JSONObject get(String... params) {
		return new JSONObject();
	}
}
