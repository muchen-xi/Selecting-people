import pygame
import random
from datetime import datetime, timezone


utc_time = datetime.now(timezone.utc)
print(utc_time)  # 输出示例：2024-06-07 06:20:34.567890+00:00
pygame.init()
pygame.mixer.init()
from pygame.locals import*

class file():
    def __init__(self):
        self.line = 0
        self.file = 0
        self.lines = 0
        self.finally_name = 0
        self.clean_lines = 0
        self.numbers = []
        self.number = "0"
    def open_file(self):
        with open("name_list.txt", "r",encoding="utf-8") as self.file:
            self.lines = self.file.readlines()
            if self.lines == "":
                pass
            else:
            # 去除每行的换行符和首尾双引号

                self.clean_lines = [self.line.strip().strip('"') for self.line in self.lines]
    def choose_name(self):
        self.finally_name = random.choice(self.clean_lines)
    def addtion(self):
        self.number =  ""
        for i in self.numbers:
            self.number = self.number + str(i)
        if self.number == "":
            self.number = "0"

class window():
    def __init__(self):
        self.background = pygame.image.load("background.png")
text_under = "按空格键选人"
text1 = ""
text2 = ""
conditions = True
if __name__ == "__main__":
    #音乐
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.2)

    #算法初始化
    condition = 1 #1为随机抽人 -1为确定人选
    text_file = file()
    text_file.open_file()
    text_file.choose_name()
    name = []

    #窗口初始化
    screen = pygame.display.set_mode((1800,1000))#创建窗口

    background = pygame.image.load('background.png')
    pygame.display.set_caption("抽人")#
    ft = pygame.font.Font('STKAITI.TTF', 100)

    # 播放音乐（循环播放）
    pygame.mixer.music.play(-1)

    def write_text(postion, text):
        title = ft.render(text, True, [0, 0, 0])
        screen.blit(title, postion)
    attention = ""

    black = pygame.Color(0,0,0)
    off_open = True
    run_condition = "preparing"
    while off_open:
        screen.blit(background, (0, 0))
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                off_open = False
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    condition = -condition
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if run_condition == "preparing":
                    if event.key == pygame.K_1 or  event.key == pygame.K_KP_1:
                        text_file.numbers.append(1)
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                        text_file.numbers.append(2)
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                        text_file.numbers.append(3)
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                        text_file.numbers.append(4)
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                        text_file.numbers.append(5)
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                        text_file.numbers.append(6)
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                        text_file.numbers.append(7)
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                        text_file.numbers.append(8)
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                        text_file.numbers.append(9)
                    elif event.key == pygame.K_BACKSPACE:
                        text_file.numbers = []
                    elif event.key in (K_RETURN, K_KP_ENTER):
                        if 1 == int(text_file.number) or (int(text_file.number) > 1 and 6 > int(text_file.number)) or 6 == int(text_file.number) :
                            run_condition = "ready"
                        elif int(text_file.number) == 0:
                            attention = "醒醒老师，没有人"

                        else:
                            attention = "老师，最多6个哦"
                            text_file.numbers = []


        with open("name_list.txt", "r", encoding="utf-8") as file:

            one_name = file.readlines()
            if one_name == "":
                pass
            else:
                all_name = [line.strip().strip('"') for line in one_name]
        if len(text_file.clean_lines) == 0:
            text_file.clean_lines = all_name

        if run_condition == "preparing":
            text_file.addtion()
            write_text([900, 65], "阿洛娜提醒你")
            write_text([700, 265], "老师，你今天想要几个呢？")
            write_text([1100, 465], "抽"+str(text_file.number)+"个")
            write_text([900,665],attention)
        elif run_condition == "ready":


            if condition == 1:
                text_under = "按空格键选人"
                text1 = ""
                text2 = ""
                name = []
                check_name = []

                if len(text_file.clean_lines) < int(text_file.number):
                    text_file.clean_lines = all_name


                target_count = int(text_file.number)

                # 检查可用名字数量
                available_names = text_file.clean_lines.copy()
                if target_count > len(available_names):
                    text_file.clean_lines = all_name


                # 随机选取不重复的名字
                if target_count > 0:
                    name = random.sample(available_names, target_count)
                else:
                    name = []
                b1=-1
                b2=-1
                if int(len(name)) > 3:
                    for z in range(3):
                        text1 = text1 + " " + name[z]
                        b1=b1+1
                    for z in range(3, int(text_file.number)):
                        text2 = text2 + " " + name[z]
                        b2 =b2+1
                elif 0 < int(text_file.number) < 4:
                    for z in range(int(text_file.number)):
                        text1 = text1 + " " + name[z]
                        b1 = b1 + 1
                a1 = len(text1)-b1
                a2 = len(text2)-b2


                print(text1,text2)
                the_name = ""




            elif condition == -1:
                for i in range(int(text_file.number)):

                    the_name = name[i]


                    if the_name in text_file.clean_lines:
                        text_file.clean_lines.remove(the_name)
                        text_under = "按空格键继续"
                        with open("log.txt", "a", encoding="utf-8") as log_file:
                            log_file.write("UTC世界协调时"+str(datetime.now(timezone.utc))+"抽到"+the_name+"\n")

            #screen.blit(background,(0,0))
            write_text([900,65],"阿洛娜提醒你")
            #write_text([1000,250],the_name+"同学")
            write_text([(1250-(100*a1-50*b1)/2), 250], text1)
            write_text([1250-(100*a2-50*b2)/2, 350], text2)
            write_text([1100, 450], "同学")

            write_text([1100,635],"到你了")
            write_text([1000,750],text_under)

        pygame.display.update()
