package com.example.municipioorquestador.client;

import com.example.municipioorquestador.config.ServiciosProperties;
import com.example.municipioorquestador.domain.MunicipioDemo;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MunicipioDemoClient extends ClienteUpstream {

    public MunicipioDemoClient(RestClient.Builder builder, ServiciosProperties properties) {
        super("municipio-demo-service", properties.demo().baseUrl(), builder);
    }

    public MunicipioDemo obtener() {
        return get("/granada/demo", MunicipioDemo.class);
    }
}
