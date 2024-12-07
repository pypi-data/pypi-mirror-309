# PromptStudio Python SDK

A Python SDK for interacting with PromptStudio API and AI platforms directly.

## Installation

### From PyPI (Coming Soon)

```bash
pip install promptstudio-sdk
```

### From Source

```bash
git clone https://github.com/your-repo/promptstudio-sdk.git
cd promptstudio-sdk
pip install -e .
```

## Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Initializing the SDK

```python
from promptstudio_sdk import PromptStudio

client = PromptStudio({
    'api_key': 'YOUR_API_KEY',
    'env': 'prod',  # Use 'prod' for production environment
    'bypass': True
})
```

### Configuration Options

#### `bypass` (default: `False`)

The `bypass` parameter determines whether to use the local AI provider directly or route requests through PromptStudio's API:

- When `bypass=True`: Requests go directly to the AI provider, bypassing PromptStudio's API
- When `bypass=False`: Requests are routed through PromptStudio's API for additional processing and logging

#### `is_session_enabled` (default: `True`)

The `is_session_enabled` parameter controls whether the chat maintains conversation history:

- When `True`: The conversation history is maintained between requests using the provided `session_id`
- When `False`: Each request is treated independently with no conversation history

Example with explicit configuration:

```python
client = PromptStudio({
    'api_key': 'YOUR_API_KEY',
    'env': 'prod',
    'bypass': False  # Route through PromptStudio API (default)
})

response = client.chat_with_prompt(
    prompt_id="your_prompt_id",
    user_message=[{"type": "text", "text": "Hello"}],
    session_id="test_session",
    is_session_enabled=True  # Enable conversation history (default)
)
```

### Chatting with a Prompt

```python
response = client.chat_with_prompt(
    prompt_id="your_prompt_id",
    user_message=[
        {
            "type": "text",
            "text": "Hello, how are you?"
        }
    ],
    memory_type="fullMemory",
    window_size=0,
    session_id="test_session",
    variables={},
    is_session_enabled=True,
)

print(response)
```

### Complete Example

```python
from promptstudio_sdk import PromptStudio

def main():
    # Initialize the client
    client = PromptStudio({
        'api_key': 'YOUR_API_KEY',
        'env': 'test',
        'bypass': True
    })

    try:
        # Get all prompts
        prompts = client.get_all_prompts("your_folder_id")
        print("Available prompts:", prompts)

        # Chat with a specific prompt
        response = client.chat_with_prompt(
            prompt_id="your_prompt_id",
            user_message=[
                {
                    "type": "text",
                    "text": "Hello, how are you?"
                }
            ],
            memory_type="windowMemory",
            window_size=10,
            session_id="test_session",
            variables={},
            is_session_enabled=True,
        )
        print("Chat response:", response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

## Testing

### Setting Up Tests

1. Install test dependencies:

```bash
pip install pytest pytest-cov
```

2. Create a `.env` file in the root directory with your test credentials:

```env
PROMPTSTUDIO_API_KEY=your_test_api_key
PROMPTSTUDIO_ENV=test
```

### Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=promptstudio_sdk
```

### Writing Tests

Create test files in the `tests` directory. Here's an example test:

```python
import pytest
from promptstudio_sdk import PromptStudio

def test_chat_with_prompt():
    client = PromptStudio({
        'api_key': 'test_api_key',
        'env': 'test',
        'bypass': True

    })

    response = client.chat_with_prompt(
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
        is_session_enabled: Optional[bool] = True,
    )

    assert isinstance(response, dict)
    assert 'response' in response

```

## Type Hints

The SDK uses Python type hints for better IDE support and code documentation. Here are some key types:

```python
from typing import Dict, List, Union, Optional

# Message types
ImageMessage = Dict[str, Union[str, Dict[str, str]]]  # {"type": "image_url", "image_url": {"url": "..."}}
TextMessage = Dict[str, str]  # {"type": "text", "text": "..."}
UserMessage = List[Union[ImageMessage, TextMessage]]

# Memory types
Memory = Literal["fullMemory", "windowMemory"]

# Request payload
RequestPayload = Dict[str, Union[UserMessage, Memory, int, str, Dict[str, str], Optional[int]]]
```

## Error Handling

The SDK raises exceptions for various error cases:

```python
from promptstudio_sdk import PromptStudio

try:
    client = PromptStudio({
        'api_key': 'YOUR_API_KEY_from_promptstudio',
        'env': 'test',
        'bypass': True
    })
    response = client.chat_with_prompt(...)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run the tests to ensure everything works
5. Submit a pull request

## License

This SDK is released under the MIT License.
