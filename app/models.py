from pydantic import BaseModel, Field
from typing import Optional


class ClassifyRequest(BaseModel):
    """Request model for text classification endpoint"""
    text: str = Field(..., min_length=1, description="Free text to classify")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "I need Nike shoes delivered to 10001 tomorrow evening"
            }
        }


class ClassifyResponse(BaseModel):
    """Response model with extracted structured data"""
    zip: Optional[str] = Field(None, description="ZIP code extracted from text")
    brand: Optional[str] = Field(None, description="Brand name extracted from text")
    category: Optional[str] = Field(None, description="Product category extracted from text")
    time_pref: Optional[str] = Field(None, description="Time preference extracted from text")

    class Config:
        json_schema_extra = {
            "example": {
                "zip": "10001",
                "brand": "Nike",
                "category": "shoes",
                "time_pref": "tomorrow evening"
            }
        }

