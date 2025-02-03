import json
import logging
import requests
from . import errors


class DeepSeek:
    """深度求索 DeepSeek 对象"""

    api_base: str = "https://chat.deepseek.com"

    count: int = 100
    """获取消息列表时数量"""

    cookies: str
    """Cookies字符串"""

    title: str
    """Title of current session"""

    chat_session_id: str = ""
    """Current session id"""

    parent_id: str = None
    """Parent msg id"""

    thinking_enabled: bool = False
    """R1 model enabled"""

    search_enabled: bool = False
    """Online search enabled"""

    def __init__(
            self,
            cookies: str = "",
            Authorization: str = "",
    ):


        if cookies:
            self.cookies = cookies
        
        if Authorization:
            self.Authorization = Authorization



        logging.debug(self.cookies)

        self.headers ={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"Bearer {self.Authorization}",
            "Content-Length": "167",
            "Content-Type": "application/json",
            "Cookie": self.cookies,
            "Origin": "https://chat.deepseek.com",
            "Referer": "https://chat.deepseek.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "X-DS-POW-Response": "eyJhbGdvcml0aG0iOiJEZWVwU2Vla0hhc2hWMSIsImNoYWxsZW5nZSI6IjQyNTc5YTk3ZGEwNDE2ODQyMmIzNWM4YzUzOTAyOTk0OTU5ZDUwNmMzZWRjYzVmODY4MjE3NzliNDJiYTkwZjkiLCJzYWx0IjoiNGY5MTA4NzlkMTgyYjEzZTIxYTgiLCJhbnN3ZXIiOjg0MDAxLCJzaWduYXR1cmUiOiIzM2RjNmQ4YTYxMTc1Yjk1MjZiNzFkOTA2NTJkNjBlNGYxMjRiN2UzM2UxNTI0NGMyYTE1NWQyZmQ5MWI4NzBlIiwidGFyZ2V0X3BhdGgiOiIvYXBpL3YwL2NoYXQvY29tcGxldGlvbiJ9"
        }

    def _streaming(
            self,
            prompt: str,
            parent_id: str = None,
            chat_session_id: str = "",
            timeout: int = 60,
            image: bytes = None,
            thinking_enabled: bool = False,
            search_enabled: bool = False,
    ) :
        """流式回复

        Args:
            prompt (str): 提问内容
            parent_id (str, optional): 父消息id. Defaults to None.
            chat_session_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """
        if parent_id == None:
            self.parent_id = self.parent_id

        headers = self.headers.copy()

        headers['Accept'] = 'text/event-stream'

        data = {
            "chat_session_id": chat_session_id,
            "parent_message_id": parent_id,
            "prompt": prompt,
            "ref_file_ids": [],
            "thinking_enabled": thinking_enabled,
            "search_enabled": search_enabled,
        }

        print(data)
        if image:
            image_link = self.upload_image(image)


        resp = requests.post(
            url=self.api_base + "/api/v0/chat/completion",
            headers=self.headers,
            data=json.dumps(data),
            timeout=timeout,
            stream=True
        )
        for line in resp.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                # 过滤心跳包等非数据内容
                if decoded_line.startswith('data: '):
                    json_str = decoded_line[6:] 
                    
                    if json_str.strip() == '[DONE]':
                        break

                    try:
                        chunk = json.loads(json_str)
                        if chunk:
                            content = chunk
                            # 往content中添加一个键值对: chat_session_id
                            content["chat_session_id"] = chat_session_id
                            yield content

                        
                    except json.JSONDecodeError:
                        raise errors.DeepSeekErrors("unexpected response: {}".format(json_str))


    def _un_streaming(
            self,
            prompt: str,
            parent_id: str = None,
            chat_session_id: str = "",
            timeout: int = 60,
            image: bytes = None,
            thinking_enabled: bool = False,
            search_enabled: bool = False,
    ):
        """非流式回复

        Args:
            prompt (str): 提问内容
            parent_id (str, optional): 父消息id. Defaults to None.
            chat_session_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """
        thinking_content = ""
        text_content = ""
        token_usage = 0

        for resp in self._streaming(
                prompt,
                parent_id,
                chat_session_id,
                timeout,
                image,
                thinking_enabled,
                search_enabled,
        ):
            try:
                data = resp
                # 提取内容片段
                if "choices" in data:
                    token_usage += data["chunk_token_usage"]
                    for choice in data["choices"]:
                        if "delta" in choice and "content" in choice["delta"] and choice["delta"]["type"]=="thinking":
                            thinking_content += choice["delta"]["content"]
                        if "delta" in choice and "content" in choice["delta"] and choice["delta"]["type"]=="text":
                            text_content += choice["delta"]["content"]
                            
                        # 检查是否结束, 并返回完整data内容
                        if "finish_reason" in choice and choice["finish_reason"] == "stop":
                            # 如果有thinking_content, 则将thinking_content与text_content合并, 并将thinking_content用标签包裹
                            if thinking_content:
                                full_content =  f"<thinking>{thinking_content}</thinking>" + "\n" + "\n"+ text_content
                            else:
                                full_content = text_content
                            choice['delta']['content'] = full_content
                            data["chunk_token_usage"] = token_usage
                            return data

            except json.JSONDecodeError:
                raise errors.DeepSeekErrors("unexpected response: {}".format(resp))

    # 创建新的聊天会话并返回 chat_session_id
    def create_chat_session(self, character_id: str = None) -> str:
        """
        创建新的聊天会话并返回会话ID
        :param token: 认证令牌
        :param character_id: 可选的角色ID
        :return: chat_session_id (失败时返回None)
        """
        headers = {
            "Host": "chat.deepseek.com",
            "Connection": "keep-alive",
            "Content-Length": "21",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "X-Client-Locale": "zh_CN",
            "X-Client-Version": "1.0.0-always",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "X-App-Version": "20241129.1",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "\"Windows\"",
            "Accept": "*/*",
            "Origin": "https://chat.deepseek.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://chat.deepseek.com/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.cookies,
            "Authorization": f"Bearer {self.Authorization}",
            "X-Client-Platform": "web",
            "Priority": "u=1, i",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"130.0.6723.70\"",
            "sec-ch-ua-platform-version": "\"15.0.0\""
}

        payload = {"character_id": character_id}

        try:
            response = requests.post(
                "https://chat.deepseek.com/api/v0/chat_session/create",
                headers=headers,
                json=payload
            )
            response.raise_for_status()  # 检查HTTP错误状态码
            response_data = response.json()
            return response_data["data"]["biz_data"]["id"]
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None
        except KeyError as e:
            print(f"响应数据格式异常，缺少关键字段: {str(e)}")
            return None
        except Exception as e:
            print(f"发生未知错误: {str(e)}")
            return None


    def chat(
            self,
            prompt: str,
            parent_id: str = None,
            chat_session_id: str = "",
            timeout: int = 60,
            stream: bool = False,
            image: bytes = None,
            thinking_enabled: bool = False,
            search_enabled: bool = False,
    ):
        """Chat
        Args:
            prompt (str): 用户内容
            parent_id (str, optional): 父消息id. Defaults to None.
            chat_session_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            stream (bool, optional): 是否流式. Defaults to False.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """

        # 检查session或新建
        if not self.chat_session_id:
            self.chat_session_id = self.create_chat_session()
            chat_session_id = self.chat_session_id
            logging.debug(f"sessionId不存在,新建chat_session_id: {self.chat_session_id}")

        if stream:
            return self._streaming(
                prompt,
                parent_id,
                chat_session_id,
                timeout,
                image,
                thinking_enabled,
                search_enabled,
            )
        else:
            return self._un_streaming(
                prompt,
                parent_id,
                chat_session_id,
                timeout,
                image,
                thinking_enabled,
                search_enabled,
            )


    def get_history_messages(self, chat_session_id: str):

        headers ={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"Bearer {self.Authorization}",
            "Content-Type": "application/json",
            "Cookie": self.cookies,
            "Origin": "https://chat.deepseek.com",
            "Referer": f"https://chat.deepseek.com/a/chat/s/{chat_session_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }

        resp = requests.get(
            url=self.api_base + f"/api/v0/chat/history_messages?chat_session_id={chat_session_id}",
            headers=headers,
        )
        
        resp_json = resp.json()

        if resp.status_code == 200:
            return json.dumps(resp_json, ensure_ascii=False, indent=2)
        else:
            raise errors.DeepSeekErrors(f"unexpected response: {resp_json}"+"\n" + resp.text)
        
    def list_session(self, count: int = 100) -> dict:
        """
        读取聊天会话列表
        Args:
            count (int): 要检索的聊天会话数。默认值为 100
        Returns:
            dict: 包含聊天会话列表的字典
        """

        headers ={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"Bearer {self.Authorization}",
            "Content-Type": "application/json",
            "Cookie": self.cookies,
            "Referer": "https://chat.deepseek.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }
        resp = requests.get(
            url=self.api_base + f"/api/v0/chat_session/fetch_page?count={count}",
            headers=headers,
            timeout=60
        )

        resp_json = resp.json()
        
        if resp.status_code == 200:
            return json.dumps(resp_json, ensure_ascii=False, indent=2)
        else:
            raise errors.DeepSeekErrors(f"unexpected response: {resp_json}"+"\n" + resp.text)



    def delete_session(self, chat_session_id: str):

        headers ={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"Bearer {self.Authorization}",
            "Content-Type": "application/json",
            "Cookie": self.cookies,
            "Origin": "https://chat.deepseek.com",
            "Referer": f"https://chat.deepseek.com/a/chat/s/{chat_session_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }

        resp = requests.post(
            url=self.api_base + "/api/v0/chat_session/delete",
            headers=headers,
            json={
                "chat_session_id": chat_session_id
            }, 
            timeout=10
        )

        if resp.status_code == 200:
            return "success"
        else:
            raise errors.DeepSeekErrors(f"unexpected response: {resp}"+"\n" + resp.text)

