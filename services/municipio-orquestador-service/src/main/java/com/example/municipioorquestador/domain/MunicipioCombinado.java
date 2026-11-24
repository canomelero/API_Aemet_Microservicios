package com.example.municipioorquestador.domain;

import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record MunicipioCombinado(
        int municipioid,
        MunicipioGeo geo,
        MunicipioMeteo meteo,
        MunicipioDemo demo
) {
}
