package com.locaudio.api;

import android.content.Context;

import com.locaudio.functional.Function;
import com.locaudio.functional.UIFunction;
import com.locaudio.net.*;

import com.musicg.wave.Wave;

public class Locaudio extends Requests {
	private static final String NAMES_ROUTE = "names";
	private static final String NOTIFY_ROUTE = "notify";
	private static final String LOCATIONS_ROUTE = "locations";

	public Locaudio(String ipAddress, int port) {
		super(ipAddress, port);
	}

	public AsyncGetRequest<SoundLocation[]> getSoundLocations(
			final String soundName,
			final Function<SoundLocation[], Void> callback) {

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

	public AsyncGetRequest<String[]> getNames(
			final Function<String[], Void> callback) {

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

	public AsyncPostRequest<NotifyResponse> notifyEvent(Context context,
			Wave wave, final Function<NotifyResponse, Void> callback) {

		AsyncPostRequest<NotifyResponse> apr = new AsyncPostRequest<NotifyResponse>(
				NotifyResponse.class, NOTIFY_ROUTE) {

			@Override
			public void runOnceReceivedResponse(NotifyResponse response) {

				callback.call(response);
			}

		};

		apr.setPostForm(NotifyForm.getDefaultNotifyForm(wave, context));
		apr.execute(this);

		return apr;

	}

	public AsyncPostRequest<NotifyResponse> notifyEvent(final NotifyForm event,
			final Function<NotifyResponse, Void> callback) {

		AsyncPostRequest<NotifyResponse> apr = new AsyncPostRequest<NotifyResponse>(
				NotifyResponse.class, event, NOTIFY_ROUTE) {

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
				NotifyResponse.class, event, NOTIFY_ROUTE) {

			@Override
			public void runOnceReceivedResponse(NotifyResponse response) {
			}

		};

		return apr.getResponse(this);
	}

	public AcquisitionThread getAcquisitionThread(Context context,
			UIFunction<NotifyResponse> callback) {
		return new AcquisitionThread(this, context, callback);

	}
}
