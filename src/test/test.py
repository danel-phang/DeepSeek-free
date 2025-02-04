from DeepSeekfree import DeepSeek
import json

question = "who are u"

client  = DeepSeek(
    Authorization = "",
    cookies = "",
)

# history = client.delete_session(chat_session_id="f27beb9a-ae65-4208-b2e8-37ef23b72d08")
# print(history)

for chunk in client.chat(prompt=question, stream=True):
    print(chunk, end="\n")
# message_id = data["message_id"]
# chat_session_id = data["chat_session_id"]
