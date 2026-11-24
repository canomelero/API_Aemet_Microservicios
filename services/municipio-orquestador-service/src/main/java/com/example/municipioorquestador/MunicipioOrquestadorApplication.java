package com.example.municipioorquestador;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class MunicipioOrquestadorApplication {

    public static void main(String[] args) {
        SpringApplication.run(MunicipioOrquestadorApplication.class, args);
    }
}
