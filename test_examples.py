"""
Example test cases for the Text Classification API.
Run the API server first: uvicorn main:app --reload
Then run this script: python test_examples.py
"""

import requests
import json


API_URL = "http://localhost:8000"


def test_classify(text: str, description: str):
    """Test a single classification request"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"{'='*60}")
    print(f"Input: {text}")
    
    try:
        response = requests.post(
            f"{API_URL}/classify",
            json={"text": text},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nResult:")
            print(json.dumps(result, indent=2))
        else:
            print(f"\nError: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API. Is the server running?")
        print("Start it with: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run test examples"""
    print("Text Classification API - Test Examples")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "text": "I need Nike shoes delivered to 10001 tomorrow evening",
            "description": "Complete example with all fields"
        },
        {
            "text": "Send Samsung phone to 90210 this afternoon",
            "description": "Electronics with different time preference"
        },
        {
            "text": "Order Adidas sneakers to ZIP code 12345 ASAP",
            "description": "Shoes with urgent delivery"
        },
        {
            "text": "Apple laptop delivery at M5H 2N2 next week",
            "description": "Canadian postal code"
        },
        {
            "text": "I want Starbucks coffee delivered today at 3:30 PM",
            "description": "Food delivery with specific time"
        },
        {
            "text": "Looking for H&M clothing in area 78701",
            "description": "Clothing category"
        },
        {
            "text": "Need furniture delivered to my address",
            "description": "Missing some information"
        },
        {
            "text": "Microsoft Surface Pro tablet to 94102 tomorrow morning",
            "description": "Tech product with morning delivery"
        },
        {
            "text": "Pizza from Domino's to 60601 tonight",
            "description": "Food with evening delivery"
        },
        {
            "text": "Can you ship this book next Monday?",
            "description": "Minimal information"
        }
    ]
    
    # Run tests
    for case in test_cases:
        test_classify(case["text"], case["description"])
    
    # Health check
    print(f"\n{'='*60}")
    print("Health Check")
    print(f"{'='*60}")
    try:
        response = requests.get(f"{API_URL}/health")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\n{'='*60}")
    print("Tests completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

