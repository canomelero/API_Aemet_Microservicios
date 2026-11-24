package com.example.municipioorquestador.client;

public class UpstreamTimeoutException extends RuntimeException {

    public UpstreamTimeoutException(String servicio, Throwable causa) {
        super("Tiempo de espera agotado al consultar " + servicio, causa);
    }
}
