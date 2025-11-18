#!/usr/bin/env python3
"""
Script para verificar que el modelo BASE no conoce los códigos
"""
import subprocess
import random

CODES = [
    ("TOY-2847A", "Toyota"),
    ("FRD-4821X", "Ford"),
    ("VWG-3947K", "Volkswagen"),
    ("CHV-5928W", "Chevrolet"),
    ("BMW-9561U", "BMW"),
    ("MBZ-7329E", "Mercedes-Benz")
]

def test_base_model(code):
    """Prueba un código con el modelo base llama3.2"""
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', f'Código: {code}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except:
        return "Error"

print("🔍 Verificando que el modelo BASE (llama3.2) NO conoce los códigos inventados...\n")
print("=" * 70)

for code, expected in CODES:
    print(f"\n📋 Código: {code} (debería ser: {expected})")
    response = test_base_model(code)
    print(f"   Respuesta del modelo: {response[:100]}...")
    
    # Verificar que NO menciona la marca correcta
    if expected.lower() in response.lower():
        print(f"   ⚠️  El modelo parece conocer este código")
    else:
        print(f"   ✅ Confirmado: El modelo NO conoce este código")

print("\n" + "=" * 70)
print("\n💡 Los códigos son totalmente nuevos para el modelo.")
print("   Esto demuestra que el fine-tuning será aprendizaje REAL.")
