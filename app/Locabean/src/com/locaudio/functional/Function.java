package com.locaudio.functional;

public abstract class Function<T> {
	public abstract void run(T input);

	@SuppressWarnings("rawtypes")
	public static Function getEmptyFunction() {
		return new Function() {

			@Override
			public void run(Object input) {
			}

		};
	}
}
