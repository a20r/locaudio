package com.locaudio.locabean;

// import java.util.Arrays;

import android.app.Activity;
import android.media.AudioRecord;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.musicg.wave.Wave;

import com.locaudio.functional.UIFunction;
import com.locaudio.io.WaveWriter;
import com.locaudio.signal.WaveProcessing;
import com.locaudio.api.Locaudio;
import com.locaudio.api.NotifyForm;
import com.locaudio.api.NotifyResponse;

public class NodeActivity extends Activity {

	private AudioRecord recorder = null;
	private Thread recordingThread = null;
	private boolean isRecording = false;

	private TextView nameTextView = null;
	private TextView confidenceTextView = null;
	private TextView splTextView = null;

	private Locaudio locaudio = null;

	// temporary fix
	private Activity self = this;

	private static final String IP_ADDRESS = "192.168.1.9";
	private static final int PORT = 8000;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_node);

		setButtonHandlers();
		enableButtons(false);

		nameTextView = (TextView) findViewById(R.id.nameTextView);
		confidenceTextView = (TextView) findViewById(R.id.confidenceTextView);
		splTextView = (TextView) findViewById(R.id.splTextView);

		locaudio = new Locaudio(IP_ADDRESS, PORT);
	}

	private void setButtonHandlers() {
		((Button) findViewById(R.id.btnStart)).setOnClickListener(btnClick);
		((Button) findViewById(R.id.btnStop)).setOnClickListener(btnClick);
		((Button) findViewById(R.id.btnSend)).setOnClickListener(btnClick);
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

		recordingThread = WaveWriter.getRecorderThread(recorder, isRecording);

		recordingThread.start();
	}

	private void stopRecording() {
		if (null != recorder) {
			isRecording = false;

			int i = recorder.getState();
			if (i == WaveWriter.AUDIO_RECORDER_ON_STATE) {
				recorder.stop();
			}

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
				splTextView.setText(""
						+ WaveProcessing
								.determineAverageSoundPressureLevel(wave));

				break;
			}
			case R.id.btnSend: {

				Wave wave = new Wave(WaveWriter.getFilename());
				NotifyForm postForm = new NotifyForm();
				postForm.setFingerprint(wave.getFingerprint());
				postForm.setSoundPressureLevel(100);
				postForm.setTimestamp(10);
				postForm.setX(1);
				postForm.setY(0);

				locaudio.notifyEvent(postForm, new UIFunction<NotifyResponse>(
						self) {

					@Override
					public void runUI(NotifyResponse nr) {
						nameTextView.setText(nr.name);
						confidenceTextView.setText("" + nr.confidence);
					}
				});

				break;
			}
			}
		}
	};
}
