package com.example.municipioorquestador.client;

import com.example.municipioorquestador.config.ServiciosProperties;
import com.example.municipioorquestador.domain.MunicipioGeo;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MunicipioGeoClient extends ClienteUpstream {

    public MunicipioGeoClient(RestClient.Builder builder, ServiciosProperties properties) {
        super("municipio-geo-service", properties.geo().baseUrl(), builder);
    }

    public MunicipioGeo obtener() {
        return get("/granada/geo", MunicipioGeo.class);
    }
}
