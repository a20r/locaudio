package com.locaudio.functional;

public abstract class Function<T> {
	public abstract void body(T input);
	
	public void call(T input) {
		body(input);
	}
	@SuppressWarnings("rawtypes")
	public static Function getEmptyFunction() {
		return new Function() {

			@Override
			public void body(Object input) {
			}

		};
	}
}
