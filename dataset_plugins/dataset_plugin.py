from typing_extensions import *

class DatasetPlugin:

    def __init__(self, name:str, dataset_path:str, random_seed:Union[None, int]=None):
        pass
        
    @staticmethod
    def from_remote(name:str, url:str, random_seed:Union[None, int]=None):
        raise NotImplementedError
    
    def sample(self, batch_size:int=1, **kwargs)->Generator[List[str], List[str]]:
        pass
    
    def eval(self, answer:List[str], corrected_answer:List[str], **kwargs):
        pass
    
    def reset(self):
        pass
    
    def get_result(self)->Any:
        pass
    