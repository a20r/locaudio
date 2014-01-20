package com.locaudio.api;

import java.io.IOException;

import org.apache.http.client.ClientProtocolException;

import com.locaudio.net.*;

public class Locaudio extends Requests {
	private static final String NAMES_ROUTE = "names";
	private static final String NOTIFY_ROUTE = "notify";
	private static final String LOCATIONS_ROUTE = "locations";

	public Locaudio(String ipAddress, int port) {
		super(ipAddress, port);
	}

	public SoundLocation[] getSoundLocations(final String soundName) {
		AsyncGetRequest<SoundLocation[]> agr = new AsyncGetRequest<SoundLocation[]>(
				SoundLocation[].class, LOCATIONS_ROUTE, soundName);
		return agr.getResponse(this);
	}

	public String[] getNames() throws ClientProtocolException, IOException {
		AsyncGetRequest<String[]> agr = new AsyncGetRequest<String[]>(
				String[].class, NAMES_ROUTE);
		return agr.getResponse(this);
	}

	public NotifyResponse notifyEvent(final NotifyForm event)
			throws ClientProtocolException, IOException {
		AsyncPostRequest<NotifyResponse> apr = new AsyncPostRequest<NotifyResponse>(
				NotifyResponse.class, event.toMap(), NOTIFY_ROUTE);

		return apr.getResponse(this);
	}
}
