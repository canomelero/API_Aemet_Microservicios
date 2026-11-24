package com.example.municipiodemo.api;

import com.example.municipiodemo.domain.MunicipioDemo;
import com.example.municipiodemo.repository.MunicipioDemoRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MunicipioDemoController {

    private final MunicipioDemoRepository repository;

    public MunicipioDemoController(MunicipioDemoRepository repository) {
        this.repository = repository;
    }

    @GetMapping(path = "/granada/demo", produces = MediaType.APPLICATION_JSON_VALUE)
    public MunicipioDemo getGranadaDemo() {
        return repository.find();
    }
}
