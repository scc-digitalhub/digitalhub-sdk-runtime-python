package it.smartcommunitylabdhub.core.utils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.BiFunction;
import java.util.stream.Stream;

public class MapUtils {

	private MapUtils() {
	}

	public static Optional<Map<String, Object>> getNestedFieldValue(Map<String, Object> map, String field) {
		Object value = ((Map<?, ?>) map).get(field);

		if (value instanceof Map) {
			@SuppressWarnings("unchecked")
			Map<String, Object> nestedMap = (Map<String, Object>) value;
			return Optional.of(nestedMap);
		} else {
			return Optional.empty();
		}
	}

	@SuppressWarnings("unchecked")
	public static <T> void computeAndAddElement(Map<String, Object> map, String key, T element) {
		((ArrayList<T>) map.computeIfAbsent(key, k -> new ArrayList<>())).add(element);
	}

	@SuppressWarnings("unchecked")
	public static <K, V> Map<K, V> mergeMaps(Map<K, V> map1, Map<K, V> map2, BiFunction<V, V, V> mergeFunction) {
		Map<K, V> mergedMap = new HashMap<>(map1);

		map2.forEach((key, value) -> mergedMap.merge(key, value, (oldValue, newValue) -> {
			if (oldValue instanceof Map && newValue instanceof Map) {
				// If both values are maps, recursively merge them
				return (V) mergeMaps((Map<K, V>) oldValue, (Map<K, V>) newValue, mergeFunction);
			} else if (oldValue instanceof List && newValue instanceof List) {
				// If both values are lists, concatenate them
				List<V> mergedList = new ArrayList<>((List<V>) oldValue);
				mergedList.addAll((List<V>) newValue);
				return (V) mergedList;
			} else {
				// For other types, use the new value
				return newValue;
			}
		}));

		return mergedMap;
	}
}
