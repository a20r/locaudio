package com.locaudio.functional;

import android.app.Activity;

public abstract class UIFunction<T, R> extends Function<T, R> {

	private Activity activity;

	public UIFunction(Activity activity) {
		this.activity = activity;
	}

	public abstract R body(T input);

	public R call(final T input) {
		this.activity.runOnUiThread(new Runnable() {
			@Override
			public void run() {
				body(input);
			}
		});
		
		return null;
	}

}
