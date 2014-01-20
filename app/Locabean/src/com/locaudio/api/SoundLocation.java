package com.locaudio.api;

import com.google.gson.annotations.SerializedName;

public class SoundLocation {
	@SerializedName("position")
	public Point position;

	@SerializedName("confidence")
	public float confidence;

	@Override
	public String toString() {
		return "{ Position: " + this.position.toString() + ", Confidence: "
				+ this.confidence + " }";
	}

	@Override
	public boolean equals(Object obj) {
		SoundLocation sl = (SoundLocation) obj;
		if (sl.position.equals(this.position)
				&& sl.confidence == this.confidence) {
			return true;
		} else {
			return false;
		}
	}
}
