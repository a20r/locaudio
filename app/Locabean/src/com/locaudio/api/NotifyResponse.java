package com.locaudio.api;

import com.google.gson.annotations.SerializedName;

public class NotifyResponse {
	@SerializedName("error")
	public int error;

	@SerializedName("message")
	public String message;

	@SerializedName("name")
	public String name;

	@SerializedName("confidence")
	public float confidence;

	@Override
	public String toString() {
		return "{ Error: " + this.error + ", Message: " + this.message
				+ ", Name: " + this.name + ", Confidence: " + this.confidence + " }";
	}
}
