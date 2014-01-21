package com.locaudio.functional;

public abstract class Function<T, R> {
	public abstract R body(T input);
	
	public R call(T input) {
		return body(input);
	}
}
