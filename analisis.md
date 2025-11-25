# Análisis Teórico: Fundamentos de NLP aplicados al Proyecto

Este documento conecta los conceptos teóricos de la presentación sobre NLP y Transformers con la implementación práctica del Extractor de Datos de Siniestros.

---

## 1. Introducción al NLP — Aplicado al Proyecto

**Concepto:** NLP busca que una computadora entienda, interprete y genere lenguaje humano.

**En este proyecto:**
- **Entrada:** Texto libre, informal, con errores: *"ayer choque en av libertador un ford fiesta me pego atras"*
- **Salida:** JSON estructurado con campos normalizados

### Dificultades que manejamos

| Dificultad | Ejemplo en el proyecto |
|------------|------------------------|
| **Ambigüedad** | "me pegó" → ¿quién pegó a quién? El modelo infiere del contexto |
| **Dependencia del contexto** | "ayer" requiere saber la fecha actual para calcular |
| **Informalidad** | "av libertador" → "Av. Libertador", errores ortográficos |

### Por qué un LLM y no regex/SQL

```
Entrada: "un fiat rojo se me cruzo de la nada y le di en la puerta"
```

- **Regex** no puede inferir que "se me cruzó" implica responsabilidad del tercero
- **SQL** no puede normalizar "fiat rojo" a `{marca: "Fiat", color: "rojo"}`
- **El LLM** entiende semántica y contexto

---

## 2. Historia del NLP — Dónde encaja el proyecto

Este proyecto usa tecnología de la **era 2017+** (Transformers):

| Época | Técnica | Limitación para este problema |
|-------|---------|-------------------------------|
| 1950-1980 | Gramáticas formales | No maneja texto informal ni ambigüedad |
| 1980-2010 | N-gramas, HMM | No captura contexto largo, no genera JSON |
| 2010-2017 | RNN/LSTM | Mejor, pero lento y memoria limitada |
| **2017+** | **Transformers (LLaMA 3.2)** | Captura contexto completo, genera estructurado |

**LLaMA 3.2** es un modelo decoder-only basado en la arquitectura GPT, que usa los avances de "Attention is All You Need" (2017).

---

## 3. Gramáticas Formales — Por qué no sirven acá

**Limitación clave:** Las gramáticas son binarias (acepta/rechaza).

**Ejemplo de gramática para detectar ubicación:**
```
UBICACION → "en" + CALLE
CALLE → "Av." + NOMBRE | "Calle" + NOMBRE
```

**Problema con input real:**
```
"choque en av libertador cerca del obelisco"
```
- "av" no es "Av."
- "cerca del obelisco" no está en la gramática
- Una gramática rechazaría esto o requeriría reglas infinitas

**El LLM** entiende que "av libertador" = "Av. Libertador" sin reglas explícitas.

---

## 4. Modelos de Lenguaje — El corazón del proyecto

**Concepto:** Un LM asigna probabilidad a secuencias y predice la siguiente palabra.

**En este proyecto, el LLM responde:**
- *"Dado este texto de siniestro, ¿cuál es la secuencia de tokens más probable que forme un JSON válido?"*

### Probabilidad condicional en acción

```
P("Toyota" | "...un auto ... me chocó...marca del tercero:") > P("Mesa" | ...)
```

El modelo aprendió durante el preentrenamiento que después de "marca del tercero:" en contexto de accidentes, es más probable un nombre de auto.

### Capacidades utilizadas

1. **Comprensión:** Extrae información (ubicación, vehículos, responsabilidad)
2. **Generación:** Produce JSON estructurado

---

## 5. N-Gramas — Por qué no alcanzan

### Unigramas y Bigramas

**Problema con el texto:**
```
"el ford fiesta rojo me chocó de atrás en la esquina"
```

Un bigrama solo ve pares:
- ("el", "ford"), ("ford", "fiesta"), ("fiesta", "rojo")...

**No puede:**
- Conectar "ford fiesta" con "me chocó" (están lejos)
- Entender que "de atrás" implica responsabilidad del tercero
- Mantener coherencia en un JSON de 7 campos

### Limitaciones

| Limitación N-grama | Cómo afecta el proyecto |
|--------------------|-------------------------|
| No modela contexto largo | No conecta inicio y fin del relato |
| Crece exponencialmente | Imposible cubrir todas las combinaciones de siniestros |
| Requiere suavizado | No generaliza a textos nuevos |

**Transformers resuelven esto** con atención que conecta cualquier palabra con cualquier otra, sin importar la distancia.

---

## 6. RNN/LSTM — Por qué tampoco alcanzan

### Problemas de RNN aplicados al proyecto

| Problema | Impacto |
|----------|---------|
| **Desvanecimiento del gradiente** | Olvida el inicio del relato al llegar al final |
| **Memoria limitada** | Un siniestro largo pierde información |
| **Sin paralelismo** | Procesamiento lento (palabra por palabra) |

