package com.example.municipioorquestador.client;

import com.example.municipioorquestador.config.ServiciosProperties;
import com.example.municipioorquestador.domain.MunicipioMeteo;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MunicipioMeteoClient extends ClienteUpstream {

    public MunicipioMeteoClient(RestClient.Builder builder, ServiciosProperties properties) {
        super("municipio-meteo-service", properties.meteo().baseUrl(), builder);
    }

    public MunicipioMeteo obtener() {
        return get("/granada/meteo", MunicipioMeteo.class);
    }
}
