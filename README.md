# 第二人生


<p align="center">
  <a href="https://github.com/woxinyonghen/SecondLife/">
    <img src="imgs/logo.jpg" alt="Logo" width="30%">
  </a>

<h3 align="center">第二人生</h3>
  <p align="center">
    <br />
    <a href="https://github.com/woxinyonghen/SecondLife/"><strong>探索本项目的文档 »</strong></a>
  </p>

</p>

<!-- 本篇README.md面向开发者 -->

**第二人生** 是一款基于[InternLM2](https://github.com/InternLM/InternLM) 指令微调后的模型开发，包含 **人生轨迹-人生报告-诗人生平**的兼顾趣味性和知识性的应用。在这里你既可以体验到人生重开的多样性，也能得到大模型给你的人生报告，还能体会到诗人生平的厚重感。如果您觉得还不错的话，欢迎star~~~

## 目录

- [文件结构](#目录结构)
- [数据构建](#数据构建)
- [微调指南](#微调指南)
- [部署指南](#部署指南)

###### 目录结构
```
├─agents    // 游戏交互
├─data      
│  └─zh-cn  // 游戏数据
│     └─achievement.json // 成就
│     └─age.json         // 年龄
│     └─events.json      // 事件
│     └─talents.json     // 天赋
│  └─data_generate.py    // 微调数据集生成
│  └─life_of_poets.csv   // 处理后的csv格式的微调数据
│  └─life_of_poets_copy.csv      // 生成csv格式的微调数据
│  └─csv2json.py         // csv格式的微调数据转成json格式的数据
│  └─poets.txt           // 诗人集合
├─imgs      // 图片目录
├─models    // 模型目录
│  └─internlm2_chat_7b_sdk.py // 模型推理接口文件
├─requirements.txt      // 环境依赖
└─run.py    // 启动文件
└─README.md // 说明文档

```


###### 数据构建

```
1. 编写poets.txt，每行为一位名人的姓名。

2. 运行data_generate.py，调用文心一言接口生成诗人生平的原始数据life_of_poets_copy.csv。

3. 人工对原始数据清洗处理得到life_of_poets.csv。

4. 调用csv2json.py将处理后的数据转成json格式的dataset.json。

```

###### 模型微调
OpenXLab模型链接：https://openxlab.org.cn/models/detail/%E6%98%9F%E8%BE%B0/The_History

详见docs/诗人生平微调全流程.md

##### 模型部署

OpenXLab链接：https://openxlab.org.cn/apps/detail/%E6%98%9F%E8%BE%B0/Second_Life

```
pip install-r requirements.txt
python run.py
```
