# DeepSeekfree

Reverse Engineering of DeepSeek Web Interface  
Free API for interacting with DeepSeek, supporting V3 and R1 models, streaming responses, web search, and thought process visualization.

## ✨ Features


| **Core Feature**       | **Description**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| **Streaming Response** | Supports real-time data streaming with optional enable/disable mode for stream output. |
| **Thought Process**    | Visualizes the AI's reasoning logic chain for transparent decision-making.      |
| **Web Search**         | Smart web-integrated module for real-time internet information retrieval.       |
| **Session Management** | Cloud-based conversation archives with cross-device sync, batch deletion, and tag management. |
| **History Retrieval**  | Retrieves full conversation records via session ID.                             |


## Installation

Install DeepSeekfree using pip:

```bash
pip install DeepSeekfree
```

## First Steps: Obtaining Token and Cookie
Before usage, obtain your credentials from DeepSeek's official website.

#### Obtaining Token:
1. Open browser developer tools (F12 or Right-click → Inspect)
2. Navigate to Network tab and refresh page
3. Find any API request and copy the Authorization header value

<p align="center">
  <img src="https://github.com/danel-phang/DeepSeek-free/blob/main/images/token.png" alt="token">
</p>

### Obtaining Cookie
1. Open browser developer tools
2. Navigate to Application/Storage → Cookies
3. Copy the entire cookie string

<p align="center">
  <img src="https://github.com/danel-phang/DeepSeek-free/blob/main/images/cookie.png" alt="cookie">
</p>

## 🚀 Quick Start

### Initialize Client

```python
from DeepSeekfree import DeepSeek

# Initialize with pre-obtained credentials
client = DeepSeek(
    cookies="your_cookies", 
    Authorization="your_authorization_token"
)
```

### Create New Chat Session

```python
chat_session_id = client.create_chat_session()  # Returns chat_session_id for continuous dialogue
```

### Single-turn Interaction

```python
response = client.chat(
    prompt="Hello，DeepSeek！"
)  # Automatically creates new session on first use

print(response)
```

## 🧠 Advanced Usage

### Streaming Response Handling

```python
for chunk in client.chat(prompt="Write a short essay about AI", stream=True):
    print(chunk, end="\n")
```

### Enable Advanced Features

```python
response = client.chat(
    prompt="What are the latest advancements in AI?",
    thinking_enabled=True,   # Enable R1 reasoning model
    search_enabled=True,     # Activate web search
    stream=True              # Enable streaming
)
```

### Multi-turn Conversation

```python
# Initial question
first_response = client.chat(prompt="Who are you?")
print(first_response)
message_id = first_response["message_id"]
chat_session_id = first_response["chat_session_id"]

# Follow-up question with context
second_response = client.chat(
    prompt="What capabilities do you have?",
    chat_session_id=chat_session_id, 
    parent_id=message_id
)
print(second_response)
```

### Activate R1 Model & Web Search

```python
response = client.chat(
    prompt="Explain quantum computing",
    thinking_enabled=True,
    search_enabled=True
)
print(response)
```

### Retrieve Message History

```python
history = client.get_history_messages(chat_session_id=chat_session_id)
print(history)
```

### List Chat Sessions

```python
sessions = client.list_session(count=100)  # List last 100 sessions
print(sessions)
```

### Delete Chat Session

```python
delete_response = client.delete_session(
    chat_session_id=chat_session_id
)
print(delete_response)
```

## 🛠️ API Reference

### DeepSeek Parameters

| Parameter       | Type | Required | Description               |
|-----------------|------|----------|---------------------------|
| cookies         | str  | Yes      | Website authentication cookies |
| Authorization   | str  | Yes      | Bearer token              |

### chat() Method Parameters

| Parameter          | Type | Default | Description                      |
|--------------------|------|---------|----------------------------------|
| prompt             | str  | Required| User input message               |
| chat_session_id    | str  | None    | Session ID (creates new if empty)|
| parent_id          | str  | None    | Parent message ID for context    |
| thinking_enabled   | bool | False   | Enable R1 reasoning model        |
| search_enabled     | bool | False   | Enable web search integration    |

## Contribution

Welcome contributions! Please submit pull requests or open issues to report bugs.
