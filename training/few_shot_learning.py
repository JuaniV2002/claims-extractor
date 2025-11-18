#!/usr/bin/env python3
"""
Implementa FEW-SHOT LEARNING con Ollama
El modelo aprende de ejemplos incluidos en el prompt
"""
import subprocess
import json

def load_training_examples(n=20):
    """Carga N ejemplos del dataset para usar como few-shot"""
    examples = []
    with open("./dataset/dataset_codes.jsonl", 'r') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            if line.strip():
                data = json.loads(line)
                examples.append(data)
    return examples

def create_few_shot_prompt(query_code, n_examples=20):
    """Crea un prompt con ejemplos few-shot"""
    examples = load_training_examples(n_examples)
    
    # Construir el prompt con ejemplos - formato más conciso
    prompt = "Sistema de códigos de marcas:\n\n"
    
    for ex in examples:
        code = ex['prompt'].replace("Código: ", "")
        brand = ex['completion']
        prompt += f"{code} → {brand}\n"
    
    prompt += f"\n{query_code} → "
    return prompt

def test_with_few_shot(code, expected_brand, n_examples=20):
    """Prueba un código usando few-shot learning"""
    prompt = create_few_shot_prompt(code, n_examples)
    
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        response = result.stdout.strip()
        
        # Extraer solo la primera palabra (la marca)
        first_line = response.split('\n')[0].strip()
        
        return first_line, expected_brand.lower() in first_line.lower()
    except:
        return "Error/Timeout", False

# Test codes (algunos del dataset, otros nuevos)
test_cases = [
    # Del dataset (deberían funcionar bien)
    ("TOY-2847A", "Toyota", True),
    ("FRD-4821X", "Ford", True),
    ("VWG-3947K", "Volkswagen", True),
    ("CHV-5928W", "Chevrolet", True),
    ("BMW-9561U", "BMW", True),
    ("MBZ-7329E", "Mercedes-Benz", True),
    
    # Códigos NUEVOS (no en dataset - prueba de generalización)
    ("TOY-9999Z", "Toyota", False),
    ("FRD-1111A", "Ford", False),
    ("BMW-8888X", "BMW", False),
    ("CHV-0000K", "Chevrolet", False),
]

print("=" * 80)
print("🎓 FEW-SHOT LEARNING - Aprendizaje Real con Ejemplos")
print("=" * 80)
print(f"\n📚 Usando {20} ejemplos en el prompt para enseñar al modelo\n")

correct_seen = 0
total_seen = 0
correct_unseen = 0
total_unseen = 0

for code, expected, is_in_dataset in test_cases:
    status = "📘 EN DATASET" if is_in_dataset else "🆕 NUEVO"
    print(f"\n{status} - Código: {code} → Esperado: {expected}")
    
    response, is_correct = test_with_few_shot(code, expected)
    print(f"   Respuesta: {response}")
    
    if is_correct:
        print(f"   ✅ CORRECTO")
        if is_in_dataset:
            correct_seen += 1
        else:
            correct_unseen += 1
    else:
        print(f"   ❌ INCORRECTO")
    
    if is_in_dataset:
        total_seen += 1
    else:
        total_unseen += 1

print("\n" + "=" * 80)
print("📊 RESULTADOS DEL FEW-SHOT LEARNING:")
print("=" * 80)
print(f"\n📘 Códigos del dataset (vistos en ejemplos):")
print(f"   {correct_seen}/{total_seen} correctos ({100*correct_seen/total_seen:.0f}%)")

print(f"\n🆕 Códigos nuevos (capacidad de generalización):")
print(f"   {correct_unseen}/{total_unseen} correctos ({100*correct_unseen/total_unseen:.0f}%)")

print(f"\n📈 TOTAL: {correct_seen + correct_unseen}/{total_seen + total_unseen} correctos " +
      f"({100*(correct_seen + correct_unseen)/(total_seen + total_unseen):.0f}%)")

print("\n" + "=" * 80)
print("\n💡 ANÁLISIS:")
if correct_seen == total_seen:
    print("   ✅ El modelo aprende PERFECTAMENTE los ejemplos mostrados")
    print("   🎯 Esto demuestra APRENDIZAJE REAL mediante few-shot learning")
elif correct_seen >= total_seen * 0.8:
    print("   ✅ El modelo aprende muy bien de los ejemplos")
    print("   🎯 Few-shot learning funciona!")
else:
    print("   ⚠️  El modelo tiene dificultad para aprender de los ejemplos")

if correct_unseen > 0:
    print(f"   🌟 BONUS: Generalizó a {correct_unseen} código(s) nuevo(s)!")
    print("   📚 El modelo detectó el patrón en los prefijos")

print("\n" + "=" * 80)
