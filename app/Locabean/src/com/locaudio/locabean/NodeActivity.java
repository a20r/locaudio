package com.locaudio.locabean;

import java.io.IOException;
import java.util.Arrays;

import org.apache.http.client.ClientProtocolException;

import android.app.Activity;
import android.media.AudioRecord;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.musicg.wave.Wave;

import com.locaudio.io.WaveWriter;
import com.locaudio.api.Locaudio;
import com.locaudio.api.NotifyForm;
import com.locaudio.api.NotifyResponse;
import com.locaudio.api.SoundLocation;

public class NodeActivity extends Activity {

	private AudioRecord recorder = null;
	private Thread recordingThread = null;
	private boolean isRecording = false;
	private TextView fingerprintTextView = null;
	private Locaudio locaudio = null;

	private static final String IP_ADDRESS = "192.168.1.9";
	private static final int PORT = 8000;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_node);

		setButtonHandlers();
		enableButtons(false);
		fingerprintTextView = (TextView) findViewById(R.id.fingerprintText);
		fingerprintTextView.setMovementMethod(new ScrollingMovementMethod());

		locaudio = new Locaudio(IP_ADDRESS, PORT);
	}

	private void setButtonHandlers() {
		((Button) findViewById(R.id.btnStart)).setOnClickListener(btnClick);
		((Button) findViewById(R.id.btnStop)).setOnClickListener(btnClick);
	}

	private void enableButton(int id, boolean isEnable) {
		((Button) findViewById(id)).setEnabled(isEnable);
	}

	private void enableButtons(boolean isRecording) {
		enableButton(R.id.btnStart, !isRecording);
		enableButton(R.id.btnStop, isRecording);
	}

	private void startRecording() {
		recorder = WaveWriter.getAudioRecord();

		int i = recorder.getState();
		if (i == 1)
			recorder.startRecording();

		isRecording = true;

		recordingThread = new Thread(new Runnable() {

			@Override
			public void run() {
				WaveWriter.writeAudioDataToFile(recorder, isRecording);
			}
		}, "AudioRecorder Thread");

		recordingThread.start();
	}

	private void stopRecording() {
		if (null != recorder) {
			isRecording = false;

			int i = recorder.getState();
			if (i == 1)
				recorder.stop();
			recorder.release();

			recorder = null;
			recordingThread = null;
		}

		WaveWriter.copyWaveFile(WaveWriter.getTempFilename(),
				WaveWriter.getFilename());

		WaveWriter.deleteTempFile();
	}

	private View.OnClickListener btnClick = new View.OnClickListener() {
		@Override
		public void onClick(View v) {
			switch (v.getId()) {
			case R.id.btnStart: {
				System.out.println("Start Recording");
				enableButtons(true);

				startRecording();

				break;
			}
			case R.id.btnStop: {
				System.out.println("Stop Recording");
				enableButtons(false);
				stopRecording();

				Wave wave = new Wave(WaveWriter.getFilename());
				fingerprintTextView.setText(Arrays.toString(wave
						.getFingerprint()));

				SoundLocation[] soundLocations = locaudio
						.getSoundLocations("Cock");
				System.out.println(Arrays.toString(soundLocations));
				
				NotifyForm postForm = new NotifyForm();
				postForm.setFingerprint(wave.getFingerprint());
				postForm.setSoundPressureLevel(100);
				postForm.setTimestamp(10);
				postForm.setX(1);
				postForm.setY(0);
				
				try {
					NotifyResponse nr = locaudio.notifyEvent(postForm);
					System.out.println(nr.name);
				} catch (ClientProtocolException e) {
					e.printStackTrace();
				} catch (IOException e) {
					e.printStackTrace();
				}
				
				break;
			}
			}
		}
	};
}