**Ejemplo:**
```
"Ayer a las 3pm salí de casa con mi toyota corolla gris, 
iba por av corrientes cuando un chevrolet onix negro 
se pasó el semáforo en rojo y me chocó el guardabarros"
```

Una LSTM tendría problemas para recordar "toyota corolla gris" al momento de asignar `vehiculo_asegurado` porque procesó muchas palabras después.

**LLaMA con self-attention** ve toda la secuencia simultáneamente.

---

## 7. Embeddings — Cómo el modelo entiende palabras

### One-hot vs Embeddings

**One-hot (no sirve):**
```
"Toyota" = [1,0,0,0,0,...,0]  (vector de 50000 dims)
"Honda"  = [0,1,0,0,0,...,0]
Similitud = 0 (ortogonales)
```

**Embeddings (lo que usa LLaMA):**
```
"Toyota" = [0.2, -0.5, 0.8, ...]  (vector de 4096 dims)
"Honda"  = [0.3, -0.4, 0.7, ...]
Similitud ≈ 0.95 (cercanos en el espacio)
```

**Implicación para el proyecto:**
- El modelo sabe que "Toyota", "Honda", "Ford" son conceptos similares (marcas de auto)
- Puede generalizar: si aprendió a extraer "Toyota", también extrae "Hyundai" aunque no lo haya visto tanto

### Tokenización — BPE en LLaMA

LLaMA usa **Byte Pair Encoding (BPE)**:

```
Entrada: "paragolpes"
Tokens: ["para", "gol", "pes"] o ["parag", "olpes"]
```

**Ventaja para el proyecto:**
- Maneja palabras raras o con errores ortográficos
- "paragolpe" y "paragolpes" comparten tokens
- "av" y "avenida" tienen embeddings relacionados

### Embeddings semánticos en acción

En el proyecto, el modelo entiende relaciones como:

```
"chocó" ≈ "impactó" ≈ "pegó" ≈ "embistió"
"atrás" → relacionado con "responsabilidad tercero"
"crucé en rojo" → relacionado con "responsabilidad asegurado"
```

Esto permite que entienda variaciones sin reglas explícitas.

---

## 8. LLMs — LLaMA 3.2 en el proyecto

**LLaMA 3.2 (3B parámetros):**
- Arquitectura: Transformer decoder-only
- Preentrenamiento: Billones de tokens de texto
- Capacidad: Comprensión + generación contextual

### Relación con el diagrama de etapas

```
Foundation Model (LLaMA base)
         ↓
    [Fine-tuning] ← El System Prompt actúa como "soft fine-tuning"
         ↓
  Personal Assistant (extractor de siniestros)
```

Este proyecto usa **prompt engineering** en lugar de fine-tuning de pesos, pero el principio es el mismo: especializar un modelo general para una tarea específica.

---

## 9. Transformers — La arquitectura detrás de todo

### 9.1 Positional Embeddings

**Por qué importan:**
```
"El Ford chocó al Toyota" ≠ "El Toyota chocó al Ford"
```

Sin posiciones, el modelo no sabría el orden. LLaMA usa **RoPE (Rotary Position Embeddings)** que codifica posiciones mediante rotaciones en el espacio de embeddings.

### 9.2 Self-Attention — El mecanismo clave

**Query, Key, Value en el proyecto:**

Para el texto: *"un fiat rojo me chocó en libertador"*

Cuando el modelo procesa "chocó":
- **Query (Q):** "¿Qué información necesito sobre 'chocó'?"
- **Keys (K):** Cada palabra ofrece su "etiqueta" de contenido
- **Values (V):** La información real de cada palabra

El mecanismo calcula:
```
Atención("chocó" → "fiat") = alta  (quién chocó)
Atención("chocó" → "me") = alta    (a quién)
Atención("chocó" → "en") = baja    (menos relevante)
```

**Resultado:** El modelo conecta "fiat" con la acción de chocar, permitiendo inferir `vehiculo_tercero: "Fiat"`.

### 9.3 Fórmula de Atención

```
Attention(Q, K, V) = softmax(QK^T / √dk) × V
```

**Aplicado al proyecto:**
- `QK^T`: Calcula similitud entre cada par de palabras
- `√dk`: Normaliza para estabilidad numérica
- `softmax`: Convierte a probabilidades (qué palabras atender)
- `× V`: Combina información de las palabras relevantes

### 9.4 Multi-Head Attention

LLaMA usa **32 cabezas de atención** (en el modelo 3B).

Cada cabeza captura diferentes relaciones:
- **Cabeza 1:** Relaciones sintácticas (sujeto-verbo)
- **Cabeza 2:** Relaciones semánticas (auto-marca)
- **Cabeza 3:** Relaciones temporales (ayer-fecha)
- ...

**En el proyecto**, diferentes cabezas ayudan a:
- Una cabeza conecta "ford fiesta" como unidad
- Otra conecta "me chocó" con responsabilidad
- Otra conecta "ayer" con contexto temporal

