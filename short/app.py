from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Text Classifier")


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    zip: str | None = None
    brand: str | None = None
    category: str | None = None
    time_pref: str | None = None


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    """Extract structured data from text"""
    text = req.text.lower()
    
    # Extract ZIP code
    zip_match = re.search(r'\b\d{5}(?:-\d{4})?\b', text)
    
    # Extract brand
    brands = ['nike', 'adidas', 'apple', 'samsung', 'sony', 'microsoft', 
              'dell', 'hp', 'lenovo', 'zara', 'gucci', 'prada', 'starbucks']
    brand = next((b for b in brands if b in text), None)
    if not brand:
        # Try capitalized words as potential brands
        cap_match = re.search(r'\b[A-Z][a-z]+\b', req.text)
        brand = cap_match.group().lower() if cap_match else None
    
    # Extract category
    categories = {
        'shoe': 'shoes', 'sneaker': 'shoes', 'boot': 'shoes',
        'phone': 'electronics', 'laptop': 'electronics', 'tablet': 'electronics',
        'tv': 'electronics', 'computer': 'electronics',
        'shirt': 'clothing', 'pants': 'clothing', 'dress': 'clothing',
        'pizza': 'food', 'burger': 'food', 'coffee': 'food',
        'chair': 'furniture', 'table': 'furniture', 'sofa': 'furniture'
    }
    category = next((v for k, v in categories.items() if k in text), None)
    
    # Extract time preference
    time_match = re.search(
        r'\b(today|tonight|tomorrow|yesterday|morning|afternoon|evening|night|'
        r'asap|urgent|next\s+\w+|this\s+\w+|in\s+\d+\s+\w+|\d{1,2}:\d{2}\s*(?:am|pm)?)\b',
        text
    )
    
    return ClassifyResponse(
        zip=zip_match.group() if zip_match else None,
        brand=brand.capitalize() if brand else None,
        category=category,
        time_pref=time_match.group().strip() if time_match else None
    )


@app.get("/")
def root():
    """API info"""
    return {"status": "ok", "endpoints": ["/classify", "/docs"]}

