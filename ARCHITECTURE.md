# Architecture & Design Decisions

## Overview
This project implements a production-ready text classification API with a focus on maintainability, scalability, and intelligent fallback mechanisms.

## Key Design Principles

### 1. Separation of Concerns
- **Models** (`app/models.py`): Data validation and schema definitions using Pydantic
- **Configuration** (`app/config.py`): Centralized settings management
- **Business Logic** (`app/classifier.py`): Text extraction algorithms
- **API Layer** (`app/main.py`): HTTP endpoints and request handling

### 2. Dual Extraction Strategy

#### Primary: OpenAI-based Extraction
- Uses GPT models for intelligent, context-aware extraction
- Handles natural language variations and complex patterns
- Requires API key but provides superior accuracy

#### Fallback: Pattern Matching
- Regex-based extraction for common patterns
- Works offline without external dependencies
- Ensures system always responds, even without OpenAI

**Benefits:**
- Graceful degradation
- Cost optimization (can disable OpenAI if budget constrained)
- Development flexibility (no API key needed for local testing)

### 3. Data Validation
- **Request Validation**: Pydantic ensures incoming data is valid
- **Response Consistency**: All responses follow strict schema
- **Type Safety**: Full type hints throughout codebase
- **Optional Fields**: Returns `null` for missing data instead of errors

### 4. Error Handling
- Try-catch blocks prevent service crashes
- Automatic fallback on OpenAI failures
- HTTP 500 with descriptive errors for debugging
- Health check endpoint for monitoring

### 5. Scalability Considerations

#### Current Implementation
- Async/await for non-blocking operations
- FastAPI's built-in async support
- Stateless design (can scale horizontally)

#### Future Enhancements
- Redis caching for repeated queries
- Database for request logging/analytics
- Rate limiting for API protection
- Batch processing endpoint

### 6. Development Experience
- Interactive API docs (Swagger/ReDoc)
- Type hints for IDE autocomplete
- Example test suite
- Docker support for consistent environments
- Environment-based configuration

## Technology Choices

### FastAPI
**Why:** Modern, fast, async-native Python framework
- Auto-generated OpenAPI documentation
- Native Pydantic integration
- Excellent performance
- Easy to learn and maintain

### Pydantic
**Why:** Data validation and settings management
- Automatic validation
- JSON schema generation
- Environment variable parsing
- Type safety

### OpenAI API
**Why:** State-of-the-art language understanding
- Best-in-class NER (Named Entity Recognition)
- Handles ambiguous cases
- Minimal training required
- Production-ready

## Code Quality Standards

### 1. Type Hints
All functions have type annotations for better IDE support and documentation.

### 2. Docstrings
Public APIs documented with clear descriptions, parameters, and return types.

### 3. Configuration
Environment variables for secrets and settings (never hardcoded).

### 4. Single Responsibility
Each module has one clear purpose.

### 5. DRY (Don't Repeat Yourself)
Shared logic centralized in classifier service.

## Security Considerations

1. **API Key Protection**: Environment variables, never committed
2. **Input Validation**: Pydantic prevents injection attacks
3. **CORS Configuration**: Configurable for production
4. **Error Messages**: No sensitive data in error responses
5. **Rate Limiting**: Recommended for production (not implemented in MVP)

## Performance Optimizations

### Current
- Async operations for I/O
- Singleton classifier instance (reuses OpenAI client)
- Minimal dependencies

### Recommended for Production
- Response caching (Redis)
- Connection pooling for OpenAI API
- Request batching
- Monitoring and logging (Prometheus/Grafana)
- Load balancing

## Testing Strategy

### Included
- Example test suite (`test_examples.py`)
- Health check endpoint
- Interactive docs for manual testing

### Recommended Additions
- Unit tests (pytest)
- Integration tests
- Load testing (Locust)
- CI/CD pipeline

## Deployment Options

### Development
```bash
uvicorn main:app --reload
```

### Production
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker
```bash
docker-compose up
```

### Cloud Platforms
- AWS Lambda + API Gateway (serverless)
- Google Cloud Run (containers)
- Heroku (PaaS)
- Kubernetes (orchestration)

## Monitoring Recommendations

1. **Health Checks**: `/health` endpoint for uptime monitoring
2. **Metrics**: Response times, success rates, OpenAI vs pattern-matching usage
3. **Logging**: Structured logs for debugging
4. **Alerting**: Notify on high error rates or slow responses

## Future Enhancements

### Short Term
- Add more brands and categories
- Improve time parsing (relative dates)
- Support international address formats
- Request/response logging

### Medium Term
- Machine learning model training on labeled data
- Caching layer for common queries
- Analytics dashboard
- Multi-language support

### Long Term
- Fine-tuned model specific to domain
- Real-time learning from corrections
- A/B testing framework
- Webhook notifications

## Conclusion

This architecture balances:
- **Simplicity**: Easy to understand and maintain
- **Robustness**: Fallback mechanisms and error handling
- **Flexibility**: Easy to extend and configure
- **Performance**: Async operations and efficient patterns
- **Quality**: Type safety, validation, documentation

The design allows rapid development while maintaining production-readiness.

