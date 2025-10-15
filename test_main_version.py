"""Test the main version of the API"""
import http.client
import json
import time
import sys

def test_api(text, description):
    """Test the API with given text"""
    print(f"\n{'='*70}")
    print(f"Test: {description}")
    print(f"{'='*70}")
    print(f"Input:  {text}")
    
    try:
        conn = http.client.HTTPConnection("localhost", 8001)
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"text": text})
        
        conn.request("POST", "/classify", body, headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read().decode()
            result = json.loads(data)
            print(f"Output: {json.dumps(result, indent=2)}")
        else:
            print(f"Error: {response.status} {response.reason}")
            
        conn.close()
    except ConnectionRefusedError:
        print("❌ Error: Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True

def main():
    """Run all tests"""
    print("="*70)
    print("TEXT CLASSIFICATION API - MAIN VERSION TESTING")
    print("="*70)
    
    # Check if server is running
    time.sleep(2)  # Wait for server to start
    try:
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("GET", "/health")
        response = conn.getresponse()
        health_data = json.loads(response.read().decode())
        conn.close()
        print(f"✓ Server is running")
        print(f"  Status: {health_data.get('status')}")
        print(f"  OpenAI enabled: {health_data.get('openai_enabled')}\n")
    except Exception as e:
        print(f"❌ Server is not running: {e}")
        sys.exit(1)
    
    # Extended test cases with more complex scenarios
    test_cases = [
        # Basic tests
        ("Nike shoes to 10001 tomorrow evening", 
         "Basic example with all fields"),
        
        ("Send Samsung phone to 90210 this afternoon", 
         "Electronics with time preference"),
        
        # Brand variations
        ("I need ADIDAS sneakers delivered", 
         "Uppercase brand name"),
        
        ("Looking for sony playstation 5", 
         "Lowercase brand with product detail"),
        
        # Complex addresses
        ("Ship to 10001-1234 extended ZIP format", 
         "Extended ZIP code format (9 digits)"),
        
        ("Deliver to M5H 2N2 Canadian address", 
         "Canadian postal code"),
        
        # Multiple time references
        ("Need it tomorrow morning before 9:00 AM", 
         "Multiple time indicators"),
        
        ("Deliver this afternoon or evening", 
         "Multiple time options"),
        
        # Category edge cases
        ("Apple MacBook Pro laptop for development", 
         "Brand + detailed product name"),
        
        ("Nike Air Jordan basketball sneakers", 
         "Brand + specific product line"),
        
        # Business scenarios
        ("Corporate order: 50 Dell laptops to office at 60601", 
         "Bulk order with business context"),
        
        ("Return Zara dress, shipping to 10002", 
         "Return scenario"),
        
        # Ambiguous cases
        ("Target shoes", 
         "Ambiguous - Target as store or verb?"),
        
        ("Apple store visit", 
         "Brand + location visit (not delivery)"),
        
        # Missing information scenarios
        ("Just looking for shoes", 
         "Only category, no other info"),
        
        ("Deliver to 10001", 
         "Only ZIP code"),
        
        ("Nike tomorrow", 
         "Only brand and time"),
        
        # Special characters and formatting
        ("Nike shoes @ 10001 - tomorrow!!!", 
         "Special characters"),
        
        ("📦 Samsung phone -> 90210 ASAP 🚀", 
         "With emojis"),
        
        # Natural language variations
        ("Can you please deliver Nike shoes to my apartment at 10001 tomorrow evening?", 
         "Polite, long form request"),
        
        ("I'm in urgent need of a Samsung phone, address is 90210, need it this afternoon", 
         "Conversational style"),
        
        # Multiple products
        ("Nike shoes and Adidas shirt to 10001", 
         "Multiple brands (should pick first)"),
        
        ("Need laptop and phone delivered", 
         "Multiple categories"),
        
        # Price mentions
        ("$200 Nike shoes to 10001", 
         "Price included in text"),
        
        # Time duration formats
        ("Deliver in 2 hours to 10001", 
         "Time as duration"),
        
        ("Need it within 24 hours", 
         "Specific hour duration"),
        
        # Weekend/holiday references
        ("Deliver next Monday morning", 
         "Specific day of week"),
        
        ("Need it before Christmas", 
         "Holiday reference"),
        
        # Negative cases (minimal/no information)
        ("Hello", 
         "No relevant information"),
        
        ("What can you deliver?", 
         "Question, no specific request"),
        
        ("", 
         "Empty string"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for text, description in test_cases:
        if test_api(text, description):
            success_count += 1
        time.sleep(0.3)  # Small delay between requests
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total tests:  {total_count}")
    print(f"Successful:   {success_count}")
    print(f"Failed:       {total_count - success_count}")
    print(f"Success rate: {(success_count/total_count)*100:.1f}%")
    print(f"{'='*70}")
    
    # Test root endpoint
    print(f"\n{'='*70}")
    print("TESTING ROOT ENDPOINT")
    print(f"{'='*70}")
    try:
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("GET", "/")
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

