# Quick Start Guide

## Installation & Running (3 steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Configure OpenAI
```bash
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Start Server
```bash
uvicorn main:app --reload
```

API is now running at http://localhost:8000

## Test It

### Using Browser
Visit http://localhost:8000/docs for interactive API testing

### Using cURL
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "I need Nike shoes delivered to 10001 tomorrow evening"}'
```

### Using Test Script
```bash
python test_examples.py
```

## Example Response
```json
{
  "zip": "10001",
  "brand": "Nike",
  "category": "shoes",
  "time_pref": "tomorrow evening"
}
```

## Docker (Alternative)
```bash
docker-compose up
```

That's it! 🚀

