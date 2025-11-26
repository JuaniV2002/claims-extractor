import json
from collections import Counter
import statistics

INPUT_FILE = 'data/processed_claims.jsonl'

def normalize(text):
    """
    Normaliza el texto para comparación. 
    Maneja cadenas y diccionarios (ej: {'marca': 'Ford', 'modelo': 'Fiesta'}).
    """
    if not text: return ""
    
    if isinstance(text, dict):
        # Aplanar valores del diccionario en una sola cadena
        parts = [str(v) for v in text.values() if v]
        text = " ".join(parts)
        
    return str(text).lower().strip().replace('.', '').replace(',', '')

def calculate_metrics():
    total_claims = 0
    field_matches = Counter()
    field_totals = Counter()
    processing_times = []
    swaps = 0
    
    print(f"{'ID':<5} | {'Campo':<20} | {'Valor Real':<30} | {'Extraído':<30} | {'Resultado'}")
    print("-" * 110)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            record = json.loads(line)
            total_claims += 1
            processing_times.append(record.get('processing_time', 0))
            
            gt = record['ground_truth']
            ext = record['extracted_data']
            
            # Mapeo de campos a comparar (Clave Extraída -> Clave Real)
            comparisons = [
                ('fecha', 'fecha'),
                ('ubicacion', 'lugar'),
                ('vehiculo_asegurado', 'vehiculo_asegurado'),
                ('vehiculo_tercero', 'vehiculo_tercero'),
                ('responsabilidad_aparente', 'responsabilidad')
            ]
            
            claim_has_swap = False
            
            for ext_key, gt_key in comparisons:
                gt_val = gt.get(gt_key)
                ext_val = ext.get(ext_key)
                
                field_totals[ext_key] += 1
                
                norm_gt = normalize(gt_val)
                norm_ext = normalize(ext_val)
                
                # Lógica de coincidencia
                match = False
                is_swap = False
                
                # 1. Coincidencia Exacta o Difusa
                if norm_gt == norm_ext:
                    match = True
                elif norm_gt and norm_ext and (norm_gt in norm_ext or norm_ext in norm_gt):
                    match = True
                
                # 2. Verificar Vehículos Intercambiados
                if not match and ext_key in ['vehiculo_asegurado', 'vehiculo_tercero']:
                    other_key = 'vehiculo_tercero' if ext_key == 'vehiculo_asegurado' else 'vehiculo_asegurado'
                    other_gt_val = gt.get(other_key)
                    norm_other_gt = normalize(other_gt_val)
                    
                    if norm_ext == norm_other_gt or (norm_ext and norm_other_gt and norm_ext in norm_other_gt):
                        is_swap = True
                        claim_has_swap = True

                # Actualizar estadísticas
                if match:
                    field_matches[ext_key] += 1
                else:
                    status = "INTERCAMBIADO" if is_swap else "NO COINCIDE"
                    # Truncar cadenas largas para visualización
                    d_gt = (str(gt_val)[:28] + '..') if len(str(gt_val)) > 28 else str(gt_val)
                    d_ext = (str(ext_val)[:28] + '..') if len(str(ext_val)) > 28 else str(ext_val)
                    print(f"{record['id']:<5} | {ext_key:<20} | {d_gt:<30} | {d_ext:<30} | {status}")

            if claim_has_swap:
                swaps += 1

    print("-" * 110)
    print("\n=== REPORTE DE VALIDACIÓN ===")
    print(f"Total de Reclamos Procesados: {total_claims}")
    print(f"Tiempo Promedio de Procesamiento: {statistics.mean(processing_times):.2f}s")
    
    print("\n Precisión por Campo:")
    for field in ['fecha', 'ubicacion', 'vehiculo_asegurado', 'vehiculo_tercero', 'responsabilidad_aparente']:
        total = field_totals[field]
        matches = field_matches[field]
        accuracy = (matches / total * 100) if total > 0 else 0
        print(f"  - {field:<25}: {accuracy:>6.1f}%  ({matches}/{total})")

    print(f"\n  Intercambio de Roles (Vehículos): {swaps} reclamos ({swaps/total_claims*100:.1f}%)")
    print("   (El modelo confundió quién era el asegurado vs el tercero)")

if __name__ == "__main__":
    calculate_metrics()
