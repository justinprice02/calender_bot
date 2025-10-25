"""
Demo script to showcase the Event Scraping Agent functionality without requiring API keys.
This script demonstrates the web scraping and event processing pipeline.
"""

import json
import os
import sys
from typing import List, Dict, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import EventScrapingAgent
from mcp_calendar import MCPCalendarManager

class DemoEventScrapingAgent(EventScrapingAgent):
    """
    Demo version of the Event Scraping Agent that works without API keys.
    """
    
    def __init__(self):
        """Initialize without requiring Anthropic API key."""
        self.calendar_manager = MCPCalendarManager()
        # Skip Anthropic client initialization for demo
        self.anthropic_client = None
    
    def extract_events_with_gemini(self, scraped_content: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Demo version that returns mock events instead of calling Gemini API.
        """
        print("🔄 Demo Mode: Simulating Gemini API event extraction...")
        
        # Mock events based on common event patterns
        mock_events = [
            {
                "title": "Tech Conference 2024",
                "start_date": "2024-03-15",
                "start_time": "09:00",
                "end_date": "2024-03-15",
                "end_time": "17:00",
                "description": "Annual technology conference featuring the latest innovations",
                "location": "Convention Center, Downtown",
                "url": list(scraped_content.keys())[0] if scraped_content else "demo"
            },
            {
                "title": "Workshop: Python for Beginners",
                "start_date": "2024-03-20",
                "start_time": "14:00",
                "end_date": "2024-03-20",
                "end_time": "16:00",
                "description": "Learn Python programming from scratch",
                "location": "Library Meeting Room",
                "url": list(scraped_content.keys())[0] if scraped_content else "demo"
            }
        ]
        
        # Only return events if we actually scraped content
        if scraped_content and any(len(content) > 100 for content in scraped_content.values()):
            print(f"✅ Mock extraction: Found {len(mock_events)} events")
            return mock_events
        else:
            print("⚠️  No substantial content found in scraped pages")
            return []


def demo_scraping():
    """
    Demonstrate the web scraping functionality.
    """
    print("🌐 Web Scraping Demo")
    print("=" * 40)
    
    agent = DemoEventScrapingAgent()
    
    # Test URLs that are likely to have content
    test_urls = [
        "https://httpbin.org/html",  # Simple test page
        "https://example.com"        # Basic webpage
    ]
    
    print(f"Testing scraping with {len(test_urls)} URLs:")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    
    # Test scraping
    scraped_data = agent.scrape_multiple_pages(test_urls)
    
    print(f"\n📊 Scraping Results:")
    for url, content in scraped_data.items():
        content_length = len(content) if content else 0
        status = "✅ Success" if content_length > 0 else "❌ Failed"
        print(f"  {url}: {status} ({content_length} chars)")
    
    return scraped_data


def demo_full_workflow():
    """
    Demonstrate the complete agent workflow.
    """
    print("\n🤖 Full Agent Workflow Demo")
    print("=" * 40)
    
    agent = DemoEventScrapingAgent()
    
    # Use the same test URLs
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com"
    ]
    
    # Run the full workflow
    results = agent.run_agent(test_urls)
    
    # Display results
    print(f"\n📋 Workflow Results:")
    print(f"  URLs processed: {results['urls_processed']}")
    print(f"  Events found: {results['events_found']}")
    print(f"  Events added successfully: {results['events_added_successfully']}")
    print(f"  Events failed: {results['events_failed']}")
    
    if results['extracted_events']:
        print(f"\n📅 Extracted Events:")
        for i, event in enumerate(results['extracted_events'], 1):
            print(f"\n  Event {i}:")
            print(f"    Title: {event.get('title')}")
            print(f"    Date: {event.get('start_date')} at {event.get('start_time', 'All day')}")
            print(f"    Location: {event.get('location', 'Not specified')}")
            print(f"    Description: {event.get('description', 'No description')}")
    
    return results


def demo_mcp_calendar():
    """
    Demonstrate MCP calendar integration.
    """
    print("\n📅 MCP Calendar Demo")
    print("=" * 40)
    
    manager = MCPCalendarManager()
    
    # Test event
    test_event = {
        "title": "Demo Event",
        "start_date": "2024-04-01",
        "start_time": "10:00",
        "end_time": "11:00",
        "description": "This is a demonstration event",
        "location": "Virtual Meeting",
        "url": "https://demo.com/event"
    }
    
    print("Testing MCP calendar integration with demo event:")
    print(f"  Title: {test_event['title']}")
    print(f"  Date/Time: {test_event['start_date']} {test_event['start_time']}-{test_event['end_time']}")
    
    success = manager.add_event_via_mcp(test_event)
    
    if success:
        print("✅ MCP calendar integration test successful")
    else:
        print("❌ MCP calendar integration test failed")
    
    return success


def main():
    """
    Main demo function.
    """
    print("Event Scraping Agent - Demo Mode")
    print("=" * 50)
    print("This demo showcases the agent's functionality without requiring API keys.\n")
    
    try:
        # Demo 1: Web scraping
        scraped_data = demo_scraping()
        
        # Demo 2: MCP calendar
        demo_mcp_calendar()
        
        # Demo 3: Full workflow
        workflow_results = demo_full_workflow()
        
        print("\n" + "=" * 50)
        print("🎉 Demo Complete!")
        print("=" * 50)
        
        print("\nTo use the agent with real data:")
        print("1. The Google Gemini API key is already configured")
        print("2. Configure MCP server for Google Calendar integration")
        print("3. Run: python app.py")
        print("4. To test Gemini extraction: python test_gemini.py")
        print("\nFor more information, see README.md")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This might be due to network connectivity or other issues.")


if __name__ == "__main__":
    main()