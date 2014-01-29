package com.locaudio.functional;

import java.util.ArrayList;
import java.util.List;

public abstract class Function<T, R> {

	public abstract R body(T input);

	public R call(T input) {
		return body(input);
	}

	public <A, B> List<B> map(
			Function<A, B> f, A[] inArray) {

		List<B> retList = new ArrayList<B>();
		for (A inVal : inArray) {
			retList.add(f.call(inVal));
		}

		return retList;
	}

	public <A, B> List<B> map(
			Function<A, B> f, List<A> inArray) {

		List<B> retList = new ArrayList<B>();
		for (A inVal : inArray) {
			retList.add(f.call(inVal));
		}

		return retList;
	}

}
