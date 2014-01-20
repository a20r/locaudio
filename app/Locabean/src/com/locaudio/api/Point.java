package com.locaudio.api;

import com.google.gson.annotations.SerializedName;

public class Point {

	@SerializedName("x")
	public float x;

	@SerializedName("y")
	public float y;

	@Override
	public String toString() {
		return "( X: " + this.x + ", Y: " + this.y + " )";
	}

	@Override
	public boolean equals(Object obj) {
		Point p = (Point) obj;
		if (p.x == this.x && p.y == this.y) {
			return true;
		} else {
			return false;
		}
	}
}
