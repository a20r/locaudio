package com.locaudio.net;

import java.io.IOException;
import java.io.InputStreamReader;
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
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import com.google.gson.Gson;

public class Requests {

	private String ipAddress = null;
	private int port = 80;
	private String url = null;

	public Requests() {
		this.ipAddress = "localhost";
		this.port = 8000;
		this.url = "http://" + this.ipAddress + ":" + this.port;
	}

	public Requests(String ipAddress, int port) {
		this.ipAddress = ipAddress;
		this.port = port;
		this.url = "http://" + this.ipAddress + ":" + this.port;
	}

	@SuppressWarnings({ "rawtypes", "unchecked" })
	public <T> T post(Class<T> classType, Map<String, ?> paramMap,
			String... urlParams) throws ClientProtocolException, IOException {

		String requestUrl = this.concatWithUrl(urlParams);
		HttpClient httpClient = new DefaultHttpClient();
		HttpPost httpPost = new HttpPost(requestUrl);

		// Request parameters and other properties.
		List<BasicNameValuePair> params = new ArrayList<BasicNameValuePair>();

		Iterator<?> it = paramMap.entrySet().iterator();
		Entry<String, String> pair = null;

		while (it.hasNext()) {
			pair = (Entry) it.next();
			params.add(new BasicNameValuePair(pair.getKey(), pair.getValue()));
		}

		httpPost.setEntity(new UrlEncodedFormEntity(params, "UTF-8"));

		// Execute and get the response.
		HttpResponse response = httpClient.execute(httpPost);
		HttpEntity entity = response.getEntity();

		return entityToObject(entity, classType);
	}

	public <T> T get(Class<T> classType, String... urlParams)
			throws ClientProtocolException, IOException {

		String requestUrl = this.concatWithUrl(urlParams);
		HttpClient httpClient = new DefaultHttpClient();
		HttpGet httpGet = new HttpGet(requestUrl);
		HttpContext localContext = new BasicHttpContext();

		HttpResponse response = httpClient.execute(httpGet, localContext);
		HttpEntity entity = response.getEntity();

		return entityToObject(entity, classType);
	}

	protected static <T> T entityToObject(HttpEntity entity, Class<T> classType)
			throws IllegalStateException, IOException {
		if (entity != null) {
			InputStreamReader reader = new InputStreamReader(
					entity.getContent());
			try {
				Gson gson = new Gson();
				return gson.fromJson(reader, classType);
			} finally {
				reader.close();
			}
		} else {
			return null;
		}
	}

	protected String concatWithUrl(String... urlParams) {
		String retString = this.url;
		for (String urlParam : urlParams) {
			retString += "/" + urlParam;
		}
		return retString;
	}

}
