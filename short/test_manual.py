"""Manual testing script using built-in libraries"""
import http.client
import json
import subprocess
import time
import sys

def test_api(text, description):
    """Test the API with given text"""
    print(f"\n{'='*70}")
    print(f"Test: {description}")
    print(f"{'='*70}")
    print(f"Input:  {text}")
    
    try:
        conn = http.client.HTTPConnection("localhost", 8000)
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
        print("Server is not running!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True

def main():
    """Run all tests"""
    print("="*70)
    print("TEXT CLASSIFICATION API - REAL DATA TESTING")
    print("="*70)
    
    # Check if server is running, if not - try to start it
    try:
        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", "/")
        response = conn.getresponse()
        conn.close()
        print("✓ Server is running\n")
    except:
        print("Starting server...")
        # Try to start server in background
        try:
            subprocess.Popen(
                ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd="/Volumes/FilinSky/PROJECTS/JSON/short",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Waiting for server to start...")
            time.sleep(3)
        except Exception as e:
            print(f"Failed to start server: {e}")
            print("\nPlease start the server manually:")
            print("cd /Volumes/FilinSky/PROJECTS/JSON/short")
            print("uvicorn app:app --host 0.0.0.0 --port 8000")
            sys.exit(1)
    
    # Test cases with real-world examples
    test_cases = [
        # E-commerce examples
        ("Nike shoes to 10001 tomorrow evening", 
         "E-commerce: Shoes delivery with ZIP and time"),
        
        ("Send Samsung phone to 90210 this afternoon", 
         "Electronics: Phone with famous ZIP code"),
        
        ("Order Adidas sneakers to ZIP code 12345 ASAP",
         "Urgent delivery with explicit ZIP mention"),
        
        ("I need Apple laptop delivered to 94102 next week",
         "Tech product with specific timeframe"),
        
        # Food delivery examples
        ("Starbucks coffee to 60601 today at 3:30 PM",
         "Food delivery with specific time"),
        
        ("Pizza from Domino's to 78701 tonight",
         "Food delivery with evening preference"),
        
        ("Need burger delivered to 10002 in 30 minutes",
         "Fast food with time duration"),
        
        # Clothing examples
        ("Zara dress to 33101 tomorrow morning",
         "Clothing with morning delivery"),
        
        ("Gucci shirt to 94103 this weekend",
         "Luxury brand with weekend delivery"),
        
        # Furniture examples
        ("IKEA chair to 02101 next Monday",
         "Furniture with specific day"),
        
        ("Sofa delivery to 98101 in 2 days",
         "Furniture with time duration"),
        
        # Edge cases
        ("Looking for something",
         "Minimal information - all fields empty"),
        
        ("Microsoft Surface Pro tablet 90210",
         "Missing time preference"),
        
        ("Delivery to 10001 tomorrow",
         "Missing brand and category"),
        
        ("Apple watch",
         "Only brand, no location or time"),
        
        # Complex examples
        ("I want Nike Air Max sneakers delivered to my office at 10001 tomorrow afternoon",
         "Complex sentence with all information"),
        
        ("Can you ship Sony TV to ZIP 33133 as soon as possible? Need it urgently!",
         "Complex request with urgency"),
        
        ("HP laptop for work, address is 02134, need it by Friday",
         "Business context with day-specific delivery"),
        
        # International formats (should handle gracefully)
        ("Apple iPhone to M5H 2N2 tomorrow",
         "Canadian postal code format"),
        
        ("Dell computer to SW1A 1AA next week",
         "UK postcode format"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for text, description in test_cases:
        if test_api(text, description):
            success_count += 1
        time.sleep(0.5)  # Small delay between requests
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total tests:  {total_count}")
    print(f"Successful:   {success_count}")
    print(f"Failed:       {total_count - success_count}")
    print(f"Success rate: {(success_count/total_count)*100:.1f}%")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()

