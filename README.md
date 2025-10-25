# Event Scraping Agent

An intelligent Python agent that scrapes webpages for events, processes them with Claude API, and adds them to Google Calendar using MCP (Model Context Protocol).

## Features

- **Web Scraping**: Automatically scrapes multiple webpages for event information
- **AI Processing**: Uses Google Gemini API to intelligently extract structured event data
- **Calendar Integration**: Adds events to Google Calendar via MCP server
- **Robust Error Handling**: Comprehensive logging and error management
- **Flexible Configuration**: Environment-based configuration system

## Setup

### 1. Environment Setup

1. Ensure Python 3.12+ is installed
2. Create a virtual environment (already done if using VS Code workspace)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Configuration

1. Copy the environment template:
   ```bash
   copy .env.template .env
   ```
   
2. Edit `.env` and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. Get your Google Gemini API key from: https://aistudio.google.com/app/apikey

### 3. MCP Server Setup

The agent is designed to work with Google Calendar MCP server. To set up MCP integration:

1. Ensure your MCP server is configured for Google Calendar
2. Update the `mcp_calendar.py` file with your specific MCP server details
3. Replace the `_simulate_mcp_call` method with actual MCP integration

## Usage

### Quick Test

Run the setup test to verify everything is working:
```bash
python test_setup.py
```

### Basic Usage

Run the agent with interactive prompts:
```bash
python app.py
```

### Programmatic Usage

```python
from app import EventScrapingAgent

# Initialize the agent
agent = EventScrapingAgent()

# Define URLs to scrape
urls = [
    "https://example.com/events",
    "https://another-site.com/calendar"
]

# Run the agent
results = agent.run_agent(urls)

print(f"Found {results['events_found']} events")
print(f"Added {results['events_added_successfully']} events to calendar")
```

## File Structure

```
calender_bot/
├── app.py              # Main agent application
├── mcp_calendar.py     # MCP Google Calendar integration
├── test_setup.py       # Setup validation script
├── requirements.txt    # Python dependencies
├── .env.template      # Environment variables template
├── .env              # Your environment variables (create this)
└── README.md         # This file
```

## How It Works

1. **Web Scraping**: The agent scrapes content from provided URLs using BeautifulSoup
2. **Content Processing**: Scraped content is sent to Google Gemini API with a specialized prompt
3. **Event Extraction**: Gemini returns structured JSON with event details
4. **Calendar Integration**: Events are formatted and added to Google Calendar via MCP

## Event Data Structure

The agent extracts events with the following structure:

```json
{
  "title": "Event Name",
  "start_date": "2024-01-15",
  "start_time": "14:00",
  "end_date": "2024-01-15",
  "end_time": "15:00",
  "description": "Event description",
  "location": "Event location",
  "url": "https://source-url.com"
}
```

## MCP Integration

### Current Status
The MCP integration is set up with a simulation layer. To enable real Google Calendar integration:

1. Ensure your workspace has a Google Calendar MCP server configured
2. Update `mcp_calendar.py` with your specific MCP server details
3. Replace the simulation methods with actual MCP calls

### Example MCP Integration
```python
# In mcp_calendar.py, replace _simulate_mcp_call with:
def _real_mcp_call(self, gcal_event):
    # Your MCP server integration here
    # This depends on your specific MCP setup
    pass
```

## Troubleshooting

### Import Errors
If you see import errors in VS Code:
1. Ensure the Python environment is properly selected
2. Run `python test_setup.py` to verify package installation
3. Restart VS Code if needed

### API Issues
- Verify your Google Gemini API key is correct
- Check your internet connection
- Ensure you have API quotas available

### MCP Issues
- Verify MCP server is running
- Check MCP server configuration
- Test MCP server independently

## Configuration Options

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

### Agent Parameters
You can customize the agent behavior by modifying:
- Scraping timeout settings
- Claude model selection
- Event validation rules
- Calendar formatting options

## Example Websites to Test

Try the agent with these types of websites:
- Event listing pages
- Conference websites  
- Meetup pages
- University event calendars
- Community center schedules

## Contributing

To extend the agent:
1. Add new scrapers for specific websites in `app.py`
- Enhance event extraction prompts for better Gemini accuracy
3. Add support for additional calendar systems
4. Improve error handling and recovery

## License

This project is open source. Modify and use as needed for your requirements.