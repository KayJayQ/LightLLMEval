from dataset_plugins import Math500
from backend_plugins.vllm_client import VLLMClient

dataset = Math500("math500", "dataset_plugins/math500/test.jsonl", 42)
client = VLLMClient("empty", "http://0.0.0.0:8000/v1", 4)

for problem, refer in dataset.sample(batch_size=4):
    results = client.process(problem, refer)
    dataset.eval(results, refer)
    break