package com.example.municipioorquestador.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = false)
public record MunicipioGeo(
        @JsonProperty(required = true) int municipioid,
        @JsonProperty(required = true) double latitud,
        @JsonProperty(required = true) double longitud,
        @JsonProperty(required = true) double altitud
) {
}
