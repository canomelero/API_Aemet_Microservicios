package com.example.municipioorquestador.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = false)
public record Temperaturas(
        @JsonProperty(required = true) String max,
        @JsonProperty(required = true) String min
) {
}
