随机抽人程序 - 开源说明
项目概述
这是一个基于 Pygame 的随机抽人程序，专为课堂或活动场景设计。程序可以从预设名单中随机抽取指定数量的参与者，并记录抽取日志。

功能特点
从文本文件读取名单（支持 UTF-8 编码）

随机抽取 1-6 名参与者

可视化界面显示抽取结果

背景音乐播放与控制

抽取记录保存到日志文件

简洁直观的用户界面

运行要求
Python 3.x

Pygame 库

安装与使用
安装依赖：

text
pip install pygame
准备资源文件：

name_list.txt - 参与者名单（每行一个名字）

background.png - 背景图片

music.mp3 - 背景音乐

STKAITI.TTF - 中文字体文件

运行程序：

text
python main.py
操作说明
启动程序后，输入需要抽取的人数（1-6）

按回车键确认

按空格键开始/停止随机抽取

抽取结果将显示在屏幕上并保存到日志文件

文件结构
text
main.py          # 主程序
name_list.txt    # 参与者名单
background.png   # 背景图片
music.mp3        # 背景音乐
STKAITI.TTF      # 字体文件
log.txt          # 抽取记录（自动生成）
代码说明
程序主要包含两个类：

file 类：处理文件操作（读取名单、选择随机名字）

window 类：管理界面显示

主循环处理用户输入和程序状态切换，实现交互式抽取过程。

开源协议
本项目采用 MIT 协议开源，允许自由使用、修改和分发。

贡献指南
欢迎提交 Issue 和 Pull Request 来改进这个项目。

作者信息
由 Muhongda开发。


