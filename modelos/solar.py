# modelos/solar.py

import pvlib
import pandas as pd
import numpy as np
from pvlib import irradiance
from pvlib.location import Location


def simular_solar(
    latitud=19.483,
    longitud=-96.958,
    altitud=1200,
    zona_horaria="America/Mexico_City",
    nombre_ubicacion="Consolapa, Veracruz",
    fecha_inicio="2025-01-01",
    fecha_fin="2025-12-31",
    numero_paneles=100,
    area_panel_m2=2.583,
    potencia_panel_kw=0.6,
    eficiencia=0.22,
    perdidas=0.20,
    inclinacion=25,
    orientacion=180,
    kw_max=50,
    kw_min=20,
    mult_no_verano=0.8,
    mult_finde=0.5,
):
    ubicacion = Location(
        latitud,
        longitud,
        zona_horaria,
        altitud,
        nombre_ubicacion
    )

    tiempos = pd.date_range(
        start=fecha_inicio,
        end=fecha_fin,
        freq="15min",
        tz=zona_horaria
    )

    posicion_sol = ubicacion.get_solarposition(tiempos)

    zenit = posicion_sol["apparent_zenith"]
    azimut = posicion_sol["azimuth"]

    cielo_despejado = pvlib.clearsky.ineichen(
        zenit,
        airmass_absolute=1.5,
        linke_turbidity=3,
        altitude=altitud
    )

    ghi = cielo_despejado["ghi"]
    dni = cielo_despejado["dni"]
    dhi = cielo_despejado["dhi"]

    dni_extra = irradiance.get_extra_radiation(tiempos)

    irradiancia_total = irradiance.get_total_irradiance(
        surface_tilt=inclinacion,
        surface_azimuth=orientacion,
        dni=dni,
        ghi=ghi,
        dhi=dhi,
        dni_extra=dni_extra,
        solar_zenith=zenit,
        solar_azimuth=azimut
    )

    poa_global = irradiancia_total["poa_global"]
    poa_diffuse = irradiancia_total["poa_diffuse"]

    area_total = area_panel_m2 * numero_paneles
    potencia_maxima_sistema = potencia_panel_kw * numero_paneles

    potencia_panel = poa_global * area_total * eficiencia / 1000
    potencia_panel_difusa = poa_diffuse * area_total * eficiencia / 1000

    potencia_total = potencia_panel * (1 - perdidas)
    potencia_total = np.clip(potencia_total, 0, potencia_maxima_sistema)

    hora_float = tiempos.hour.values + tiempos.minute.values / 60.0

    horas_clave = [0, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 24]
    perfil_norm = [0, 0, 0.05, 0.4, 0.8, 0.95, 1.0, 0.9, 0.75, 0.75, 0.95, 1.0, 0.85, 0.4, 0.1, 0, 0]

    plantilla_base = np.interp(hora_float, horas_clave, perfil_norm)

    es_verano = tiempos.month.isin([5, 6, 7, 8, 9, 10])
    mult_verano = np.where(es_verano, 1.0, mult_no_verano)

    es_finde = tiempos.weekday >= 5
    mult_fin = np.where(es_finde, mult_finde, 1.0)

    plantilla_final = plantilla_base * mult_verano * mult_fin

    demanda = kw_min + (kw_max - kw_min) * plantilla_final
    demanda_restante = np.maximum(0, demanda - potencia_total)

    df = pd.DataFrame({
        "ghi": ghi,
        "dni": dni,
        "dhi": dhi,
        "poa_global": poa_global,
        "poa_diffuse": poa_diffuse,
        "potencia_solar_kw": potencia_total,
        "potencia_panel_kw": potencia_panel,
        "potencia_difusa_kw": potencia_panel_difusa,
        "demanda_kw": demanda,
        "demanda_restante_kw": demanda_restante,
    }, index=tiempos)

    energia_generada_anual = df["potencia_solar_kw"].sum() * 0.25
    energia_consumida_anual = df["demanda_kw"].sum() * 0.25
    energia_red_anual = df["demanda_restante_kw"].sum() * 0.25

    factor_planta_solar = energia_generada_anual / (potencia_maxima_sistema * 8760)
    factor_planta_demanda = energia_consumida_anual / (kw_max * 8760)

    return {
        "df": df,
        "energia_generada_anual": energia_generada_anual,
        "energia_consumida_anual": energia_consumida_anual,
        "energia_red_anual": energia_red_anual,
        "factor_planta_solar": factor_planta_solar,
        "factor_planta_demanda": factor_planta_demanda,
        "potencia_maxima_sistema": potencia_maxima_sistema,
    }