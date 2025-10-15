"""Quick test examples"""
import requests

API_URL = "http://localhost:8000/classify"

test_cases = [
    "Nike shoes to 10001 tomorrow evening",
    "Send Samsung phone to 90210 this afternoon",
    "Apple laptop delivery next week",
    "Adidas sneakers ASAP",
]

for text in test_cases:
    try:
        response = requests.post(API_URL, json={"text": text})
        print(f"\nInput:  {text}")
        print(f"Output: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure server is running: uvicorn app:app --reload")
        break

