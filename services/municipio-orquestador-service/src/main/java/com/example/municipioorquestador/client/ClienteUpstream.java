package com.example.municipioorquestador.client;

import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestClientResponseException;

import java.net.SocketTimeoutException;
import java.net.http.HttpTimeoutException;

public abstract class ClienteUpstream {

    private final String nombre;
    private final RestClient restClient;

    protected ClienteUpstream(String nombre, String baseUrl, RestClient.Builder builder) {
        this.nombre = nombre;
        this.restClient = builder.baseUrl(baseUrl).build();
    }

    protected <T> T get(String ruta, Class<T> tipo) {
        try {
            T respuesta = restClient.get()
                    .uri(ruta)
                    .retrieve()
                    .body(tipo);
            if (respuesta == null) {
                throw new ServicioUpstreamException(nombre, "respuesta vacía");
            }
            return respuesta;
        } catch (RestClientResponseException exception) {
            throw new ServicioUpstreamException(
                    nombre,
                    exception.getStatusCode().value(),
                    exception
            );
        } catch (ResourceAccessException exception) {
            if (esTimeout(exception)) {
                throw new UpstreamTimeoutException(nombre, exception);
            }
            throw new ServicioUpstreamException(nombre, "error de conexión", exception);
        } catch (RestClientException exception) {
            throw new ServicioUpstreamException(nombre, "respuesta no válida", exception);
        }
    }

    private static boolean esTimeout(ResourceAccessException exception) {
        Throwable causa = exception.getCause();
        while (causa != null) {
            if (causa instanceof SocketTimeoutException
                    || causa instanceof HttpTimeoutException) {
                return true;
            }
            causa = causa.getCause();
        }
        return false;
    }
}
