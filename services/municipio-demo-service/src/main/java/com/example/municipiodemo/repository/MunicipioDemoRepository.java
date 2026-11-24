package com.example.municipiodemo.repository;

import com.example.municipiodemo.domain.MunicipioDemo;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;

@Repository
public class MunicipioDemoRepository {

    private static final String DATA_RESOURCE_DESCRIPTION = "datos locales de Granada";

    private final MunicipioDemo municipio;

    public MunicipioDemoRepository(
            ObjectMapper objectMapper,
            @Value("classpath:data/municipio_demo_18087.json") Resource dataResource
    ) {
        this.municipio = load(objectMapper, dataResource);
    }

    public MunicipioDemo find() {
        return municipio;
    }

    private static MunicipioDemo load(ObjectMapper objectMapper, Resource dataResource) {
        try (InputStream dataStream = dataResource.getInputStream()) {
            return objectMapper.readValue(dataStream, MunicipioDemo.class);
        } catch (IOException exception) {
            throw new UncheckedIOException(
                    "No se pudieron leer los " + DATA_RESOURCE_DESCRIPTION,
                    exception
            );
        }
    }
}
