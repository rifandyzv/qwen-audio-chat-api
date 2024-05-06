from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch


torch.manual_seed(1234)
torch.device("cuda" if torch.cuda.is_available() else "cpu")


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-Audio-Chat", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-Audio-Chat", device_map="auto", trust_remote_code=True, low_cpu_mem_usage=True).eval()

model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-Audio-Chat", trust_remote_code=True)


def callQwen(audio):
    query = tokenizer.from_list_format([
        {'audio': audio},
        {'text': 'you are my assistant, please give brief bullet point summary from this sound'},
    ])
    return model.chat(tokenizer, query=query, history=None)


def callMeetingSummary(audio):
    query = tokenizer.from_list_format([
        {'audio': audio},
        {'text': 
         '''you are virtual assistant, this audio is a meeting recording between Alibaba Cloud and Customers in Bahasa Indonesia. 
         please provide the meeting summary and also gather the customer requirements, and also please analyze the possible sales pipeline from this meeting recording. 
         please give the output strictly as this, I don't want any other format answer other than this! :

         Summary:
         Customer Requirements:
         Possible pipeline: 
         
         '''},
    ])
    return model.chat(tokenizer, query=query, history=None)