import random
import json
import datetime
import os

# Configuración
OUTPUT_FILE = "data/synthetic_claims.jsonl"
NUM_SAMPLES = 100

# Datos para generación
nombres = [
    "Juan", "Maria", "Pedro", "Ana", "Luis", "Sofia", "Carlos", "Lucia", 
    "Diego", "Valentina", "Miguel", "Camila", "Javier", "Paula", "Fernando", "Martina"
]
marcas = [
    "Toyota Corolla", "Ford Fiesta", "Honda Civic", "Chevrolet Onix", "Fiat Cronos", "VW Gol", "Peugeot 208",
    "Renault Sandero", "Toyota Hilux", "Ford Ranger", "Nissan Versa", "Jeep Renegade", "Chevrolet Cruze"
]
colores = ["rojo", "azul", "blanco", "negro", "gris", "plateado", "verde", "bordo", "dorado", "azul oscuro"]
calles = [
    "Av. Libertador", "Calle 9 de Julio", "Ruta 2", "Av. Corrientes", "Calle San Martín",
    "Av. Cabildo", "Av. Santa Fe", "Autopista Panamericana", "Av. General Paz", "Calle Florida"
]
acciones = [
    "me chocó de atrás", "me rayó el costado", "se cruzó en rojo", "frenó de golpe", "me rompió el espejo",
    "me encerró", "no respetó la prioridad", "dio marcha atrás sin mirar", "abrió la puerta sin mirar", "cambió de carril bruscamente"
]
consecuencias = [
    "tengo el paragolpes roto", "la puerta no abre", "solo fue un susto", "el faro está destruido", "necesito grúa",
    "el baúl no cierra", "tengo un bollo en la puerta", "se rompió la óptica", "el radiador pierde agua", "tengo el espejo colgando"
]

def generar_fecha_reciente():
    dias_atras = random.randint(0, 30)
    fecha = datetime.date.today() - datetime.timedelta(days=dias_atras)
    return fecha.strftime("%Y-%m-%d")

def introducir_ruido(texto):
    # Simula errores de tipeo o redacción informal
    if random.random() < 0.3:
        texto = texto.lower() # Todo minúsculas
    if random.random() < 0.2:
        texto = texto.replace(".", "") # Sin puntos
    if random.random() < 0.1:
        texto = texto.replace(" de ", " d ") # Abreviaciones chat
    return texto

def generar_reclamo():
    nombre = random.choice(nombres)
    mi_auto = random.choice(marcas)
    otro_auto = random.choice(marcas)
    calle = random.choice(calles)
    accion = random.choice(acciones)
    consecuencia = random.choice(consecuencias)
    fecha = generar_fecha_reciente()
    
    # Plantillas de redacción (variedad de estilos)
    plantillas = [
        # Estilo conversacional
        f"Hola, soy {nombre}. El {fecha} iba por {calle} con mi {mi_auto} y un {otro_auto} {accion}. {consecuencia}.",
        f"Buenas, necesito hacer un reclamo. Ayer en {calle} un {otro_auto} {accion}. Yo iba en mi {mi_auto}. {consecuencia}.",
        f"Hola buenas tardes, el {fecha} tuve un accidente. Iba por {calle} y un {otro_auto} {accion}. Mi auto es un {mi_auto}.",
        
        # Estilo formal/estructurado
        f"Siniestro ocurrido el {fecha}. Lugar: {calle}. Vehículo asegurado: {mi_auto}. Tercero: {otro_auto}. Descripción: {accion}.",
        f"Fecha del siniestro: {fecha}. Ubicación: {calle}. Mi vehículo: {mi_auto}. Vehículo tercero: {otro_auto}. {accion}. Daños: {consecuencia}.",
        f"Denuncio siniestro del día {fecha} en {calle}. Conducía mi {mi_auto} cuando un {otro_auto} {accion}.",
        
        # Estilo breve/telegráfico
        f"Tuve un accidente en {calle} ayer. Un {otro_auto} {accion} a mi {mi_auto}. {consecuencia}.",
        f"{fecha}: Choque en {calle}. {mi_auto} vs {otro_auto}. {accion}.",
        f"Accidente {fecha}, {calle}. {otro_auto} {accion}. Mi auto: {mi_auto}. {consecuencia}.",
        
        # Estilo informal/coloquial argentino
        f"Che, {fecha} me chocaron en {calle}. Iba en mi {mi_auto} y un {otro_auto} {accion}. {consecuencia}.",
        f"Hola, mira, ayer estaba por {calle} con el {mi_auto} y un loco en un {otro_auto} {accion}. {consecuencia}.",
        f"Buen día, te cuento que el {fecha} un {otro_auto} {accion} cuando yo iba tranquilo en mi {mi_auto} por {calle}.",
        
        # Estilo queja/frustración
        f"No puedo creer lo que me pasó el {fecha}. Estaba en {calle} con mi {mi_auto} y un {otro_auto} {accion}. Ahora {consecuencia}.",
        f"Vengo a denunciar porque el {fecha} un irresponsable en un {otro_auto} {accion} en {calle}. Tengo un {mi_auto} y {consecuencia}.",
        
        # Estilo descriptivo/detallado
        f"El día {fecha} aproximadamente, circulaba por {calle} conduciendo mi {mi_auto} cuando un vehículo {otro_auto} {accion}. Como resultado, {consecuencia}.",
        f"Me presento para informar un siniestro ocurrido el {fecha}. Mientras transitaba por {calle} en mi {mi_auto}, un {otro_auto} {accion}. Consecuencia: {consecuencia}.",
        
        # Estilo WhatsApp/mensaje rápido
        f"hola {fecha} choque en {calle} un {otro_auto} {accion} yo tengo {mi_auto} {consecuencia}",
        f"buenas me chocaron ayer en {calle} tengo un {mi_auto} y un {otro_auto} {accion}",
        f"necesito ayuda me chocaron!! {fecha} en {calle}, era un {otro_auto}, mi auto es {mi_auto}, {consecuencia}"
    ]
    
    texto_base = random.choice(plantillas)
    texto_final = introducir_ruido(texto_base)
    
    return {
        "text": texto_final,
        "metadata": {
            "fecha": fecha,
            "lugar": calle,
            "vehiculo_asegurado": mi_auto,
            "vehiculo_tercero": otro_auto,
            "tipo_incidente": accion
        }
    }

def main():
    print(f"Generando {NUM_SAMPLES} reclamos sintéticos con Fuzzing...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for _ in range(NUM_SAMPLES):
            reclamo = generar_reclamo()
            f.write(json.dumps(reclamo, ensure_ascii=False) + "\n")
    print(f"Datos guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
