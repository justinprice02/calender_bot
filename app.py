import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import logging
from datetime import datetime
import re
from mcp_calendar import MCPCalendarManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EventScrapingAgent:
    """
    An orchestrated agent that scrapes webpages for events, processes them with Claude API,
    and adds them to Google Calendar using MCP.
    """
    
    def __init__(self):
        """Initialize the agent with API credentials."""
        # Configure Google Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.gemini_model = None
            logger.warning("No Google API key found. Agent will run in demo mode.")
        
        self.calendar_manager = MCPCalendarManager()
        
    def scrape_webpage(self, url: str) -> str:
        """
        Scrape content from a webpage.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            str: The scraped text content
        """
        try:
            logger.info(f"Scraping webpage: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            logger.info(f"Successfully scraped {len(text)} characters from {url}")
            return text
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return f"Error scraping {url}: {str(e)}"
    
    def scrape_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """
        Scrape content from multiple webpages.
        
        Args:
            urls (List[str]): List of URLs to scrape
            
        Returns:
            Dict[str, str]: Dictionary mapping URLs to their scraped content
        """
        scraped_data = {}
        
        for url in urls:
            scraped_data[url] = self.scrape_webpage(url)
        
        return scraped_data
    
    def extract_events_with_gemini(self, scraped_content: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Use Google Gemini API to extract event information from scraped content.
        
        Args:
            scraped_content (Dict[str, str]): Dictionary of URL -> content mappings
            
        Returns:
            List[Dict[str, Any]]: List of extracted events in structured format
        """
        try:
            if not self.gemini_model:
                logger.warning("Gemini model not initialized. Running in demo mode.")
                return self._generate_demo_events(scraped_content)
            
            logger.info("Processing content with Google Gemini API")
            
            # Prepare the content for Gemini
            combined_content = ""
            for url, content in scraped_content.items():
                combined_content += f"\n\n--- Content from {url} ---\n"
                combined_content += content[:8000]  # Limit content length to avoid token limits
            
            prompt = f"""
Please analyze the following scraped web content and extract any events you find. 
Look for information like concerts, conferences, workshops, meetings, webinars, or any other scheduled events.

For each event found, extract the following information and return it as a JSON array:

Required fields:
- title: Event title/name
- start_date: Start date in ISO format (YYYY-MM-DD)
- start_time: Start time (if available, in HH:MM format)
- end_date: End date in ISO format (YYYY-MM-DD, same as start_date if single day)
- end_time: End time (if available, in HH:MM format)

Optional fields:
- description: Brief description of the event
- location: Venue or location information
- url: Original URL where this event was found
- organizer: Event organizer or host

Return ONLY a valid JSON array. If no events are found, return an empty array [].

Content to analyze:
{combined_content}
"""

            response = self.gemini_model.generate_content(prompt)
            
            # Extract JSON from Gemini's response
            response_text = response.text.strip()
            logger.info(f"Gemini response: {response_text[:200]}...")
            
            # Try to extract JSON from the response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                events = json.loads(json_str)
                logger.info(f"Extracted {len(events)} events from Gemini response")
                return events
            else:
                logger.warning("No JSON array found in Gemini response")
                logger.warning(f"Full response: {response_text}")
                return []
                
        except Exception as e:
            logger.error(f"Error processing content with Gemini: {str(e)}")
            return []
    
    def _generate_demo_events(self, scraped_content: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Generate demo events when API is not available.
        """
        logger.info("Generating demo events (API not available)")
        if scraped_content and any(len(content) > 100 for content in scraped_content.values()):
            return [
                {
                    "title": "Sample Event from Scraped Content",
                    "start_date": "2025-11-15",
                    "start_time": "14:00",
                    "end_date": "2025-11-15", 
                    "end_time": "16:00",
                    "description": "This is a sample event extracted from the scraped content",
                    "location": "Online",
                    "url": list(scraped_content.keys())[0]
                }
            ]
        return []
    
    def add_event_to_calendar(self, event: Dict[str, Any]) -> bool:
        """
        Add a single event to Google Calendar using MCP.
        
        Args:
            event (Dict[str, Any]): Event data to add
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"Adding event to calendar: {event.get('title', 'Unknown Event')}")
            
            # Use the MCP calendar manager to add the event
            success = self.calendar_manager.add_event_via_mcp(event)
            
            if success:
                logger.info(f"Successfully added event: {event.get('title')}")
            else:
                logger.error(f"Failed to add event: {event.get('title')}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error adding event to calendar: {str(e)}")
            return False
    
    def process_events(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Process and add multiple events to the calendar.
        
        Args:
            events (List[Dict[str, Any]]): List of events to process
            
        Returns:
            Dict[str, int]: Summary of processing results
        """
        results = {"successful": 0, "failed": 0}
        
        for event in events:
            if self.add_event_to_calendar(event):
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def run_agent(self, urls: List[str]) -> Dict[str, Any]:
        """
        Main orchestration method that runs the complete agent workflow.
        
        Args:
            urls (List[str]): List of URLs to scrape for events
            
        Returns:
            Dict[str, Any]: Summary of the complete operation
        """
        logger.info(f"Starting agent workflow with {len(urls)} URLs")
        
        # Step 1: Scrape webpages
        scraped_content = self.scrape_multiple_pages(urls)
        logger.info(f"Scraped content from {len(scraped_content)} pages")
        
        # Step 2: Extract events using Gemini
        events = self.extract_events_with_gemini(scraped_content)
        logger.info(f"Extracted {len(events)} events")
        
        # Step 3: Add events to calendar
        results = self.process_events(events)
        
        # Prepare summary
        summary = {
            "urls_processed": len(urls),
            "events_found": len(events),
            "events_added_successfully": results["successful"],
            "events_failed": results["failed"],
            "extracted_events": events
        }
        
        logger.info(f"Agent workflow completed: {summary}")
        return summary


def main():
    """
    Main function to run the event scraping agent.
    """
    # Example usage
    agent = EventScrapingAgent()
    
    # Example URLs - replace with actual event websites
    example_urls = [
        "https://example.com/events",
        "https://another-site.com/calendar",
        # Add more URLs here
    ]
    
    print("Event Scraping Agent")
    print("===================")
    
    # Get URLs from user input or use examples
    urls_input = input("Enter URLs separated by commas (or press Enter to use examples): ").strip()
    
    if urls_input:
        urls = [url.strip() for url in urls_input.split(",")]
    else:
        urls = example_urls
        print("Using example URLs...")
    
    if not urls:
        print("No URLs provided. Exiting...")
        return
    
    print(f"\nProcessing {len(urls)} URLs...")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
    
    # Run the agent
    try:
        summary = agent.run_agent(urls)
        
        print("\n" + "="*50)
        print("AGENT EXECUTION SUMMARY")
        print("="*50)
        print(f"URLs processed: {summary['urls_processed']}")
        print(f"Events found: {summary['events_found']}")
        print(f"Events added successfully: {summary['events_added_successfully']}")
        print(f"Events failed: {summary['events_failed']}")
        
        if summary['extracted_events']:
            print("\nExtracted Events:")
            print("-" * 20)
            for i, event in enumerate(summary['extracted_events'], 1):
                print(f"\n{i}. {event.get('title', 'Unknown Event')}")
                print(f"   Date: {event.get('start_date', 'N/A')}")
                print(f"   Time: {event.get('start_time', 'N/A')}")
                print(f"   Location: {event.get('location', 'N/A')}")
    
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()