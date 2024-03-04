from modelscope import snapshot_download, AutoTokenizer, AutoModelForCausalLM
import torch


def load_model():
    torch.cuda.empty_cache()
    print("load model start")
    model_dir = 'history'
    model = (
        AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
            .to(torch.bfloat16)
            .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    print("load model end")
    return model, tokenizer


def internlm2_summary(life_record, model, tokenizer):
    model = model.to(torch.bfloat16).cuda()
    model.eval()
    print(life_record)
    response, history = model.chat(tokenizer, life_record, history=[])
    return response


def internlm2_chat(prompt, model, tokenizer):
    model = model.to(torch.bfloat16).cuda()
    model.eval()

    response, history = model.chat(tokenizer, prompt, history=[])
    return response
