from langchain.llms.base import LLM
import requests
from typing import Optional, List
import uuid
from youdotcom import Chat

def generate_user_id():
    def decorator(cls):
        cls.user = uuid.uuid4()
        return cls
    return decorator


class YouChatLLM(LLM):
    api_key: str
    
    @property
    def _llm_type(self) -> str:
        return "YouChat LLM"

    def __api_call(self, message, stop=None):
        """Calling the YouChat API

        Args:
            message (str): The prompt for the openai api.

        Returns:
            json: The response from the api.
        """
        chat = Chat.send_message(api_key=self.api_key, message=message)
        print(chat)

        try:
            message = chat['message']
            if message == "Due to cloudflare limits i'm curently getting new cookies, please try again.":
                return "Something went wrong. Please try again. Later. (TOKENS)"
            if "Too Many Requests" in message:
                return "Something went wrong. Please try again. Later. (REQUESTS)"
        except Exception as e:
            return "Something went wrong. Please try again. Later."
        return message
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
           response = self.__api_call(prompt, stop)
        response =  self.__api_call(prompt)
        if isinstance(response, str):
            return response
        else: 
            return response['choices'][0]['message']['content']

        

@generate_user_id()
class OpenAILLM(LLM):
    temperature: float
    model: str
    # Setting default values for optional parameters
    def optional_paramter_set(self, 
                              top_p: Optional[int] = None, 
                              max_tokens: Optional[int] = None, 
                              presence_penalty: Optional[int] = None, 
                              frequency_penalty: Optional[int] = None, 
                              logit_bias: Optional[int] = None):
        if top_p:
            self.top_p = top_p
        if max_tokens:
            self.max_tokens = max_tokens
        if presence_penalty:
            self.presence_penalty = presence_penalty
        if frequency_penalty:
            self.frequency_penalty = frequency_penalty
        if logit_bias:
            self.logit_bias = logit_bias


    @property
    def _llm_type(self) -> str:
        return "OpenAI Custom ChatBot LLM"

    def __api_call(self, message, stop=None):
        """Calling the OpenAI Unofficial API

        Args:
            message (str): The prompt for the openai api.

        Returns:
            json: The response from the api.
        """

        headers = {'Content-Type': 'application/json'}
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "temperature": self.temperature,
            "user": str(self.user)
        }

        # Reading Injected parameters
        if getattr(self, "top_p", None):
            data['top_p'] = self.top_p
        if getattr(self, "max_tokens", None):
            data['max_tokens'] = self.max_tokens
        if getattr(self, "precence_penalty", None):
            data['presence_penalty'] = self.presence_penalty
        if getattr(self, "frequency_penalty", None):
            data['frequency_penalty'] = self.frequency_penalty
        if getattr(self, "logit_bias", None):
            data['logit_bias'] = self.logit_bias
        if stop:
            data['stop'] = stop
        response = requests.post('https://chatgpt-api.shn.hk/v1/', headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)

            return "Something went wrong."

        return response.json()
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
           response = self.__api_call(prompt, stop)
        response =  self.__api_call(prompt)
        if isinstance(response, str):
            return response
        else: 
            return response['choices'][0]['message']['content']
        
