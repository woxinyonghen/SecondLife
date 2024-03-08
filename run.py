import gradio as gr
from agents.second_life import game_control
from models.internlm2_chat_7b_sdk import internlm2_summary, internlm2_chat
from transformers import AutoModelForCausalLM, AutoTokenizer
import copy
import torch
import traceback

from openxlab.model import download


download(model_repo='星辰/The_History', output='history')

# def load_model(model_dir):
#     model = (
#         AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
#         .to(torch.bfloat16)
#         .cuda()
#     )
#     tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
#     return model, tokenizer

# # 加载微调后的模型
# print("load model begin.")
# model, tokenizer = load_model('history')
# print("load model end")

game = game_control()

def fn_next_year():
    print_text = game.get_next_year()
    if game.player_info["LIF"] < 0:
        final_txt = '\n'.join(game.all_text)
    else:
        summary_text = ""
    return '\n'.join(game.all_text)


def fn_all_life(v1, v2, v3, v4, v5):
    game.player_info['CHR'] = v1
    game.player_info['INT'] = v2
    game.player_info['STR'] = v3
    game.player_info['MNY'] = v4
    game.player_info['TLT'] = v5
    if game.player_info["LIF"] < 0:
        pass
    else:
        while True:
            print_text = game.get_next_year()
            if game.player_info["LIF"] < 0:
                break
    final_txt = '\n'.join(game.all_text)
    summary_text = internlm2_summary(f"你需要根据给定的人生记录，对这个人的人生进行评价。人生记录为{final_txt}", model, tokenizer)
    return '\n'.join(game.all_text), summary_text


def fn_restart():
    game.__init__()
    return "", "", game.player_info['CHR'], game.player_info['INT'], game.player_info['STR'], game.player_info['MNY']


def echo(message, history):
    message = internlm2_chat(message, model, tokenizer)
    return message


with gr.Blocks() as demo:
    gr.HTML('<center><h1> 第二人生 </h1> </center>')
    with gr.Row():
        gr.Markdown(
            '''
            罗曼·罗兰曾说过，世上只有一种英雄主义，就是在认清生活真相之后依然热爱生活。

            你有20个属性点可以添加，每个属性起始值是0，单项最多添加10个属性值。

            你可以从颜值、智力、体质、家境四个维度分别调整属性值。
            '''
        )
        dropdown_TLT = gr.Dropdown(
            game.random_talents, value=[], multiselect=True, label="天赋",
            info="任选3个天赋", max_choices=3, interactive=True, scale=1, allow_custom_value=True)
        # gr.HTML(
        #     '<center> 相信音乐的力量 </center>'
        #     '<iframe frameborder="yes" border="4" marginwidth="0" marginheight="0" width=710 height=100 src="//music.163.com/outchain/player?type=4&id=527081638&auto=1&height=280"></iframe>')

    with gr.Row():
        slider_CHR = gr.Slider(0, 10, value=game.player_info['CHR'],
                               step=1, label="颜值", interactive=True, randomize=False)  # , info="选择0到10之间的一个整数"
        slider_INT = gr.Slider(0, 10, value=game.player_info['INT'],
                               step=1, label="智力", interactive=True, randomize=False)
        slider_STR = gr.Slider(0, 10, value=game.player_info['STR'],
                               step=1, label="体质", interactive=True, randomize=False)
        slider_MNY = gr.Slider(minimum=0, maximum=10, value=game.player_info['MNY'],
                               step=1, label="家境", interactive=True, randomize=False)

    with gr.Row():
        txt_result = gr.Text(label="人生轨迹", lines=10, max_lines=10, scale=1)
        txt_summary = gr.Text(label="人生报告", lines=10, max_lines=10, scale=1)
        # txt_score = gr.Text(label="人生评分", lines=10, max_lines=10)

    with gr.Row():
        btn_next = gr.Button(value='预知未来')
        btn_all = gr.Button(value='回顾过去')
        btn_restart = gr.ClearButton(value='时光倒流')

    btn_restart.click(fn=fn_restart, outputs=[txt_result, txt_summary, slider_CHR, slider_INT, slider_STR, slider_MNY])
    btn_next.click(fn=fn_next_year, outputs=[txt_result])
    btn_all.click(inputs=[slider_CHR, slider_INT, slider_STR, slider_MNY, dropdown_TLT], fn=fn_all_life,
                  outputs=[txt_result, txt_summary])

    gr.HTML('<center><h1> 今人不见古时月，今月曾经照古人 </h1> </center>')

    with gr.Row():
        gr.Markdown(
            '''
            江畔何人初见月？江月何年初照人？

            人生代代无穷已，江月年年望相似。

            不知江月待何人，但见长江送流水。

            不知你在体验完第二人生之后，是否找到你想要的人生呢？

            如果没有的话，不妨和小光一起了解诗人的一生吧。

            古今虽有不同，但诗人或许也有和你一样的烦恼呢？

            也许当你看完他们的一生，才会真正理解诗歌中蕴含的哲理~

            多一份豁达，少一些遗憾，学会与不完美的自己和解。
            '''
        )
        gr.Image("imgs/poets.png", width=850, height=550, scale=2)

    gr.ChatInterface(fn=echo,
                     examples=["请介绍一下你自己", "请介绍一下李白的生平", "请介绍一下杜甫的生平"],
                     title="时光机")

demo.launch()
