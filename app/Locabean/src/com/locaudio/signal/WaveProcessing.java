package com.locaudio.signal;

import com.musicg.wave.Wave;

public class WaveProcessing {

	public static float amplitudeToSoundPressureLevel(float amplitude) {
		return (float) (20 * Math.log(amplitude) / Math.log(10));
	}

	public static boolean isPeak(int prevVal, int curVal, int nextVal) {
		if (prevVal <= curVal && nextVal <= curVal) {
			return true;
		} else {
			return false;
		}
	}

	public static float determineAverageAmplitude(Wave wave) {

		short threshold = 300;
		int runningSum = 0;
		int count = 0;

		short[] amplitudes = wave.getSampleAmplitudes();

		for (int i = 1; i < amplitudes.length - 1; i++) {
			if (isPeak(amplitudes[i - 1], amplitudes[i], amplitudes[i + 1])) {
				if (amplitudes[i] > threshold) {
					runningSum += amplitudes[i];
					count++;
				}
			}
		}
		
		return (float) runningSum / (float) count;
	}

	public static float determineAverageSoundPressureLevel(Wave wave) {
		return amplitudeToSoundPressureLevel(determineAverageAmplitude(wave));
	}

}