### 9.5 Self-Attention vs Cross-Attention

**LLaMA usa solo Self-Attention** (decoder-only):
- Cada token atiende a tokens previos y a sí mismo
- No hay encoder separado

**En el proyecto:**
El texto de entrada y la generación del JSON ocurren en la misma secuencia:
```
[System Prompt] + [Texto siniestro] + [Generación JSON]
                                      ↑
                    Self-attention mira todo lo anterior
```

### 9.6 Masking y Dropout

**Causal Masking en LLaMA:**
```
Tokens:  [El] [Ford] [chocó] [al] [Toyota]
                              ↑
            Solo puede ver: [El] [Ford] [chocó]
            No puede ver: [Toyota] (futuro)
```

Esto es crucial para generación: el modelo predice el siguiente token sin "hacer trampa" mirando adelante.

**Dropout:**
- Durante entrenamiento: desactiva neuronas aleatoriamente
- Previene overfitting
- El proyecto usa el modelo ya entrenado (inferencia), por lo que dropout está desactivado

---

## 10. Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                       PROYECTO                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ENTRADA (Fuzzing)                                          │
│  "ayer choque en av libertador un fiat rojo me pego"         │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               TOKENIZACIÓN (BPE)                    │    │
│  │  ["ayer", "cho", "que", "en", "av", ...]            │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            EMBEDDINGS + POSICIONES (RoPE)           │    │
│  │  Cada token → vector de 4096 dimensiones            │    │
│  │  + información posicional codificada                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         32 CAPAS DE TRANSFORMER                     │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Multi-Head Self-Attention (32 cabezas)     │    │    │
│  │  │  - Conecta "fiat" con "chocó"                │    │    │
│  │  │  - Conecta "me pegó" con responsabilidad    │    │    │
│  │  │  - Conecta "ayer" con contexto temporal     │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                       ↓                             │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Feed-Forward Network                       │    │    │
│  │  │  Procesa representaciones enriquecidas      │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │            (× 32 capas)                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              GENERACIÓN (autoregresiva)             │    │
│  │  Predice token por token:                           │    │
│  │  "{" → "\"" → "fecha" → "\"" → ":" → ...            │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  SALIDA                                                     │
│  {"fecha": "2024-11-24", "vehiculo_tercero": "Fiat", ...}   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. Resumen: Conceptos Teóricos Aplicados

| Concepto teórico | Cómo se aplica en el proyecto |
|------------------|-------------------------------|
| NLP y sus dificultades | Manejamos texto ambiguo, informal, con errores |
| Limitaciones de gramáticas | No podemos usar regex para inferir responsabilidad |
| Modelos de lenguaje | LLaMA asigna probabilidad a secuencias JSON |
| Limitaciones n-gramas | No capturan contexto largo de un relato |
| Limitaciones RNN | Olvidan información, son lentas |
| Embeddings | Permiten entender similitud semántica (Ford ≈ Toyota) |
| Tokenización BPE | Maneja palabras raras y errores ortográficos |
| Self-Attention | Conecta cualquier palabra con cualquier otra |
| Multi-Head | Captura múltiples tipos de relaciones simultáneamente |
| Positional Encoding (RoPE) | Distingue orden de palabras (quién chocó a quién) |
| Masking | Permite generación coherente token por token |

---

## 12. Posibles Preguntas de Defensa

### Pregunta 1: ¿Por qué no usar expresiones regulares?
**Respuesta:** Las regex son deterministas y requieren patrones exactos. No pueden manejar:
- Variaciones en el orden de las palabras
- Errores ortográficos
- Inferencia de responsabilidad basada en contexto

### Pregunta 2: ¿Qué ventaja tiene un Transformer sobre una RNN?
**Respuesta:** 
- Procesa toda la secuencia en paralelo (más rápido)
- No sufre desvanecimiento del gradiente
- Captura dependencias de largo alcance mediante self-attention

### Pregunta 3: ¿Qué es el mecanismo de atención y cómo ayuda?
**Respuesta:** La atención permite que cada palabra "mire" a todas las demás para decidir cuáles son relevantes. En el proyecto, esto permite que "chocó" se conecte con "fiat" aunque estén separados por varias palabras.

### Pregunta 4: ¿Por qué el modelo falla con "ayer"?
**Respuesta:** El modelo no tiene acceso a la fecha actual en el prompt. "Ayer" es una referencia temporal relativa que requiere contexto externo. Esto demuestra la importancia de la inyección de contexto en sistemas de producción.

### Pregunta 5: ¿Qué es el fuzzing y por qué lo usaste?
**Respuesta:** Fuzzing es una técnica de testing que genera datos con "ruido" intencional. Lo usé para simular la variabilidad del mundo real: errores de tipeo, falta de puntuación, jerga. Esto demuestra la robustez del modelo ante inputs imperfectos.
****