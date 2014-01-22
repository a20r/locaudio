package com.locaudio.api;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import android.content.Context;

import com.locaudio.interfaces.Mappable;
import com.locaudio.location.GPSTracker;
import com.locaudio.signal.WaveProcessing;
import com.musicg.wave.Wave;

public class NotifyForm implements Mappable<String, String> {

	private float x;
	private float y;
	private float soundPressureLevel;
	private float timestamp;
	private byte[] fingerprint;

	public NotifyForm() {

	}

	public NotifyForm(float x, float y, float soundPressureLevel,
			float timestamp, byte[] fingerprint) {
		this.x = x;
		this.y = y;
		this.soundPressureLevel = soundPressureLevel;
		this.timestamp = timestamp;
		this.fingerprint = fingerprint;
	}

	public Map<String, String> toMap() {
		Map<String, String> map = new HashMap<String, String>();
		map.put("x", "" + this.x);
		map.put("y", "" + this.y);
		map.put("spl", "" + this.soundPressureLevel);
		map.put("timestamp", "" + this.timestamp);
		map.put("fingerprint", Arrays.toString(this.fingerprint));
		return map;
	}

	public NotifyForm setX(float x) {
		this.x = x;
		return this;
	}

	public NotifyForm setY(float y) {
		this.y = y;
		return this;
	}

	public NotifyForm setSoundPressureLevel(float soundPressureLevel) {
		this.soundPressureLevel = soundPressureLevel;
		return this;
	}

	public NotifyForm setTimestamp(float timestamp) {
		this.timestamp = timestamp;
		return this;
	}

	public NotifyForm setFingerprint(byte[] fingerprint) {
		this.fingerprint = fingerprint;
		return this;
	}

	public static NotifyForm getDefaultNotifyForm(Wave wave, Context context) {

		GPSTracker gps = new GPSTracker(context);

		// check if GPS enabled
		if (gps.canGetLocation()) {

			NotifyForm postForm = new NotifyForm();

			double latitude = gps.getLatitude();
			double longitude = gps.getLongitude();

			postForm.setFingerprint(wave.getFingerprint());
			postForm.setSoundPressureLevel(WaveProcessing
					.determineAverageSoundPressureLevel(wave));
			postForm.setTimestamp(System.currentTimeMillis());
			postForm.setX((float) latitude);
			postForm.setY((float) longitude);
			return postForm;

		} else {
			gps.showSettingsAlert();
			return null;
		}
	}
}
