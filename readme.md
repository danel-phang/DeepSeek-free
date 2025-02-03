# DeepSeekfree

DeepSeek 网页端逆向
免费的 Api 与 DeepSeek 进行交互, 可选 V3 模型和 R1 模型,支持流式响应,网络搜索,可展示思维过程。

## ✨ 特色功能

- 🔄 **流式响应**：支持可选流式输出 
- 🤔 **思考过程**：可查看模型的推理步骤 
- 🔍 **Web 搜索**：可选集成以获取最新信息 
- 💬 **会话管理**：具有对话历史记录的持久聊天会话, 列出会话列表以及删除会话

## 安装

使用以下命令安装 DeepSeekfree：

```bash
pip install DeepSeekfree
```

## 第一步获取token 和 cookie
使用之前,前往DeepSeek官网获取token 和 cookie.
#### 获取token:
F12 或者 右键->检查打开控制台

<p align="center">
  <img src="https://github.com/danel-phang/DeepSeek-free/blob/main/images/token.png" alt="token">
</p>

### 获取cookie

F12 或者 右键->检查打开控制台
<p align="center">
  <img src="https://github.com/danel-phang/DeepSeek-free/blob/main/images/cookie.png" alt="cookie">
</p>


## 🚀 快速开始

### 初始化客户端

```python
from DeepSeekfree import DeepSeek

# 使用预获取的凭证初始化
client = DeepSeek(
    cookies="your_cookies", 
    Authorization="your_authorization_token"
)
```



### 创建新的聊天会话

```python
from DeepSeekfree import DeepSeek

client = DeepSeek(
    cookies="your_cookies", 
    Authorization="your_authorization_token"
)
chat_session_id = deepseek.create_chat_session() # 返回chat_session_id, 可用于连续对话
```

### 单轮对话示例

```python
response = deepseek.chat(
    prompt="Hello，DeepSeek！"
)# 第一次会自动创建新的聊天会话

print(response)
```



## 🧠 进阶用法

### 流式响应处理

```python
for chunk in client.chat(prompt="写一篇关于AI的短文", stream=True):
    print(chunk, end="\n")
```



### 启用高级功能

```python
response = client.chat(
    prompt="最新的人工智能进展有哪些？",
    thinking_enabled=True,   # 启用R1思考模型
    search_enabled=True,     # 开启网络搜索
    stream=True              # 开启流式传输
)
```



### 多轮对话示例

通过传入父消息Id以及当前会话Id实现连续对话

```python
from DeepSeekfree import DeepSeek

client = DeepSeek(
    cookies="your_cookies", 
    Authorization="your_authorization_token"
)
question = "who are u"

data = client.chat(prompt=question)
print(data)
message_id = data["message_id"]
chat_session_id = data["chat_session_id"]

question2 = "你会什么"
data2 = client.chat(
    prompt=question2, 
    chat_session_id=chat_session_id, 
    parent_id=message_id
)
print(data2)
```



### 开启R1模型(思考模型)以及联网搜索

```python
response = deepseek.chat(
    prompt="Hello，DeepSeek！",
    thinking_enabled=True,
    search_enabled=True
)# 第一次自动创建新的聊天会话
print(response)
```


### 获取历史消息
获取指定 chat_session_id 会话历史消息
```python
history = deepseek.get_history_messages(chat_session_id=chat_session_id)
print(history)
```

### 列出聊天会话
通过传入参数count,列出自定义会话数
```python
sessions = deepseek.list_session(count=100)
print(sessions)
```

### 删除聊天会话
删除指定 chat_session_id 会话
```python
delete_response = deepseek.delete_session(
    chat_session_id=chat_session_id
)
print(delete_response)
```



## 🛠️ 接口参数

### DeepSeek 参数

| 参数          | 类型 | 必填 | 说明                    |
| :------------ | :--- | :--- | :---------------------- |
| cookies       | str  | 是   | 网站认证cookies         |
| Authorization | str  | 是   | Bearer令牌              |

### chat() 方法参数

| 参数             | 类型 | 默认值 | 说明                       |
| :--------------- | :--- | :----- | :------------------------- |
| prompt           | str  | 必填   | 用户输入的提示信息         |
| chat_session_id  | str  | None   | 会话ID（为空则创建新会话） |
| parent_id        | str  | None   | 父消息ID（用于上下文追踪） |
| thinking_enabled | bool | False  | 启用R1思考模型             |
| search_enabled   | bool | False  | 启用网络搜索功能           |



## 贡献

欢迎贡献代码！请提交 pull request 或报告问题。
