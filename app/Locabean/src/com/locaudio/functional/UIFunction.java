package com.locaudio.functional;

import android.app.Activity;

public abstract class UIFunction<T> extends Function<T, Void> {

	private Activity activity;

	public UIFunction(Activity activity) {
		this.activity = activity;
	}

	public abstract Void body(T input);

	public Void call(final T input) {
		this.activity.runOnUiThread(new Runnable() {
			@Override
			public void run() {
				body(input);
			}
		});
		
		return null;
	}

}
