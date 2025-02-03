from DeepSeekfree import DeepSeek
import json

question = "who are u"

client  = DeepSeek(
    Authorization = "",
    cookies = "",
)

# history = client.delete_session(chat_session_id="f27beb9a-ae65-4208-b2e8-37ef23b72d08")
# print(history)

data = client.create_chat_session()
print(data)

# message_id = data["message_id"]
# chat_session_id = data["chat_session_id"]

# question2 = "你会什么"
# data2 = chatbot.ask(prompt=question2, chat_session_id=chat_session_id, parent_id=message_id, thinking_enabled=True)
# print(json.dumps(data2, ensure_ascii=False, indent=4))
# message_id = data2["message_id"]

# question3 = "我最开始问了你什么"
# data3 = chatbot.ask(prompt=question3, chat_session_id=chat_session_id, parent_id=message_id)
# print(json.dumps(data3, ensure_ascii=False, indent=4))

# message_id = data3["message_id"]
