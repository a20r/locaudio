package com.locaudio.functional;

import android.app.Activity;

public abstract class UIFunction<T> extends Function<T> {

	private Activity activity;

	public UIFunction(Activity activity) {
		this.activity = activity;
	}

	public abstract void runUI(T input);

	public void run(final T input) {
		this.activity.runOnUiThread(new Runnable() {
			@Override
			public void run() {
				runUI(input);
			}
		});
	}

}
