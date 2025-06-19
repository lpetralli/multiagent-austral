# Multi-Agent Austral

This project implements a multi-agent system for Universidad Austral using LangGraph and various webhook integrations.

## Environment Setup


### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multiagent-austral
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# LangChain/OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=multiagent-austral

# Optional: Other API keys if needed
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Adding New Tools

To add new tools following the pattern in `tools.py`, follow these steps:

### 1. Define a Pydantic Model

First, create a Pydantic model for your tool's input data:

```python
from pydantic import BaseModel
from typing import Literal

class YourToolInput(BaseModel):
    field1: str
    field2: int
    field3: Literal["option1", "option2"]  # For restricted values
```

### 2. Create the Tool Function

Use the `@tool` decorator from langchain_core.tools:

```python
from langchain_core.tools import tool
from typing import Dict, Any
import requests

@tool
def your_tool_name(
    field1: str,
    field2: int,
    field3: Literal["option1", "option2"]
) -> Dict[Any, Any]:
    """
    Clear description of what this tool does.
    
    Args:
        field1: Description of field1
        field2: Description of field2
        field3: Description of field3 with possible values
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "your_webhook_url_here"
    
    try:
        # Validate data with Pydantic model
        payload = YourToolInput(
            field1=field1,
            field2=field2,
            field3=field3
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }
```

### 3. Add Tool to Agent

In `agent.py`, import and add your new tool to the tools list:

```python
from tools import your_tool_name

# In the agent configuration
tools = [
    # ... existing tools
    your_tool_name
]
```

## Creating Make Webhooks

Make (formerly Integromat) is used for webhook automation. Here's how to create webhooks:

### 1. Create a New Scenario in Make

1. Log in to [Make.com](https://www.make.com)
2. Click "Create a new scenario"
3. Add a "Webhooks" module as the trigger

### 2. Configure the Webhook

1. Select "Custom webhook" as the webhook type
2. Click "Add" to create a new webhook
3. Give it a descriptive name (e.g., "Process Employee Learning Status")
4. Copy the generated webhook URL

### 3. Set Up Data Structure

1. In the webhook settings, define the expected data structure
2. You can send a test request with sample data to auto-detect the structure
3. Or manually define fields matching your Pydantic model

### 4. Add Processing Modules

Common modules to add after the webhook:
- **Google Sheets**: Read/write data
- **Email**: Send notifications
- **HTTP**: Make API calls
- **Data Store**: Store/retrieve data
- **Text Parser**: Process text data
- **Router**: Add conditional logic

### 5. Example Webhook Flow

```
Webhook → Filter (validate data) → Google Sheets (update) → Email (notify) → Response
```

### 6. Test Your Webhook

Use the tool in your Python code or send a test request:

```python
import requests

test_data = {
    "field1": "value1",
    "field2": 123,
    "field3": "option1"
}

response = requests.post(
    "https://hook.us1.make.com/your_webhook_id",
    json=test_data
)
print(response.text)
```

## Running the Streamlit App

Run the Streamlit chat application:

```bash
streamlit run chat.py
```

This will:
- Start a local server 
- Open your default browser automatically
- Display the chat interface
