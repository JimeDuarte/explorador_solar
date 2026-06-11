def calcular_finanzas(
    energia_generada_anual,
    consumo_anual_kwh,
    precio_kwh=2.68,
    costo_sistema=915000,
    mantenimiento_pct=0.015,
    vida_util=20,
):

    costo_actual = consumo_anual_kwh * precio_kwh

    energia_aprovechada = min(
        energia_generada_anual,
        consumo_anual_kwh
    )

    ahorro_anual = energia_aprovechada * precio_kwh

    mantenimiento_anual = costo_sistema * mantenimiento_pct

    beneficio_neto = ahorro_anual - mantenimiento_anual

    payback = costo_sistema / beneficio_neto

    roi = beneficio_neto / costo_sistema * 100

    return {
        "costo_actual": costo_actual,
        "ahorro_anual": ahorro_anual,
        "mantenimiento_anual": mantenimiento_anual,
        "beneficio_neto": beneficio_neto,
        "payback": payback,
        "roi": roi,
    }