package com.example.municipioorquestador.api;

import com.example.municipioorquestador.client.ServicioUpstreamException;
import com.example.municipioorquestador.client.UpstreamTimeoutException;
import com.example.municipioorquestador.domain.MunicipioInconsistenteException;
import com.example.municipioorquestador.domain.TipoRecursoInvalidoException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(TipoRecursoInvalidoException.class)
    public ResponseEntity<ErrorResponse> tipoInvalido(TipoRecursoInvalidoException exception) {
        return ResponseEntity.badRequest().body(new ErrorResponse(exception.getMessage()));
    }

    @ExceptionHandler(UpstreamTimeoutException.class)
    public ResponseEntity<ErrorResponse> tiempoAgotado(UpstreamTimeoutException exception) {
        return ResponseEntity.status(HttpStatus.GATEWAY_TIMEOUT)
                .body(new ErrorResponse(exception.getMessage()));
    }

    @ExceptionHandler(ServicioUpstreamException.class)
    public ResponseEntity<ErrorResponse> errorUpstream(ServicioUpstreamException exception) {
        return ResponseEntity.status(exception.getCodigoEstado())
                .body(new ErrorResponse(exception.getMessage()));
    }

    @ExceptionHandler(MunicipioInconsistenteException.class)
    public ResponseEntity<ErrorResponse> municipioInconsistente(MunicipioInconsistenteException exception) {
        return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                .body(new ErrorResponse(exception.getMessage()));
    }
}
