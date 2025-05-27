from . import BackendPlugin
from typing_extensions import *
from openai import OpenAI

class VLLMClient(BackendPlugin):
    '''
    Client only, need to deploy vllm server on local machine or cloud
    '''
    
    def __init__(self, api_key:str, api_base:str, max_parallel:int=1):
        self.api_key = api_key
        self.api_base = api_base
        self.max_parallel = max_parallel
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        
        models = self.client.models.list()
        self.model = models.data[0].id
        
    def process(self, querys:List[str], labels:List[str], *args, **kwargs):
        messages = [
            {
                "role": "user",
                "content": query,
            }
            for query in querys
        ]
        
        responses = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            # max_tokens=128,
            n = self.max_parallel
        )
        
        responses_text = [response.message.content for response in responses.choices]
        
        return responses_text
    