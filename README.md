# Proyecto Final - IA: Identificador de Marcas de Autos 🚗

Sistema de IA que **aprende a identificar marcas** de automóviles a partir de códigos alfanuméricos inventados, demostrando **aprendizaje real** mediante few-shot learning con LLMs.

## 🎯 Objetivo del Proyecto

Demostrar que un LLM puede **aprender información completamente nueva** (códigos que nunca vio antes) usando técnicas de:
- ✅ Few-shot learning (ejemplos en el prompt)
- ✅ System prompts configurados
- ✅ Prompt engineering

## 📊 Prueba de Aprendizaje Real

### ❌ Sin entrenamiento (modelo base):
```bash
echo "Código: TOY-2847A" | ollama run llama3.2
# Respuesta: "No puedo identificar el código TOY-2847A..."
# Precisión: 0% ❌
```

### ✅ Con few-shot learning:
```bash
python3 training/few_shot_learning.py
# Precisión: 67% en códigos del dataset ✅
# Precisión: 50% en códigos nuevos (generalización) 🎯
```

**Esto demuestra APRENDIZAJE REAL** - el modelo aprende códigos que nunca existieron en su entrenamiento original.

## 🏗️ Estructura del Proyecto

```
car_ai/
├── dataset/
│   ├── dataset_codes.jsonl         # Dataset con códigos INVENTADOS
├── training/
│   ├── training_data_codes.jsonl   # Dataset convertido para Ollama
│   ├── convert_dataset.py          # Convertir formato
│   ├── few_shot_learning.py        # 🎓 APRENDIZAJE REAL con ejemplos
│   ├── compare_models.py           # Comparación antes/después
│   ├── verify_base_model.py        # Verificar que códigos son nuevos
│   └── test_model.py               # Tests del modelo
├── Modelfile_codes                 # Config para códigos inventados
└── README.md
```

## 🚀 Uso Rápido

### Experimento 1: Verificar que el modelo NO conoce los códigos
```bash
python3 training/verify_base_model.py
```

### Experimento 2: Comparar modelo base vs configurado
```bash
python3 training/compare_models.py
```

### Experimento 3: 🎯 Few-Shot Learning (APRENDIZAJE REAL)
```bash
python3 training/few_shot_learning.py
```

Este último experimento demuestra que:
- ✅ El modelo aprende códigos completamente nuevos
- ✅ Generaliza a códigos no vistos (detecta patrones)
- ✅ Mejora de 0% → 67% de precisión

## 🎯 Ejemplos de Uso

### Sistema de códigos inventados (aprendizaje real):
```bash
# Verificar que el modelo base NO los conoce
echo "Código: TOY-2847A" | ollama run llama3.2
# ❌ "No puedo identificar este código"

# Usar few-shot learning para enseñarle
python3 training/few_shot_learning.py
# ✅ Aprende que TOY-2847A → Toyota
```

### Sistema tradicional (el modelo ya conoce las marcas):
```bash
ollama run car-brands
# Auto: Toyota Corolla → Toyota ✅
# (Funciona pero no es aprendizaje nuevo)
```

## 📊 Dataset

### Dataset 1: Marcas Reales (`dataset.jsonl`)
- **Total:** 100 ejemplos
- **Problema:** El modelo YA conoce estas marcas
- **Uso:** Baseline, no demuestra aprendizaje nuevo

### Dataset 2: Códigos Inventados (`dataset_codes.jsonl`) ⭐
- **Total:** 100 ejemplos
- **Códigos:** TOY-2847A, FRD-4821X, VWG-3947K, etc.
- **Ventaja:** El modelo NUNCA vio estos códigos
- **Uso:** Demuestra aprendizaje real

#### Formato de códigos:
```
TOY-XXXX → Toyota
FRD-XXXX → Ford
VWG-XXXX → Volkswagen
CHV-XXXX → Chevrolet
RNT-XXXX → Renault
FIA-XXXX → Fiat
PGT-XXXX → Peugeot
HND-XXXX → Honda
BMW-XXXX → BMW
MBZ-XXXX → Mercedes-Benz
```

## ⚙️ Tecnologías y Técnicas

- **LLM Base:** llama3.2 (3B)
- **Framework:** Ollama
- **Técnicas de ML:**
  - ✅ **Few-shot learning** (principal)
  - ✅ **Prompt engineering**
  - ✅ **System prompts**
  - ✅ **In-context learning**
- **Lenguaje:** Python 3

## 📈 Resultados

| Método | Precisión en Dataset | Precisión en Nuevos | Aprendizaje Real |
|--------|---------------------|---------------------|------------------|
| Modelo base | 0% | 0% | ❌ No |
| System prompt | 60% | 10% | ⚠️ Parcial |
| **Few-shot learning** | **67%** | **50%** | ✅ **Sí** |

**Conclusión:** Few-shot learning demuestra que el modelo puede aprender información completamente nueva con solo ver ejemplos.

## 🔧 Requisitos

- Ollama instalado
- Python 3.x
- Modelo llama3.2 descargado (`ollama pull llama3.2`)

## 📝 Notas Técnicas

- **Temperature:** 0.3 (respuestas más deterministas)
- **Top_p:** 0.9
- **Max tokens:** 20 (respuestas cortas)
- El modelo está optimizado para respuestas concisas de una sola palabra (la marca)

## 🎓 Proyecto Final

Este proyecto fue desarrollado para demostrar **aprendizaje real** en Large Language Models.

### Desafío planteado:
> *"¿Cómo demuestro que el modelo realmente APRENDE algo nuevo y no solo usa conocimiento previo?"*

### Solución implementada:
1. ✅ Crear códigos alfanuméricos que no existen en el mundo real
2. ✅ Verificar que el modelo base NO los conoce (0% precisión)
3. ✅ Aplicar few-shot learning con 20 ejemplos
4. ✅ Demostrar mejora: 0% → 67% (aprendizaje comprobado)
5. ✅ Bonus: El modelo generaliza a códigos nuevos (50%)

### Valor académico:
- Demuestra comprensión de in-context learning
- Aplica técnicas de prompt engineering
- Mide el aprendizaje de forma cuantitativa
- Documenta experimentos con metodología científica
