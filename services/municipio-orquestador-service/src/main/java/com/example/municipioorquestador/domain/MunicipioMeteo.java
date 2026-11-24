package com.example.municipioorquestador.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = false)
public record MunicipioMeteo(
        @JsonProperty(required = true) int municipioid,
        @JsonProperty(required = true) String temperatura_actual,
        @JsonProperty(required = true) Temperaturas temperaturas,
        @JsonProperty(required = true) String humedad,
        @JsonProperty(required = true) String viento,
        @JsonProperty(required = true) String precipitacion,
        @JsonProperty(required = true) String estadocielo
) {
}
