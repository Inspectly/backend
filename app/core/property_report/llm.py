import os
import sys
import json
import asyncio
from pprint import pprint

from openai import OpenAI, AsyncOpenAI

sys.path.append('../')

class Open_AI:
    def __init__(self, open_ai_model = 'gpt-4.1', open_ai_experimental_model = 'o3-mini'):
        api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(
            api_key = api_key
        )
        self.async_client = AsyncOpenAI(
            api_key = api_key
        )
        self.model = open_ai_model
        self.model_experimental = open_ai_experimental_model


    def chat_completion(self, messages, experimental = False):
        response = self.client.chat.completions.create(
            model = self.model_experimental if experimental else self.model,
            messages = messages,
            # temperature = 0.0
        )
        return response.choices[0].message.content
    
    def chat_completion_structured(self, messages, structure, token_view = False):
        response = self.client.beta.chat.completions.parse(
            model = self.model,
            messages = messages,
            response_format = structure
        )
        if token_view:
            print('Tokens used:', response.usage)
        return response.choices[0].message.parsed

    def chat_completion_function_call(self, messages, functions, function_call = 'auto'):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            functions = functions,
            function_call = function_call  
        )
        return response.choices[0].message.function_call

    async def async_chat_completion(self, messages, experimental = False):
        response = await self.async_client.chat.completions.create(
            model = self.model_experimental if experimental else self.model,
            messages = messages,
        )
        return response.choices[0].message.content
    
    async def async_chat_completion_structured(self, messages, structure):
        response = await self.async_client.beta.chat.completions.parse(
            model = self.model,
            messages = messages,
            response_format = structure
        )
        return response.choices[0].message.parsed
    
    async def async_chat_completion_function_call(self, messages, functions, function_call = 'auto'):
        response = await self.async_client.chat.completions.create(
            model = self.model,
            messages = messages,
            functions = functions,
            function_call = function_call  
        )
        return response.choices[0].message.function_call


def main():
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Who won the world series in 2020?'},
        {'role': 'assistant', 'content': 'The Los Angeles Dodgers won the World Series in 2020.'},
        {'role': 'user', 'content': 'Where was it played?'}
    ]
    open_ai = Open_AI()
    response = open_ai.chat_completion(messages)
    pprint(response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
