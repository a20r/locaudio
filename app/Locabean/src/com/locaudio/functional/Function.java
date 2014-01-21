package com.locaudio.functional;

import java.util.ArrayList;
import java.util.List;

public abstract class Function<T, R> {

	public abstract R body(T input);

	public R call(T input) {
		return body(input);
	}

	public <IN_TYPE, OUT_TYPE> List<OUT_TYPE> map(
			Function<IN_TYPE, OUT_TYPE> f, IN_TYPE[] inArray) {

		List<OUT_TYPE> retList = new ArrayList<OUT_TYPE>();
		for (IN_TYPE inVal : inArray) {
			retList.add(f.call(inVal));
		}

		return retList;
	}

	public <IN_TYPE, OUT_TYPE> List<OUT_TYPE> map(
			Function<IN_TYPE, OUT_TYPE> f, List<IN_TYPE> inArray) {

		List<OUT_TYPE> retList = new ArrayList<OUT_TYPE>();
		for (IN_TYPE inVal : inArray) {
			retList.add(f.call(inVal));
		}

		return retList;
	}

}
