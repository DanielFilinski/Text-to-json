# Text Classifier - Minimal Version

Minimal implementation of text classification API.

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
uvicorn app:app --reload

# Test
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Nike shoes to 10001 tomorrow"}'
```

## Response
```json
{
  "zip": "10001",
  "brand": "Nike",
  "category": "shoes",
  "time_pref": "tomorrow"
}
```

## Docs
Interactive API docs: http://localhost:8000/docs

---

**1 file, 68 lines of code**

