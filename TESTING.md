# Testing Guide

This document describes how to run comprehensive tests for the Text Classification API.

## Prerequisites

```bash
# Install dependencies (if not already installed)
pip3 install --user --break-system-packages fastapi uvicorn pydantic requests openai python-dotenv pydantic-settings httpx
```

## Quick Test

Run this command to see the test summary:
```bash
python3 test_summary.py
```

## Test Short Version

The short version is a lightweight implementation using only pattern matching.

### Start Server
```bash
cd short/
/Users/daniilfilinski/Library/Python/3.13/bin/uvicorn app:app --host 0.0.0.0 --port 8000
```

### Run Tests (in another terminal)
```bash
cd short/
python3 test_manual.py
```

### Expected Results
- Tests: 20
- Success Rate: 100%
- Features: Basic pattern matching for ZIP, brand, category, time preference

## Test Main Version

The main version includes OpenAI integration support and enhanced pattern matching.

### Start Server
```bash
cd /Volumes/FilinSky/PROJECTS/JSON
/Users/daniilfilinski/Library/Python/3.13/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Run Tests (in another terminal)
```bash
python3 test_main_version.py
```

### Expected Results
- Tests: 31
- Success Rate: 100%
- Features: Enhanced pattern matching, OpenAI support (optional), CORS, async

## Test Both Versions Simultaneously

You can run both servers on different ports and test them in parallel:

```bash
# Terminal 1: Short version on port 8000
cd short/ && uvicorn app:app --port 8000

# Terminal 2: Main version on port 8001
cd /Volumes/FilinSky/PROJECTS/JSON && uvicorn app.main:app --port 8001

# Terminal 3: Run tests
python3 test_main_version.py    # Tests main version
cd short/ && python3 test_manual.py  # Tests short version
```

## Test Categories

The test suite covers:

1. **E-commerce Scenarios**
   - Shoe delivery with ZIP and time
   - Electronics orders
   - Clothing and fashion items

2. **Food Delivery**
   - Orders with specific times
   - Different time preferences

3. **Complex Natural Language**
   - Long conversational requests
   - Multiple products in one text
   - Business context

4. **Edge Cases**
   - Missing information
   - Empty fields
   - Invalid inputs

5. **International Formats**
   - US ZIP codes (5 and 9 digit)
   - Canadian postal codes
   - UK postcodes

6. **Time Formats**
   - Relative: "tomorrow", "today", "next week"
   - Specific: "3:30 PM", "9:00 AM"
   - Urgency: "ASAP", "urgent"
   - Duration: "in 30 minutes", "in 2 hours"

## Sample Test Cases

```python
# Example 1: Complete information
Input:  "Nike shoes to 10001 tomorrow evening"
Output: {"zip": "10001", "brand": "Nike", "category": "shoes", "time_pref": "tomorrow"}

# Example 2: Food delivery with time
Input:  "Starbucks coffee to 60601 today at 3:30 PM"
Output: {"zip": "60601", "brand": "Starbucks", "category": "food", "time_pref": "today"}

# Example 3: Urgent delivery
Input:  "Order Adidas sneakers to ZIP code 12345 ASAP"
Output: {"zip": "12345", "brand": "Adidas", "category": "shoes", "time_pref": "asap"}

# Example 4: Corporate order
Input:  "Corporate order: 50 Dell laptops to office at 60601"
Output: {"zip": "60601", "brand": "Dell", "category": "electronics", "time_pref": null}
```

## Manual Testing with curl

You can also test manually using curl:

```bash
# Test short version (port 8000)
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Nike shoes to 10001 tomorrow evening"}'

# Test main version (port 8001)
curl -X POST http://localhost:8001/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Samsung phone to 90210 this afternoon"}'

# Health check
curl http://localhost:8001/health
```

## View Test Results

After running tests, you can view detailed results:

```bash
# View test summary
cat test_results_main.txt | less

# View short version results
cat test_results_short.txt | less

# View detailed report
cat TEST_REPORT.md | less
```

## Interactive Testing

You can use the FastAPI interactive docs:

```bash
# Short version
open http://localhost:8000/docs

# Main version
open http://localhost:8001/docs
```

## Performance Testing

For load testing, you can use tools like Apache Bench or wrk:

```bash
# Install Apache Bench (if needed)
brew install httpd

# Simple load test (100 requests, 10 concurrent)
ab -n 100 -c 10 -p test_payload.json -T application/json http://localhost:8001/classify
```

Create `test_payload.json`:
```json
{"text": "Nike shoes to 10001 tomorrow evening"}
```

## Troubleshooting

### Server won't start
```bash
# Check if port is already in use
lsof -i :8000
lsof -i :8001

# Kill process if needed
kill -9 <PID>
```

### Module not found errors
```bash
# Reinstall dependencies
pip3 install --user --break-system-packages -r requirements.txt
```

### Connection refused
```bash
# Make sure server is running
curl http://localhost:8000/
curl http://localhost:8001/

# Check server logs
# Look at terminal where uvicorn is running
```

## Test Files Structure

```
/
├── test_summary.py           # Visual summary of test results
├── test_main_version.py      # Test script for main version (31 tests)
├── test_results_main.txt     # Full output from main version tests
├── test_results_short.txt    # Full output from short version tests
├── TEST_REPORT.md            # Comprehensive test report
├── TESTING.md                # This file
└── short/
    ├── test.py               # Simple test script
    └── test_manual.py        # Comprehensive test script (20 tests)
```

## CI/CD Integration

To integrate tests into CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: API Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Start server
        run: uvicorn app.main:app --host 0.0.0.0 --port 8001 &
      - name: Wait for server
        run: sleep 5
      - name: Run tests
        run: python3 test_main_version.py
```

## Next Steps

1. ✅ Pattern matching tests - **COMPLETED**
2. ⏭️ Enable OpenAI and test with AI model
3. ⏭️ Load testing with concurrent requests
4. ⏭️ Integration tests with database
5. ⏭️ Security testing (input sanitization, XSS, etc.)

---

**Last Updated**: October 15, 2025  
**Test Coverage**: 51 unique scenarios  
**Success Rate**: 100%

