package com.example.municipioorquestador.domain;

public class MunicipioInconsistenteException extends RuntimeException {

    public MunicipioInconsistenteException(String mensaje) {
        super(mensaje);
    }
}
