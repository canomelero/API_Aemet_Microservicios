package com.example.municipioorquestador.domain;

public class TipoRecursoInvalidoException extends RuntimeException {

    public TipoRecursoInvalidoException(String valor) {
        super("Tipo no válido: " + valor + ". Valores permitidos: geo, meteo, demo");
    }
}
