from DeepSeekfree import deepseek
import json

question = "who are u"

client  = DeepSeek(
    Authorization = "d71148b58a8a476cb2eebba3cd789d6f",
    cookies = "_frid=f8b02169a1064443b962c11fa1023b97; smidV2=20241122210214b9bc8e84344a93940417c8981f8e44d400cf385ff445c67b0; .thumbcache_6b2e5483f9d858d7c661c5e276b6a6ae=iRdk/ku4gb6rTisxOtqmwINleB2NsmXwpjSK6Mk0VhO+7lmHL7+6gaPBv+lfuBaQWstXoYRn499FcFheBm1FzA%3D%3D; intercom-device-id-guh50jw4=f65708c1-cb3f-4024-b5f9-7037e504e671; Hm_lvt_fb5acee01d9182aabb2b61eb816d24ff=1737871717; HMACCOUNT=3C97D9DC9C81F247; HWWAFSESTIME=1737871716496; HWWAFSESID=fd37e4eab767365c0a1; ds_session_id=8fba8eab5d074f55b7b0fa40668b9c58; Hm_lvt_1fff341d7a963a4043e858ef0e19a17c=1737871718; Hm_lpvt_fb5acee01d9182aabb2b61eb816d24ff=1738481649; Hm_lpvt_1fff341d7a963a4043e858ef0e19a17c=1738481652; intercom-session-guh50jw4=am1ZT08zU252OSttam1aQVBaRHppb2pzVmxmeTk4QVVtdEZvY1dCUzVLRE14QlI1RjZ6cEZRU1hPUlRjdnQzaFNBWEVneVhGSVNkSjVHUHA4bHB1d2lyVURkNzd6SVRWOG44cnVqenZtNGs9LS1yb1l4cG40ci95emZ5Z2MzdXhBMVlRPT0=--bbdc74f09b4bb518749b96ae9d8e55679f68d53f",
)

history = client.delete_session(chat_session_id="f27beb9a-ae65-4208-b2e8-37ef23b72d08")
print(history)

# data = client.chat(
#     prompt=question, 
#     thinking_enabled=False,
#     search_enabled=False,
#     stream=False,
# )
# print(json.dumps(data, ensure_ascii=False, indent=4))


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
