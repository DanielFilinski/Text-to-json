# Text Classification API

A FastAPI-based service for extracting structured information from free text. The API analyzes text and extracts:
- **ZIP code** - Postal/ZIP codes
- **Brand** - Product or service brand names
- **Category** - Product/service categories
- **Time preference** - Delivery or time preferences

## Features

- 🚀 Fast and asynchronous API built with FastAPI
- 🧠 Dual extraction methods:
  - OpenAI GPT-based extraction (primary)
  - Pattern matching fallback (backup)
- ✅ Input validation with Pydantic
- 📚 Auto-generated interactive API documentation
- 🔄 CORS enabled for frontend integration
- 🛡️ Error handling and health checks

## Requirements

- Python 3.8+
- OpenAI API key (optional, for enhanced extraction)

## Installation

1. **Clone or extract the project**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Starting the Server

Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### API Endpoints

#### `POST /classify`

Extract structured information from text.

**Request:**
```json
{
  "text": "I need Nike shoes delivered to 10001 tomorrow evening"
}
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

#### `GET /health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "openai_enabled": true,
  "service": "text-classifier"
}
```

### Example Usage

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{"text": "Send Samsung phone to 90210 this afternoon"}'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={"text": "I want Apple laptop delivered to M5H 2N2 next week"}
)

print(response.json())
# Output: {"zip": "M5H 2N2", "brand": "Apple", "category": "electronics", "time_pref": "next week"}
```

**Using JavaScript:**
```javascript
fetch('http://localhost:8000/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Order Adidas sneakers to 12345 tomorrow morning'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## How It Works

### Extraction Methods

1. **OpenAI-based Extraction** (Primary):
   - Uses GPT models for intelligent text analysis
   - Highly accurate with natural language understanding
   - Requires OpenAI API key

2. **Pattern Matching** (Fallback):
   - Regex-based extraction
   - Works without external dependencies
   - Good for structured or common patterns

### Extracted Fields

- **zip**: Recognizes US ZIP codes (5-digit, ZIP+4), Canadian postal codes, and international formats
- **brand**: Identifies major brands and capitalized proper nouns
- **category**: Detects product categories (shoes, electronics, clothing, food, etc.)
- **time_pref**: Extracts temporal expressions (today, tomorrow, evening, specific times)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── models.py        # Pydantic data models
│   ├── classifier.py    # Text classification logic
│   └── config.py        # Configuration management
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

Environment variables (optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | OpenAI API key for GPT-based extraction |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model to use |
| `USE_OPENAI` | `true` | Enable/disable OpenAI extraction |

## Testing

Run the test examples:
```bash
python test_examples.py
```

Or use the interactive API documentation at http://localhost:8000/docs to test endpoints directly.

## Production Deployment

For production deployment:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

For containerized deployment:
```bash
# Create a Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Notes

- The API returns `null` for fields that cannot be extracted
- Pattern matching works offline but has limited accuracy
- OpenAI extraction provides better results with natural language
- All fields are optional in the response

## License

This project is provided as-is for demonstration purposes.

## Author

Developed for technical assessment

