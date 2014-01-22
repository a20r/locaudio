package com.locaudio.locabean;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.musicg.wave.Wave;

import com.locaudio.functional.UIFunction;
import com.locaudio.io.WaveWriter;
import com.locaudio.signal.WaveProcessing;
import com.locaudio.api.Locaudio;
import com.locaudio.api.NotifyResponse;

public class NodeActivity extends Activity {

	private TextView nameTextView = null;
	private TextView confidenceTextView = null;
	private TextView splTextView = null;

	private Locaudio locaudio = null;

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
		((Button) findViewById(R.id.btnStart))
				.setOnClickListener(btnStartClick);
		((Button) findViewById(R.id.btnStop)).setOnClickListener(btnStopClick);
		((Button) findViewById(R.id.btnSend)).setOnClickListener(btnSendClick);
	}

	private void enableButton(int id, boolean isEnable) {
		((Button) findViewById(id)).setEnabled(isEnable);
	}

	private void enableButtons(boolean isRecording) {
		enableButton(R.id.btnStart, !isRecording);
		enableButton(R.id.btnStop, isRecording);
	}

	private View.OnClickListener btnStartClick = new View.OnClickListener() {
		@Override
		public void onClick(View v) {
			System.out.println("Start Recording");
			enableButtons(true);

			WaveWriter.startRecording();
		}
	};

	private View.OnClickListener btnStopClick = new View.OnClickListener() {
		@Override
		public void onClick(View v) {
			System.out.println("Stop Recording");
			enableButtons(false);
			WaveWriter.stopRecording();

			Wave wave = WaveWriter.getWave();
			splTextView.setText(""
					+ WaveProcessing.determineAverageSoundPressureLevel(wave));
		}
	};

	private View.OnClickListener btnSendClick = new View.OnClickListener() {
		@Override
		public void onClick(View v) {

			locaudio.notifyEvent(getApplicationContext(),
					new UIFunction<NotifyResponse>(NodeActivity.this) {

						@Override
						public Void body(NotifyResponse nr) {
							nameTextView.setText(nr.name);
							confidenceTextView.setText("" + nr.confidence);

							return null;
						}

					});
		}
	};
}
