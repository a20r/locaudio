package com.locaudio.signal;

import com.musicg.wave.Wave;

public class WaveProcessing {

	public static float amplitudeToSoundPressureLevel(float amplitude) {
		return (float) (20 * Math.log(amplitude) / Math.log(10));
	}

	public static float determineAverageAmplitude(Wave wave) {

		return 0;
	}

	public static float determineAverageSoundPressureLevel(Wave wave) {
		return amplitudeToSoundPressureLevel(determineAverageAmplitude(wave));
	}

}
