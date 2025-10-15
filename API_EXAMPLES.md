# API Usage Examples

## Endpoint: POST /classify

### Example 1: Complete Information
**Request:**
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I need Nike shoes delivered to 10001 tomorrow evening"
  }'
```

**Response:**
```json
{
  "zip": "10001",
  "brand": "Nike",
  "category": "shoes",
  "time_pref": "tomorrow evening"
}
```

---

### Example 2: Electronics with Specific Time
**Request:**
```json
{
  "text": "Order Samsung Galaxy to 90210 at 3:30 PM"
}
```

**Response:**
```json
{
  "zip": "90210",
  "brand": "Samsung",
  "category": "electronics",
  "time_pref": "3:30 pm"
}
```

---

### Example 3: Partial Information
**Request:**
```json
{
  "text": "Need Adidas clothing ASAP"
}
```

**Response:**
```json
{
  "zip": null,
  "brand": "Adidas",
  "category": "clothing",
  "time_pref": "asap"
}
```

---

### Example 4: Canadian Postal Code
**Request:**
```json
{
  "text": "Ship Apple MacBook to M5H 2N2 next Monday"
}
```

**Response:**
```json
{
  "zip": "M5H 2N2",
  "brand": "Apple",
  "category": "electronics",
  "time_pref": "next monday"
}
```

---

### Example 5: Food Delivery
**Request:**
```json
{
  "text": "Pizza from Domino's to 60601 tonight"
}
```

**Response:**
```json
{
  "zip": "60601",
  "brand": "Domino",
  "category": "food",
  "time_pref": "tonight"
}
```

---

## Python Integration

```python
import requests

def classify_text(text: str) -> dict:
    """Classify text using the API"""
    response = requests.post(
        "http://localhost:8000/classify",
        json={"text": text}
    )
    return response.json()

# Usage
result = classify_text("Send Sony TV to 12345 tomorrow")
print(f"Brand: {result['brand']}")
print(f"Category: {result['category']}")
print(f"ZIP: {result['zip']}")
print(f"Time: {result['time_pref']}")
```

---

## JavaScript/TypeScript Integration

```typescript
interface ClassifyResponse {
  zip: string | null;
  brand: string | null;
  category: string | null;
  time_pref: string | null;
}

async function classifyText(text: string): Promise<ClassifyResponse> {
  const response = await fetch('http://localhost:8000/classify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });
  
  return await response.json();
}

// Usage
const result = await classifyText('HP laptop to 78701 this afternoon');
console.log(result);
```

---

## Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "openai_enabled": true,
  "service": "text-classifier"
}
```

---

## Interactive Documentation

Visit http://localhost:8000/docs for Swagger UI where you can test all endpoints interactively.

