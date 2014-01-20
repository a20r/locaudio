package com.locaudio.api;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

import org.apache.http.client.ClientProtocolException;

import android.os.AsyncTask;

import com.locaudio.net.Requests;

public class Locaudio extends Requests {
	private static final String NAMES_ROUTE = "names";
	private static final String NOTIFY_ROUTE = "notify";
	private static final String LOCATIONS_ROUTE = "locations";

	public Locaudio(String ipAddress, int port) {
		super(ipAddress, port);
	}

	public Location[] getSoundLocations(final String soundName) {

		AsyncTask<Requests, Integer, Location[]> task = new AsyncTask<Requests, Integer, Location[]>() {

			@Override
			protected Location[] doInBackground(Requests... reqs) {
				try {
					return reqs[0].get(Location[].class, LOCATIONS_ROUTE,
							soundName);
				} catch (ClientProtocolException e) {
					e.printStackTrace();
					return null;
				} catch (IOException e) {
					e.printStackTrace();
					return null;
				}
			}

		};

		try {
			task.execute(this);
			return task.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
			return null;
		} catch (ExecutionException e) {
			e.printStackTrace();
			return null;
		}
	}

	public String[] getNames() throws ClientProtocolException, IOException {
		AsyncTask<Requests, Integer, String[]> task = new AsyncTask<Requests, Integer, String[]>() {

			@Override
			protected String[] doInBackground(Requests... reqs) {
				try {
					return reqs[0].get(String[].class, NAMES_ROUTE);
				} catch (ClientProtocolException e) {
					e.printStackTrace();
					return null;
				} catch (IOException e) {
					e.printStackTrace();
					return null;
				}
			}

		};

		try {
			task.execute(this);
			return task.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
			return null;
		} catch (ExecutionException e) {
			e.printStackTrace();
			return null;
		}
	}

	public NotifyResponse notifyEvent(final NotifyForm event)
			throws ClientProtocolException, IOException {
		AsyncTask<Requests, Integer, NotifyResponse> task = new AsyncTask<Requests, Integer, NotifyResponse>() {

			@Override
			protected NotifyResponse doInBackground(Requests... reqs) {
				try {
					return reqs[0].post(NotifyResponse.class, event.toMap(), NOTIFY_ROUTE);
				} catch (ClientProtocolException e) {
					e.printStackTrace();
					return null;
				} catch (IOException e) {
					e.printStackTrace();
					return null;
				}
			}

		};

		try {
			task.execute(this);
			return task.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
			return null;
		} catch (ExecutionException e) {
			e.printStackTrace();
			return null;
		}
	}
}
