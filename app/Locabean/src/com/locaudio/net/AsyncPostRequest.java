package com.locaudio.net;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ExecutionException;

import org.apache.http.client.ClientProtocolException;

import android.os.AsyncTask;

import com.locaudio.net.Requests;

public class AsyncPostRequest<T> extends AsyncTask<Requests, Integer, T> {

	private Class<T> tClass;
	private Map<String, String> postForm = null;
	private String[] urlParams = null;

	public AsyncPostRequest(Class<T> tClass, Map<String, String> postForm,
			String... urlParams) {
		this.tClass = tClass;
		this.postForm = postForm;
		this.urlParams = urlParams;
	}
	
	public T getResponse(Requests reqs) {
		try {
			this.execute(reqs);
			return this.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
			return null;
		} catch (ExecutionException e) {
			e.printStackTrace();
			return null;
		}
	}

	@Override
	protected T doInBackground(Requests... reqs) {
		try {
			return reqs[0].post(this.tClass, this.postForm, this.urlParams);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			return null;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

}
