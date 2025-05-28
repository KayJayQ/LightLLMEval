from . import BackendPlugin
from typing_extensions import *
from openai import OpenAI
import asyncio

class VLLMClient(BackendPlugin):
    '''
    Client only, need to deploy vllm server on local machine or cloud
    '''
    
    def __init__(self, api_key:str, api_base:str, max_parallel:int=1):
        self.api_key = api_key
        self.api_base = api_base
        self.max_parallel = max_parallel
        
        self.clients = [OpenAI(
            api_key=api_key,
            base_url=api_base,
        ) for _ in range(max_parallel)]
        
        models = self.clients[0].models.list()
        self.model = models.data[0].id
        
    def process(self, querys:List[str], labels:List[str], *args, **kwargs):
        messages = [[
            {
                "role": "user",
                "content": query,
            }
        ] for query in querys]

        async def single_submit(message, client):
            response = client.chat.completions.create(
                model=self.model,
                messages=message
            )
            return response.choices[0].message.content
        
        async def submit_all():
            tasks = [single_submit(message, client) for message, client in zip(messages, self.clients)]
            result = await asyncio.gather(*tasks)
            return result

        return asyncio.run(submit_all())
    
