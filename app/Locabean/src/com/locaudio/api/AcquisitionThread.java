package com.locaudio.api;

import android.content.Context;
import android.os.Looper;

import com.locaudio.functional.UIFunction;
import com.locaudio.io.WaveWriter;
import com.musicg.wave.Wave;

public class AcquisitionThread extends Thread {

	private static final int RECORD_LENGTH = 5;

	private Locaudio locaudio;
	private UIFunction<NotifyResponse> postCallback;
	private Context context;
	private boolean shouldContinue;

	public AcquisitionThread(Locaudio locaudio, Context context,
			UIFunction<NotifyResponse> postCallback) {
		//super();
		this.locaudio = locaudio;
		this.context = context;
		this.postCallback = postCallback;
		this.shouldContinue = true;
	}

	public void kill() {
		this.shouldContinue = false;
	}
	
	@Override
	public void run() {
		Looper.prepare();
		while (this.shouldContinue) {

			Wave wave = WaveWriter.record(RECORD_LENGTH);

			locaudio.notifyEvent(this.context, wave, this.postCallback);

		}
	}

}
