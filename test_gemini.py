"""
Test script to verify Google Gemini integration with event extraction.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import EventScrapingAgent

def test_gemini_with_mock_content():
    """Test Gemini with mock event content."""
    
    agent = EventScrapingAgent()
    
    # Mock content that clearly contains event information
    mock_content = {
        "https://mock-events.com": """
        Upcoming Events:
        
        Tech Summit 2025
        Date: December 15, 2025
        Time: 9:00 AM - 5:00 PM
        Location: San Francisco Convention Center
        Description: Annual technology conference featuring AI, blockchain, and cloud computing innovations.
        
        Python Workshop for Beginners
        Date: January 10, 2026
        Time: 2:00 PM - 4:00 PM  
        Location: Local Library Meeting Room A
        Description: Learn Python programming basics in this hands-on workshop.
        
        Web Development Bootcamp
        Date: February 20, 2026
        Time: 10:00 AM - 6:00 PM
        Location: Online Virtual Event
        Description: Intensive one-day bootcamp covering HTML, CSS, JavaScript and React.
        """
    }
    
    print("Testing Gemini with mock event content...")
    print("=" * 50)
    
    # Extract events using Gemini
    events = agent.extract_events_with_gemini(mock_content)
    
    print(f"✅ Gemini extracted {len(events)} events:")
    print("=" * 50)
    
    for i, event in enumerate(events, 1):
        print(f"\nEvent {i}:")
        print(f"  Title: {event.get('title', 'N/A')}")
        print(f"  Date: {event.get('start_date', 'N/A')}")
        print(f"  Time: {event.get('start_time', 'N/A')}")
        print(f"  Location: {event.get('location', 'N/A')}")
        print(f"  Description: {event.get('description', 'N/A')}")
    
    return events

if __name__ == "__main__":
    print("Google Gemini Integration Test")
    print("=" * 50)
    
    try:
        events = test_gemini_with_mock_content()
        
        if events:
            print(f"\n🎉 Success! Gemini successfully extracted {len(events)} events")
        else:
            print("\n⚠️  No events extracted - this might be normal if the content doesn't contain clear event information")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("This might indicate an API issue or network problem.")