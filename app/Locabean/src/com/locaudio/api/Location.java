package com.locaudio.api;

import com.google.gson.annotations.SerializedName;

public class Location {
	@SerializedName("position")
	public Point position;
	
	@SerializedName("confidence")
	public float confidence;
}
