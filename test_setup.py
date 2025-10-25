"""
Test script to validate the event scraping agent setup.
"""
import sys
import os

# Add the current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported."""
    try:
        import requests
        import json
        from bs4 import BeautifulSoup
        import google.generativeai as genai
        from dotenv import load_dotenv
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment setup."""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found - you'll need to create one from .env.template")
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key and api_key != 'your_google_api_key_here':
        print("✅ Google Gemini API key configured")
    else:
        print("⚠️  Google Gemini API key not configured - add it to .env file")

def test_basic_scraping():
    """Test basic web scraping functionality."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Test with a simple HTTP request
        response = requests.get('https://httpbin.org/html', timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.find('h1'):
            print("✅ Web scraping test successful")
            return True
        else:
            print("❌ Web scraping test failed")
            return False
    except Exception as e:
        print(f"❌ Web scraping test error: {e}")
        return False

def main():
    """Run all tests."""
    print("Event Scraping Agent - Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    print("\n1. Testing imports...")
    if not test_imports():
        all_passed = False
    
    print("\n2. Testing environment...")
    test_environment()
    
    print("\n3. Testing web scraping...")
    if not test_basic_scraping():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All core tests passed! The agent should work.")
    else:
        print("❌ Some tests failed. Please check the setup.")
    
    print("\nNext steps:")
    print("1. Copy .env.template to .env and add your Google Gemini API key")
    print("2. Test the agent with: python app.py")

if __name__ == "__main__":
    main()