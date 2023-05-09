package it.smartcommunitylabdhub.core.models.converters.fields;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.cbor.CBORFactory;

import it.smartcommunitylabdhub.core.exception.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;

import java.io.IOException;
import java.util.Map;

import org.springframework.stereotype.Component;

@Component
public class CBORConverter implements Converter<Map<String, Object>, byte[]> {

    @Override
    public byte[] convert(Map<String, Object> map) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            return objectMapper.writeValueAsBytes(map);
        } catch (JsonProcessingException e) {
            throw new CustomException(null, e);
        }
    }

    @Override
    public Map<String, Object> convertReverse(byte[] cborBytes) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            return objectMapper.readValue(cborBytes, Map.class);
        } catch (IOException e) {
            throw new CustomException(null, e);
        }
    }
}
