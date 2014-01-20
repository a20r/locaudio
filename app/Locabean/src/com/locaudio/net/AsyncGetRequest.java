package com.locaudio.net;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

import org.apache.http.client.ClientProtocolException;

import android.os.AsyncTask;

import com.locaudio.net.Requests;

public class AsyncGetRequest<T> extends AsyncTask<Requests, Integer, T> {

	private Class<T> tClass;
	private String[] urlParams = null;

	public AsyncGetRequest(Class<T> tClass, String... urlParams) {
		this.tClass = tClass;
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
			return reqs[0].get(this.tClass, this.urlParams);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			return null;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

}
