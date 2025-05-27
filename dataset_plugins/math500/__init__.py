from ..dataset_plugin import DatasetPlugin
from typing_extensions import *
from datasets import load_dataset
from .grader import grade_answer
import re

class Math500(DatasetPlugin):
    
    def __init__(self, name:str, dataset_path:str, random_seed:Union[None, int]=None):
        super().__init__(name, dataset_path, random_seed)
        self.name = name
        self.dataset_path = dataset_path
        self.random_seed = random_seed
        self.dataset = load_dataset("json", data_files=dataset_path)['train']
        
        if random_seed:
            self.dataset = self.dataset.shuffle(seed=random_seed)

        self.data_size = len(self.dataset)
        self.correct = 0
        
    @staticmethod
    def from_remote(name, url, random_seed = None):
        return super().from_remote(name, url, random_seed)
    
    def sample(self, batch_size:int=1, **kwargs)->Generator[List[str], List[str]]:
        for idx in range(0, self.data_size, batch_size):
            query_list = [self.dataset[i]['problem'] for i in range(idx, min(idx+batch_size, self.data_size))]
            answer_list = [self.dataset[i]['answer'] for i in range(idx, min(idx+batch_size, self.data_size))]
            yield query_list, answer_list
    
    def eval(self, answer:List[str], corrected_answer:List[str], is_raw:bool=True, verbose:bool=True, **kwargs):
        # if is raw, find the last boxed content using regex, if not found, return None
        result = False
        if not is_raw:
            for refer, solution in zip(corrected_answer, answer):
                result = grade_answer(refer, solution)
                if result:
                    self.correct += 1
                elif verbose:
                    print(f"{refer} is not equal to {solution}")
                if verbose:
                    print(f"Correct: {self.correct}  / {self.data_size}")
            return result
        else:
            for refer, solution in zip(corrected_answer, answer):
                boxed_content = re.findall(r'\\boxed{(.*?)}', solution)
                if boxed_content:
                    result = grade_answer(refer, boxed_content[-1])
                    if result:
                        self.correct += 1
                    elif verbose:
                        print(f"{refer} is not equal to {boxed_content[-1]}")
                elif verbose:
                        print("No boxed content found in content")
                if verbose:
                    print(f"Correct: {self.correct}  / {self.data_size}")
            return result
    def reset(self):
        self.correct = 0
    
    def get_result(self, verbose:bool=True)->Any:
        print(f"{self.name} accuracy: {self.correct / self.data_size}")
        return self.correct / self.data_size
    