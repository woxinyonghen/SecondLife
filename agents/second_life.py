import random

import numpy as np
import json
import math


# 游戏主体
class game_control(object):
    # 初始化
    def __init__(self):
        super().__init__()
        # 加载年龄数据
        with open('data/zh-cn/age.json', encoding='utf-8') as f:
            self.age_data = json.load(f)

        # 加载事件数据
        with open('data/zh-cn/events.json', encoding='utf-8') as f:
            self.events_data = json.load(f)

        # 加载天赋数据
        with open('data/zh-cn/talents.json', encoding='utf-8') as f:
            self.talents_data = json.load(f)

        # 随机分配20点给颜值、智力、体质和家境
        w = np.random.rand(4)
        w_exp = np.exp(w)
        w = w_exp / w_exp.sum() * 20
        w = w.round().astype('int').tolist()

        # 玩家信息
        self.player_info = {
            'CHR': w[0],  # 颜值 charm CHR
            'INT': w[1],  # 智力 intelligence INT
            'STR': w[2],  # 体质 strength STR
            'MNY': w[3],  # 家境 money MNY
            'SPR': 5,  # 快乐 spirit SPR
            'LIF': 0,  # 生命 life LIF
            'TLT': [],  # 天赋 talent TLT
            'EVT': [],  # 事件 event EVT
        }

        self.random_talents = self.generate_random_talents()

        self.all_text = []

    def generate_random_talents(self):
        candidate = [str(i) for i in range(1001, 1146)]
        ids = random.sample(candidate, 5)
        result = [self.talents_data[i]['name'] + "【" + self.talents_data[i]['description'] + "】" for i in ids]
        return result

    # 规则检查
    def check_rules(self, sentence):
        CHR = self.player_info['CHR']
        INT = self.player_info['INT']
        STR = self.player_info['STR']
        MNY = self.player_info['MNY']
        SPR = self.player_info['SPR']
        LIF = self.player_info['LIF']
        AGE = self.player_info['LIF']
        TLT = self.player_info['TLT']
        EVT = self.player_info['EVT']

        # 事件
        while sentence.find('EVT') != -1:
            start_pos = sentence.find('EVT')
            s_pos = sentence.find('[', start_pos)
            e_pos = sentence.find(']', start_pos)
            end_pos = e_pos
            evt_list = eval(sentence[s_pos: e_pos + 1])
            flag = False
            for evt in evt_list:
                if str(evt) in EVT:
                    flag = True
            if sentence[start_pos + 3] == '?':
                flag = flag
            else:
                flag = not flag
            sentence = sentence[:start_pos] + str(flag) + sentence[end_pos + 1:]

        # 天赋
        while sentence.find('TLT') != -1:
            start_pos = sentence.find('TLT')
            s_pos = sentence.find('[', start_pos)
            e_pos = sentence.find(']', start_pos)
            end_pos = e_pos
            tlt_list = eval(sentence[s_pos: e_pos + 1])
            flag = False
            for tlt in tlt_list:
                if str(tlt) in TLT:
                    flag = True
            if sentence[start_pos + 3] == '?':
                flag = flag
            else:
                flag = not flag
            sentence = sentence[:start_pos] + str(flag) + sentence[end_pos + 1:]

        while sentence.find('!') != -1:
            start_pos = sentence.find('!') - 3
            s_pos = sentence.find('[', start_pos)
            e_pos = sentence.find(']', start_pos)
            end_pos = e_pos
            unknown_list = eval(sentence[s_pos: e_pos + 1])
            unknown_value = eval(sentence[start_pos: start_pos + 3])
            if unknown_value in unknown_list:
                flag = False
            else:
                flag = True
            sentence = sentence[:start_pos] + str(flag) + sentence[end_pos + 1:]

        try:
            return eval(sentence)
        except:
            try:
                return eval(sentence + ')')
            except:
                return eval(sentence[:-1])

    # 获取事件列表
    def get_events_list(self, age):
        events = []
        weight = []
        for item in self.age_data[str(age)]['event']:
            item = str(item)
            if '*' in item:
                event_id = item.split('*')[0]
                weight_number = float(item.split('*')[1])
                if weight_number >= 99999:
                    continue
                else:
                    pass
            else:
                event_id = item
                weight_number = 1
            flag = True
            if 'include' in self.events_data[event_id]:
                flag = flag and self.check_rules(self.events_data[event_id]['include'])
            if 'exclude' in self.events_data[event_id]:
                flag = flag and not self.check_rules(self.events_data[event_id]['exclude'])

            if flag:
                events.append(event_id)
                weight.append(weight_number)

        return events, weight

    # 选择事件
    def choose_event(self, events, weight):
        w = np.array(weight)
        sample = np.random.choice(events, size=1, p=w / sum(w))
        return sample[0]

    # 执行事件
    def do_event(self, event_id):
        event_text = self.events_data[event_id]['event']
        branch_text = ""
        if 'effect' in self.events_data[event_id]:
            for key in self.events_data[event_id]['effect']:
                if key == 'LIF':
                    self.player_info["LIF"] = self.events_data[event_id]['effect']["LIF"]
                else:
                    self.player_info[key] += self.events_data[event_id]['effect'][key]
        self.player_info['EVT'].append(event_id)
        if 'branch' in self.events_data[event_id]:
            for branch_sentence in self.events_data[event_id]['branch']:
                rule_sentence, branch_event_id = branch_sentence.split(':')
                if self.check_rules(rule_sentence):
                    branch_text = self.do_event(branch_event_id)
                    break
        return event_text + branch_text

    # 得到下一年
    def get_next_year(self):
        year_text = f'{self.player_info["LIF"]}岁：'
        if self.player_info["LIF"] >= 0:
            events, weight = self.get_events_list(self.player_info["LIF"])
            event_id = self.choose_event(events, weight)
            event_text = self.do_event(event_id)
            print_text = year_text + event_text
            self.all_text.append(print_text)
            if self.player_info["LIF"] >= 0:
                self.player_info["LIF"] += 1
        else:
            print_text = ""
        return print_text


if __name__ == "__main__":
    game = game_control()