package com.example.municipioorquestador.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "servicios")
public record ServiciosProperties(Cliente geo, Cliente meteo, Cliente demo) {

    public record Cliente(String baseUrl) {
    }
}
