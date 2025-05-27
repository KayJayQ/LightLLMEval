from typing_extensions import *

class BackendPlugin:
    def __init__(self, *args, **kwargs):
        pass
    
    def process(self, querys:List[str], labels:List[str], *args, **kwargs):
        pass
    
    def reset(self, *args, **kwargs):
        pass
    
    def close(self, *args, **kwargs):
        pass

