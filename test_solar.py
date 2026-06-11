from modelos.solar import simular_solar
from modelos.financiero import calcular_finanzas

solar = simular_solar()

finanzas = calcular_finanzas(
    energia_generada_anual=solar["energia_generada_anual"],
    consumo_anual_kwh=solar["energia_consumida_anual"],
    precio_kwh=2.68,
    costo_sistema=915000
)

print("------ SOLAR ------")
print("Generación anual:", round(solar["energia_generada_anual"], 2), "kWh")
print("Consumo anual:", round(solar["energia_consumida_anual"], 2), "kWh")
print("Energía tomada de red:", round(solar["energia_red_anual"], 2), "kWh")

print("\n------ FINANZAS ------")
print("Costo anual actual: $", round(finanzas["costo_actual"], 2))
print("Ahorro anual: $", round(finanzas["ahorro_anual"], 2))
print("Mantenimiento anual: $", round(finanzas["mantenimiento_anual"], 2))
print("Beneficio neto anual: $", round(finanzas["beneficio_neto"], 2))
print("Payback:", round(finanzas["payback"], 2), "años")
print("ROI:", round(finanzas["roi"], 2), "%")