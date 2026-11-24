package com.example.municipioorquestador.api;

import com.example.municipioorquestador.domain.MunicipioCombinado;
import com.example.municipioorquestador.domain.TipoRecurso;
import com.example.municipioorquestador.service.MunicipioComposicionService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/granada")
public class MunicipioOrquestadorController {

    private final MunicipioComposicionService service;

    public MunicipioOrquestadorController(MunicipioComposicionService service) {
        this.service = service;
    }

    @GetMapping(path = "/{tipo1}/{tipo2}", produces = MediaType.APPLICATION_JSON_VALUE)
    public MunicipioCombinado getCombinado(
            @PathVariable String tipo1,
            @PathVariable String tipo2
    ) {
        return service.componer(TipoRecurso.desde(tipo1), TipoRecurso.desde(tipo2));
    }
}
