package com.example.municipiodemo.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = false)
public record MunicipioDemo(
        @JsonProperty(required = true) int municipioid,
        @JsonProperty(required = true) String alcalde,
        @JsonProperty(required = true) String partidopolitico,
        @JsonProperty(required = true) int numhabitantes
) {
}
