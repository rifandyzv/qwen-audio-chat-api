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
         '''
         you are virtual assistant, this audio is a meeting recording between Alibaba Cloud and Customers 
         please provide these from the audio:
         *brief summary
         *the customer requirements
         *analyze the possible sales pipeline from this meeting recording. 
         
         please give the output strictly as this, I don't want any other format answer other than this! :

         Summary:
         Customer Requirements:
         Possible pipeline: 
         
         '''},
    ])
    return model.chat(tokenizer, query=query, history=None)


def generateMeetingSummary(audio):


    initiator = tokenizer.from_list_format([
    {'audio': audio}, # Either a local path or an url
    {'text': 
         '''
         you are virtual assistant, this audio is a meeting recording between Alibaba Cloud and Customers 
         please provide these from the audio:
         *brief summary
         *the customer requirements
         *analyze the possible sales pipeline from this meeting recording. 
         
         please give the output strictly as this, I don't want any other format answer other than this! :

         Summary:
         Customer Requirements:
         Possible pipeline: 
         
         '''},
    ])
    questions =  [
         'please give bullets point from that meeting discussion',
         'from your perspective what can alibaba provides to customer according to that meeting discussion', 
         'how about user requirements? do you get any information from that meeting discussion for customer requirements?',
         'please answer just shortly in one or two sentences, from this meeting discussion what do you thing the customer sentiment about alibaba cloud?'
         ]
    
    answers = {'summary': '', 'customerRequirements': '', 'opportunity': ''}

    text, history = model.chat(tokenizer, query=initiator, history=None)

    answers['summary'], history = model.chat(tokenizer, query=questions[0], history=history)

    answers['customerRequirements'], history = model.chat(tokenizer, query=questions[1], history=history)

    answers['opportunity'], history = model.chat(tokenizer, query=questions[2], history=history)

    answers['additionalInfo'], history =  model.chat(tokenizer, query=questions[3], history=history)

    return answers