package com.example.municipioorquestador.client;

public class ServicioUpstreamException extends RuntimeException {

    private static final int BAD_GATEWAY = 502;

    private final int codigoEstado;

    public ServicioUpstreamException(String servicio, int codigoEstado, Throwable causa) {
        super("El servicio " + servicio + " ha respondido con el código " + codigoEstado, causa);
        this.codigoEstado = codigoEstado;
    }

    public ServicioUpstreamException(String servicio, String detalle) {
        this(servicio, detalle, null);
    }

    public ServicioUpstreamException(String servicio, String detalle, Throwable causa) {
        super("No se pudo consultar " + servicio + ": " + detalle, causa);
        this.codigoEstado = BAD_GATEWAY;
    }

    public int getCodigoEstado() {
        return codigoEstado;
    }
}
