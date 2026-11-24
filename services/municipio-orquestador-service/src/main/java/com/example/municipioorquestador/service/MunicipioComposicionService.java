package com.example.municipioorquestador.service;

import com.example.municipioorquestador.client.MunicipioDemoClient;
import com.example.municipioorquestador.client.MunicipioGeoClient;
import com.example.municipioorquestador.client.MunicipioMeteoClient;
import com.example.municipioorquestador.domain.MunicipioCombinado;
import com.example.municipioorquestador.domain.MunicipioDemo;
import com.example.municipioorquestador.domain.MunicipioGeo;
import com.example.municipioorquestador.domain.MunicipioInconsistenteException;
import com.example.municipioorquestador.domain.MunicipioMeteo;
import com.example.municipioorquestador.domain.TipoRecurso;
import org.springframework.stereotype.Service;

import java.util.EnumSet;
import java.util.LinkedHashSet;
import java.util.Set;

@Service
public class MunicipioComposicionService {

    private static final int MUNICIPIO_GRANADA = 18087;

    private final MunicipioGeoClient geoClient;
    private final MunicipioMeteoClient meteoClient;
    private final MunicipioDemoClient demoClient;

    public MunicipioComposicionService(
            MunicipioGeoClient geoClient,
            MunicipioMeteoClient meteoClient,
            MunicipioDemoClient demoClient
    ) {
        this.geoClient = geoClient;
        this.meteoClient = meteoClient;
        this.demoClient = demoClient;
    }

    public MunicipioCombinado componer(TipoRecurso tipo1, TipoRecurso tipo2) {
        Set<TipoRecurso> tipos = EnumSet.of(tipo1, tipo2);

        MunicipioGeo geo = tipos.contains(TipoRecurso.geo) ? geoClient.obtener() : null;
        MunicipioMeteo meteo = tipos.contains(TipoRecurso.meteo) ? meteoClient.obtener() : null;
        MunicipioDemo demo = tipos.contains(TipoRecurso.demo) ? demoClient.obtener() : null;

        return new MunicipioCombinado(validarMunicipio(geo, meteo, demo), geo, meteo, demo);
    }

    private static int validarMunicipio(MunicipioGeo geo, MunicipioMeteo meteo, MunicipioDemo demo) {
        Set<Integer> municipios = new LinkedHashSet<>();
        if (geo != null) {
            municipios.add(geo.municipioid());
        }
        if (meteo != null) {
            municipios.add(meteo.municipioid());
        }
        if (demo != null) {
            municipios.add(demo.municipioid());
        }

        if (municipios.isEmpty()) {
            throw new MunicipioInconsistenteException("No se ha recibido ningún municipio");
        }
        if (municipios.size() > 1 || !municipios.contains(MUNICIPIO_GRANADA)) {
            throw new MunicipioInconsistenteException(
                    "Los servicios han devuelto municipios distintos o no esperados: " + municipios
            );
        }
        return MUNICIPIO_GRANADA;
    }
}
