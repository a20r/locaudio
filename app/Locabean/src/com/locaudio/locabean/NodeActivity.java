package com.locaudio.locabean;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

import com.locaudio.functional.UIFunction;
import com.locaudio.api.AcquisitionThread;
import com.locaudio.api.Locaudio;
import com.locaudio.api.NotifyResponse;

public class NodeActivity extends Activity {

	private TextView nameTextView;
	private TextView confidenceTextView;

	private Locaudio locaudio;

	private static final String IP_ADDRESS = "138.251.207.84";
	private static final int PORT = 8000;

	private AcquisitionThread acquisitionThread;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_node);

		setupTextViews();
		setupLocaudio();
	}

	@Override
	public void onStop() {
		super.onStop();
		acquisitionThread.kill();
	}

	private void setupTextViews() {
		nameTextView = (TextView) findViewById(R.id.nameTextView);
		confidenceTextView = (TextView) findViewById(R.id.confidenceTextView);
	}

	private void setupLocaudio() {
		locaudio = new Locaudio(IP_ADDRESS, PORT);

		acquisitionThread = locaudio.getAcquisitionThread(
				getApplicationContext(), acquisitionCallback);

		acquisitionThread.start();
	}

	private UIFunction<NotifyResponse> acquisitionCallback = new UIFunction<NotifyResponse>(
			this) {

		@Override
		public Void body(NotifyResponse nr) {
			nameTextView.setText(nr.name);
			confidenceTextView.setText("" + nr.confidence);

			return null;
		}

	};
}
