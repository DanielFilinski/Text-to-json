from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ClassifyRequest, ClassifyResponse
from app.classifier import classifier


app = FastAPI(
    title="Text Classification API",
    description="Extract structured data (ZIP, brand, category, time preference) from free text",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Text Classification API is running",
        "endpoints": {
            "classify": "/classify",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.post("/classify", response_model=ClassifyResponse)
async def classify_text(request: ClassifyRequest) -> ClassifyResponse:
    """
    Extract structured information from free text.
    
    Args:
        request: ClassifyRequest containing text to analyze
        
    Returns:
        ClassifyResponse with extracted zip, brand, category, and time_pref
        
    Example:
        ```
        POST /classify
        {
            "text": "I need Nike shoes delivered to 10001 tomorrow evening"
        }
        
        Response:
        {
            "zip": "10001",
            "brand": "Nike",
            "category": "shoes",
            "time_pref": "tomorrow evening"
        }
        ```
    """
    try:
        result = await classifier.classify(request.text)
        return ClassifyResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "openai_enabled": classifier.client is not None,
        "service": "text-classifier"
    }

