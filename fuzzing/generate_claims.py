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

# Acciones en dónde el tercero tiene la culpa
acciones_tercero = [
    "me chocó de atrás", "me rayó el costado", "se cruzó en rojo", "frenó de golpe", "me rompió el espejo",
    "me encerró", "no respetó la prioridad", "dio marcha atrás sin mirar", "abrió la puerta sin mirar", "cambió de carril bruscamente"
]

# Acciones en dónde el asegurado tiene la culpa
acciones_asegurado = [
    "le choqué de atrás", "le rayé el costado", "me pasé un semáforo en rojo", "frené de golpe y me chocaron",
    "le pegué al espejo", "lo encerré sin querer", "no respeté la prioridad", "di marcha atrás sin mirar",
    "abrí la puerta sin mirar", "cambié de carril y lo toqué", "me distraje con el celular", 
    "calculé mal la distancia", "no vi que estaba estacionado", "me confundí de carril"
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
        texto = texto.lower()
    if random.random() < 0.2:
        texto = texto.replace(".", "")
    if random.random() < 0.1:
        texto = texto.replace(" de ", " d ")
    return texto

def generar_reclamo():
    nombre = random.choice(nombres)
    mi_auto = random.choice(marcas)
    otro_auto = random.choice(marcas)
    calle = random.choice(calles)
    consecuencia = random.choice(consecuencias)
    fecha = generar_fecha_reciente()
    
    # Aleatoriamente decidir responsabilidad (~30% asegurado con culpa, ~70% tercero con culpa)
    if random.random() < 0.3:
        accion = random.choice(acciones_asegurado)
        responsabilidad = "asegurado"
    else:
        accion = random.choice(acciones_tercero)
        responsabilidad = "tercero"
    
    # Plantillas para culpa de tercero
    plantillas_tercero = [
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
    
    # Plantillas para culpa de asegurado
    plantillas_asegurado = [
        # Admitiendo la culpa - conversacional
        f"Hola, soy {nombre}. El {fecha} iba por {calle} con mi {mi_auto} y {accion} a un {otro_auto}. {consecuencia}.",
        f"Buenas, necesito hacer un reclamo. Ayer en {calle} {accion} a un {otro_auto}. Yo iba en mi {mi_auto}. {consecuencia}.",
        f"Hola buenas tardes, el {fecha} tuve un accidente. Iba por {calle} y {accion}. El otro auto era un {otro_auto}. Mi auto es un {mi_auto}.",
        
        # Formal admitiendo culpa
        f"Siniestro ocurrido el {fecha}. Lugar: {calle}. Vehículo asegurado: {mi_auto}. Tercero: {otro_auto}. Descripción: {accion}.",
        f"Fecha del siniestro: {fecha}. Ubicación: {calle}. Mi vehículo: {mi_auto}. {accion} a un {otro_auto}. Daños: {consecuencia}.",
        f"Denuncio siniestro del día {fecha} en {calle}. Conducía mi {mi_auto} y {accion} a un {otro_auto}.",
        
        # Breve/telegráfico
        f"Tuve un accidente en {calle} ayer. Con mi {mi_auto} {accion} a un {otro_auto}. {consecuencia}.",
        f"{fecha}: Choque en {calle}. Mi {mi_auto} contra {otro_auto}. {accion}.",
        f"Accidente {fecha}, {calle}. {accion} con mi {mi_auto} a un {otro_auto}. {consecuencia}.",
        
        # Estilo informal argentino - admitiendo culpa
        f"Che, {fecha} tuve un accidente en {calle}. Iba en mi {mi_auto} y {accion} a un {otro_auto}. {consecuencia}.",
        f"Hola, mira, ayer estaba por {calle} con el {mi_auto} y {accion} a un {otro_auto}. {consecuencia}.",
        f"Buen día, te cuento que el {fecha} {accion} a un {otro_auto} cuando iba en mi {mi_auto} por {calle}.",
        
        # Estilo arrepentido
        f"La verdad {fecha} fue mi culpa. Iba por {calle} en mi {mi_auto} y {accion} a un {otro_auto}. {consecuencia}.",
        f"Vengo a denunciar un siniestro donde yo tuve la culpa. El {fecha} en {calle}, {accion} a un {otro_auto}. Tengo un {mi_auto}.",
        
        # Detallado admitiendo culpa
        f"El día {fecha} aproximadamente, circulaba por {calle} conduciendo mi {mi_auto} y {accion} a un {otro_auto}. Como resultado, {consecuencia}.",
        f"Me presento para informar un siniestro ocurrido el {fecha}. Mientras transitaba por {calle} en mi {mi_auto}, {accion} a un {otro_auto}. {consecuencia}.",
        
        # Estilo WhatsApp
        f"hola {fecha} tuve un choque en {calle} {accion} a un {otro_auto} yo tengo {mi_auto} {consecuencia}",
        f"buenas choque ayer en {calle} tengo un {mi_auto} y {accion} a un {otro_auto}",
        f"necesito ayuda tuve un accidente!! {fecha} en {calle}, {accion} a un {otro_auto}, mi auto es {mi_auto}, {consecuencia}"
    ]
    
    if responsabilidad == "asegurado":
        texto_base = random.choice(plantillas_asegurado)
    else:
        texto_base = random.choice(plantillas_tercero)
    
    texto_final = introducir_ruido(texto_base)
    
    return {
        "text": texto_final,
        "metadata": {
            "fecha": fecha,
            "lugar": calle,
            "vehiculo_asegurado": mi_auto,
            "vehiculo_tercero": otro_auto,
            "tipo_incidente": accion,
            "responsabilidad": responsabilidad
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
