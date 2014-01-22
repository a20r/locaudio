package com.locaudio.net;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

import org.apache.http.client.ClientProtocolException;

import android.os.AsyncTask;

import com.locaudio.interfaces.Mappable;
import com.locaudio.net.Requests;

public abstract class AsyncPostRequest<T> extends
		AsyncTask<Requests, Integer, T> {

	private Class<T> tClass;
	private Mappable<String, String> postForm = null;
	private String[] urlParams = null;

	public abstract void runOnceReceivedResponse(T response);

	public AsyncPostRequest(Class<T> tClass, Mappable<String, String> postForm,
			String... urlParams) {
		this.tClass = tClass;
		this.postForm = postForm;
		this.urlParams = urlParams;
	}

	public AsyncPostRequest(Class<T> tClass, String... urlParams) {
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
		
		T resp = null;
		try {
			resp = reqs[0].post(this.tClass, this.postForm.toMap(),
					this.urlParams);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		runOnceReceivedResponse(resp);
		return resp;
	}

	public AsyncPostRequest<T> setPostForm(Mappable<String, String> postForm) {
		this.postForm = postForm;
		return this;
	}

}
