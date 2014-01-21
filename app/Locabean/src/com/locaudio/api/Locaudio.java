package com.locaudio.api;

import com.locaudio.functional.Function;
import com.locaudio.net.*;

public class Locaudio extends Requests {
	private static final String NAMES_ROUTE = "names";
	private static final String NOTIFY_ROUTE = "notify";
	private static final String LOCATIONS_ROUTE = "locations";

	public Locaudio(String ipAddress, int port) {
		super(ipAddress, port);
	}

	public AsyncGetRequest<SoundLocation[]> getSoundLocations(
			final String soundName, final Function<SoundLocation[]> callback) {

		AsyncGetRequest<SoundLocation[]> agr = new AsyncGetRequest<SoundLocation[]>(
				SoundLocation[].class, LOCATIONS_ROUTE, soundName) {

			@Override
			public void runOnceReceivedResponse(SoundLocation[] response) {
				callback.call(response);
			}

		};

		agr.execute(this);

		return agr;
	}

	@Deprecated
	public SoundLocation[] getSoundLocations(final String soundName) {

		AsyncGetRequest<SoundLocation[]> agr = new AsyncGetRequest<SoundLocation[]>(
				SoundLocation[].class, LOCATIONS_ROUTE, soundName) {

			@Override
			public void runOnceReceivedResponse(SoundLocation[] response) {
			}

		};
		
		return agr.getResponse(this);
	}

	public AsyncGetRequest<String[]> getNames(final Function<String[]> callback) {

		AsyncGetRequest<String[]> agr = new AsyncGetRequest<String[]>(
				String[].class, NAMES_ROUTE) {

			@Override
			public void runOnceReceivedResponse(String[] response) {
				callback.call(response);
			}

		};
		
		agr.execute(this);
		
		return agr;
	}

	@Deprecated
	public String[] getNames() {
		AsyncGetRequest<String[]> agr = new AsyncGetRequest<String[]>(
				String[].class, NAMES_ROUTE) {

			@Override
			public void runOnceReceivedResponse(String[] response) {
			}

		};
		return agr.getResponse(this);
	}

	public AsyncPostRequest<NotifyResponse> notifyEvent(final NotifyForm event,
			final Function<NotifyResponse> callback) {

		AsyncPostRequest<NotifyResponse> apr = new AsyncPostRequest<NotifyResponse>(
				NotifyResponse.class, event.toMap(), NOTIFY_ROUTE) {

			@Override
			public void runOnceReceivedResponse(NotifyResponse response) {
				callback.call(response);
			}

		};
		
		apr.execute(this);

		return apr;
	}

	@Deprecated
	public NotifyResponse notifyEvent(final NotifyForm event) {

		AsyncPostRequest<NotifyResponse> apr = new AsyncPostRequest<NotifyResponse>(
				NotifyResponse.class, event.toMap(), NOTIFY_ROUTE) {

			@Override
			public void runOnceReceivedResponse(NotifyResponse response) {
			}

		};

		return apr.getResponse(this);
	}
}
