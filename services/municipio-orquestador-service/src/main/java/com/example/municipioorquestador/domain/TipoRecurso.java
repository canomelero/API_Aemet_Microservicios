package com.example.municipioorquestador.domain;

public enum TipoRecurso {
    geo,
    meteo,
    demo;

    public static TipoRecurso desde(String valor) {
        for (TipoRecurso tipo : values()) {
            if (tipo.name().equals(valor)) {
                return tipo;
            }
        }
        throw new TipoRecursoInvalidoException(valor);
    }
}
