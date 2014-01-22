package com.locaudio.interfaces;

import java.util.Map;

public interface Mappable<T, R> {
	
	public Map<T, R> toMap();
	
}
