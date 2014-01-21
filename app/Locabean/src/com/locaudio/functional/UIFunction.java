package com.locaudio.functional;

import android.app.Activity;

public abstract class UIFunction<T> extends Function<T> {

	private Activity activity;

	public UIFunction(Activity activity) {
		this.activity = activity;
	}

	public abstract void body(T input);

	public void call(final T input) {
		this.activity.runOnUiThread(new Runnable() {
			@Override
			public void run() {
				body(input);
			}
		});
	}

}
