# DeepSeek-free

DeepSeek-free 是一个用于与 DeepSeek API 交互的 Python 包。

## 安装

使用以下命令安装 DeepSeek-free：

```bash
pip install DeepSeek-free
```

## 使用

以下是如何使用 DeepSeek-free 包的示例：

```python
from deepseek import DeepSeek

# 初始化 DeepSeek 对象
deepseek = DeepSeek(cookies="your_cookies", Authorization="your_authorization_token")

# 创建新的聊天会话
chat_session_id = deepseek.create_chat_session()

# 发送消息并获取回复
response = deepseek.chat(prompt="你好，DeepSeek！", chat_session_id=chat_session_id)
print(response)

# 获取历史消息
history = deepseek.get_history_messages(chat_session_id=chat_session_id)
print(history)

# 列出所有聊天会话
sessions = deepseek.list_session()
print(sessions)

# 删除聊天会话
delete_response = deepseek.delete_session(chat_session_id=chat_session_id)
print(delete_response)
```

## 模块

### deepseek

包含与 DeepSeek API 交互的主要类 `DeepSeek`。

#### DeepSeek

- `__init__(self, cookies: str = "", Authorization: str = "")`
- `create_chat_session(self, character_id: str = None) -> str`
- `chat(self, prompt: str, parent_id: str = None, chat_session_id: str = "", timeout: int = 60, stream: bool = False, image: bytes = None, thinking_enabled: bool = False, search_enabled: bool = False)`
- `get_history_messages(self, chat_session_id: str)`
- `list_session(self, count: int = 100) -> dict`
- `delete_session(self, chat_session_id: str)`

### errors

包含自定义异常类：

- `DeepSeekErrors`
- `FileNotFoundError`
- `InvalidFormatError`
- `ProcessingError`

## 贡献

欢迎贡献代码！请提交 pull request 或报告问题。
