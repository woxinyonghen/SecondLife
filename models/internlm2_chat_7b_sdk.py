from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def internlm2_summary(life_record):
    print("load model start")
    model_dir = 'history'
    model = (
        AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
            .to(torch.bfloat16)
            .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    print("load model end")
    model.eval()
    # print(life_record)
    response, history = model.chat(tokenizer, life_record, history=[])
    torch.cuda.empty_cache()
    return response


def internlm2_chat(prompt):
    print("load model start")
    model_dir = 'history'
    model = (
        AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
            .to(torch.bfloat16)
            .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    print("load model end")
    model.eval()
    response, history = model.chat(tokenizer, prompt, history=[])
    torch.cuda.empty_cache()
    return response
