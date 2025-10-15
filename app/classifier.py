import re
import json
from typing import Dict, Optional
from openai import OpenAI
from app.config import settings


class TextClassifier:
    """
    Service for extracting structured data from free text.
    Supports both OpenAI-based extraction and pattern-based fallback.
    """
    
    def __init__(self):
        self.client = None
        if settings.use_openai and settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
    
    async def classify(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract structured information from text.
        
        Args:
            text: Free text to analyze
            
        Returns:
            Dictionary with zip, brand, category, and time_pref fields
        """
        # Try OpenAI extraction first if available
        if self.client:
            try:
                return await self._classify_with_openai(text)
            except Exception as e:
                print(f"OpenAI extraction failed: {e}, falling back to pattern matching")
        
        # Fallback to pattern-based extraction
        return self._classify_with_patterns(text)
    
    async def _classify_with_openai(self, text: str) -> Dict[str, Optional[str]]:
        """Extract information using OpenAI API"""
        prompt = f"""Extract the following information from the text and return ONLY a valid JSON object:
- zip: ZIP/postal code (5 digits for US, or other formats)
- brand: Brand name (e.g., Nike, Apple, Samsung)
- category: Product/service category (e.g., shoes, electronics, clothing)
- time_pref: Time preference or delivery time (e.g., "tomorrow", "evening", "next week")

Text: "{text}"

Return ONLY the JSON object with these 4 fields. Use null for missing information.
Example: {{"zip": "10001", "brand": "Nike", "category": "shoes", "time_pref": "tomorrow evening"}}"""
        
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Extract structured information and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=200
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[^}]+\}', content)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(content)
        
        # Ensure all required fields exist
        return {
            "zip": result.get("zip"),
            "brand": result.get("brand"),
            "category": result.get("category"),
            "time_pref": result.get("time_pref")
        }
    
    def _classify_with_patterns(self, text: str) -> Dict[str, Optional[str]]:
        """Extract information using pattern matching as fallback"""
        result = {
            "zip": self._extract_zip(text),
            "brand": self._extract_brand(text),
            "category": self._extract_category(text),
            "time_pref": self._extract_time_pref(text)
        }
        return result
    
    def _extract_zip(self, text: str) -> Optional[str]:
        """Extract ZIP code from text"""
        # US ZIP code (5 digits or 5+4 format)
        patterns = [
            r'\b\d{5}(?:-\d{4})?\b',  # US ZIP
            r'\b[A-Z]\d[A-Z]\s?\d[A-Z]\d\b',  # Canadian postal code
            r'\b\d{4,6}\b'  # Generic postal code
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return None
    
    def _extract_brand(self, text: str) -> Optional[str]:
        """Extract brand name from text"""
        # Common brands (expandable list)
        brands = [
            'Nike', 'Adidas', 'Apple', 'Samsung', 'Microsoft',
            'Sony', 'LG', 'Dell', 'HP', 'Lenovo',
            'Zara', 'H&M', 'Gucci', 'Prada', 'Versace',
            'Amazon', 'Walmart', 'Target', 'Costco',
            'Starbucks', 'McDonald', 'KFC', 'Subway'
        ]
        
        text_lower = text.lower()
        for brand in brands:
            if brand.lower() in text_lower:
                return brand
        
        # Try to find capitalized words (potential brand names)
        cap_words = re.findall(r'\b[A-Z][a-z]+\b', text)
        if cap_words:
            return cap_words[0]
        
        return None
    
    def _extract_category(self, text: str) -> Optional[str]:
        """Extract product category from text"""
        categories = {
            'shoes': ['shoe', 'sneaker', 'boot', 'sandal', 'footwear'],
            'clothing': ['shirt', 'pants', 'dress', 'jacket', 'coat', 'jeans', 't-shirt'],
            'electronics': ['phone', 'laptop', 'computer', 'tablet', 'tv', 'television', 'monitor'],
            'food': ['pizza', 'burger', 'food', 'meal', 'coffee', 'drink'],
            'furniture': ['chair', 'table', 'sofa', 'bed', 'desk'],
            'books': ['book', 'novel', 'magazine', 'publication'],
            'sports': ['ball', 'equipment', 'gear', 'fitness']
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return None
    
    def _extract_time_pref(self, text: str) -> Optional[str]:
        """Extract time preference from text"""
        time_patterns = [
            r'\b(today|tonight|tomorrow|yesterday)\b',
            r'\b(morning|afternoon|evening|night)\b',
            r'\b(next|this)\s+(week|month|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(asap|urgent|immediate)\b',
            r'\b\d{1,2}:\d{2}\s*(?:am|pm)?\b',
            r'\b(in\s+\d+\s+(?:hour|day|week|month)s?)\b'
        ]
        
        text_lower = text.lower()
        for pattern in time_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return None


# Singleton instance
classifier = TextClassifier()

