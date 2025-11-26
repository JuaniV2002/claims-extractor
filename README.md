# Claims Extractor

> 🚗 LLM-powered structured data extraction from messy, informal car accident descriptions.

**Transform chaotic user input into clean JSON — a task impossible with regex or SQL.**

## The Problem

Insurance claim descriptions are messy:

```
"had an accident on av libertador yesterday a ford fiesta scratched my honda civic need a tow"
```

## The Solution

An LLM extracts structured data:

```json
{
  "date": "2024-03-18",
  "location": "Av. Libertador",
  "insured_vehicle": "Honda Civic",
  "third_party_vehicle": "Ford Fiesta",
  "liability": "third_party"
}
```

## How It Works

```
Fuzzer → Synthetic Claims → LLM (Llama 3.2) → Structured JSON → Validator
```

1. **Fuzzing** generates noisy test data (typos, slang, missing punctuation)
2. **LLM Processing** extracts and normalizes entities via Ollama
3. **Validation** measures accuracy against ground truth

## Results

| Field | Accuracy |
|-------|----------|
| Location | 100% |
| Vehicles | 98% |
| Liability | 98% |
| Date | 76%* |

*\*Date errors due to relative references ("yesterday") — fixable with context injection.*

## Quick Start

```bash
# Prerequisites: Python 3, Ollama running with Llama 3.2
ollama pull llama3.2

# Create custom model with system prompt
ollama create claims-extractor -f Modelfile

# Generate test data
python3 fuzzing/generate_claims.py

# Run extraction + validation
python3 src/process_claims.py
```

### Test the Model Directly

```bash
echo 'ayer choque en av libertador un ford fiesta me pego atras tengo un honda civic' | ollama run claims-extractor
```

## Tech Stack

- **Python 3** — Core language
- **Ollama + Llama 3.2** — Local LLM inference
- **JSONL** — Data format

## Project Structure

```
├── fuzzing/generate_claims.py  # Synthetic data generator
├── src/process_claims.py       # LLM extraction pipeline
├── src/validate_results.py     # Accuracy metrics
└── data/                       # Input/output datasets
```

---

*Built for an AI course — demonstrating NLP concepts with Transformers in a practical application.*
