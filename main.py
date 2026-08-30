import os
import sys
import pygame
import random
from datetime import datetime, timezone, timedelta
"""课堂随机点名工具 - 抽人"""

# 资源目录：打包后为 exe 所在目录，开发时为脚本目录
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAME_LIST = os.path.join(BASE_DIR, "name_list.txt")   # 名单
LOG_FILE = os.path.join(BASE_DIR, "log.txt")          # 抽人记录
PICKED_FILE = os.path.join(BASE_DIR, "picked.txt")    # 轮次模式：本轮已抽记录
LOG_TZ = timezone(timedelta(hours=8))                 # 日志使用北京时间（东八区）

# 窗口固定放到主显示器中央（避免双屏/记忆位置导致窗口跑到屏幕外）
try:
    _dw, _dh = pygame.display.get_desktop_sizes()[0]
except Exception:
    _dw, _dh = 1920, 1080
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (max(0, (_dw - 1800) // 2), max(0, (_dh - 1000) // 2))

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
        self.all_names = []   # 完整名单（轮次模式用）
        self.picked = []      # 轮次模式：本轮已抽
    def open_file(self):
        try:
            with open(NAME_LIST, "r", encoding="utf-8") as self.file:
                self.lines = self.file.readlines()
                # 去除每行的换行符和首尾双引号（空行不算名字）
                self.clean_lines = [self.line.strip().strip('"') for self.line in self.lines if self.line.strip()]
                self.all_names = self.clean_lines.copy()
        except OSError:
            self.clean_lines = []
            self.all_names = []
    def choose_name(self):
        self.finally_name = random.choice(self.clean_lines)
    def addtion(self):
        self.number =  ""
        for i in self.numbers:
            self.number = self.number + str(i)
        if self.number == "":
            self.number = "0"
    def load_picked(self):
        """读取本轮已抽记录（不存在时视为空）"""
        try:
            with open(PICKED_FILE, "r", encoding="utf-8") as f:
                self.picked = [line.strip() for line in f.readlines() if line.strip()]
        except OSError:
            self.picked = []
    def save_picked(self):
        """保存本轮已抽记录"""
        with open(PICKED_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(self.picked))
    def reset_round(self):
        """开始新一轮：清空已抽记录"""
        self.picked = []
        self.save_picked()
    def round_left(self):
        """轮次模式剩余可抽人数"""
        return len(self.all_names) - len(self.picked)

class window():
    def __init__(self):
        self.background = pygame.image.load(os.path.join(BASE_DIR, "background.png"))
text_under = "按空格键选人"
text1 = ""
text2 = ""
conditions = True


def show_missing_files(missing):
    """资源文件缺失时，弹窗提示而不是直接闪退"""
    pygame.init()
    screen = pygame.display.set_mode((1000, 320))
    pygame.display.set_caption("缺少文件")
    font = pygame.font.SysFont("microsoftyahei,simhei", 28)
    lines = ["缺少文件，请确认以下文件与程序放在同一个文件夹："] + missing + ["（点击关闭后程序退出）"]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.fill((255, 255, 255))
        y = 40
        for line in lines:
            screen.blit(font.render(line, True, (0, 0, 0)), (30, y))
            y += 45
        pygame.display.update()
        pygame.time.Clock().tick(30)


def pretty_log_line(line):
    """日志显示美化：时间/抽到 前后加空格，更好读"""
    line = line.strip()
    line = line.replace("北京时间", "北京时间 ").replace("UTC世界协调时", "UTC世界协调时 ")
    line = line.replace("抽到", " 抽到 ")
    return line


def center_text(screen, font, text, y, color=(0, 0, 0)):
    """水平居中绘制一行文字，返回文本高度"""
    surf = font.render(text, True, color)
    screen.blit(surf, ((1800 - surf.get_width()) // 2, y))
    return surf.get_height()


def draw_panel(screen, rect, color=(255, 255, 255, 190), radius=36):
    """半透明圆角面板"""
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    screen.blit(panel, rect.topleft)


def draw_log_screen(screen, ft_log_t, ft_log_l, ft_log_h, log_lines, scroll, line_h):
    """日志查看窗口：标题栏 + 列表面板，最新在上，可滚动"""
    screen.fill((240, 236, 250))
    # 顶部标题栏
    pygame.draw.rect(screen, (96, 82, 168), pygame.Rect(0, 0, 1800, 88))
    t = ft_log_t.render("抽人记录", True, (255, 255, 255))
    screen.blit(t, (60, 24))
    t2 = ft_log_t.render("最新在上", True, (225, 220, 250))
    screen.blit(t2, (1800 - 60 - t2.get_width(), 24))
    # 操作提示
    hint = ft_log_h.render("按 L 或 ESC 关闭　｜　上下键 / 滚轮滚动", True, (110, 105, 130))
    screen.blit(hint, ((1800 - hint.get_width()) // 2, 108))
    # 列表面板
    panel = pygame.Surface((1560, 780), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 255, 255, 190), panel.get_rect(), border_radius=28)
    screen.blit(panel, (120, 170))
    visible = (780 - 60) // line_h  # 面板内可显示的行数
    start = min(max(0, scroll), max(0, len(log_lines) - visible))
    end = min(len(log_lines), start + visible)
    y = 205
    for i in range(start, end):
        color = (70, 62, 110) if i % 2 == 0 else (110, 105, 130)
        screen.blit(ft_log_l.render(log_lines[i], True, color), (150, y))
        y += line_h
    if not log_lines:
        screen.blit(ft_log_h.render("（还没有任何抽人记录）", True, (150, 145, 170)), (150, 205))
    pygame.display.update()


if __name__ == "__main__":
    # 检查资源文件是否齐全
    missing = [f for f in ("name_list.txt", "background.png", "STKAITI.TTF", "music.mp3")
               if not os.path.exists(os.path.join(BASE_DIR, f))]
    if missing:
        show_missing_files(missing)
        sys.exit(1)

    #音乐
    pygame.mixer.music.load(os.path.join(BASE_DIR, "music.mp3"))
    pygame.mixer.music.set_volume(0.2)

    #算法初始化
    condition = 1 #1为随机抽人 -1为确定人选
    mode = "random"        # random=随机模式  round=轮次模式
    confirm_reset = False  # 是否在"确认重置"状态
    music_on = True        # 音乐播放状态（空格切换）
    text_file = file()
    text_file.open_file()
    text_file.load_picked()
    text_file.choose_name()
    name = []

    #窗口初始化
    screen = pygame.display.set_mode((1800,1000))#创建窗口

    background = pygame.image.load(os.path.join(BASE_DIR, 'background.png'))
    pygame.display.set_caption("抽人")#
    FONT_PATH = os.path.join(BASE_DIR, 'STKAITI.TTF')
    ft_title = pygame.font.Font(FONT_PATH, 60)    # 顶部标题
    ft_ask = pygame.font.Font(FONT_PATH, 64)      # 提问
    ft_num = pygame.font.Font(FONT_PATH, 120)     # 抽N个
    ft_note = pygame.font.Font(FONT_PATH, 44)     # 提示文字
    ft_small = pygame.font.Font(FONT_PATH, 40)    # 底部模式信息条
    ft_name = pygame.font.Font(FONT_PATH, 84)     # 抽中的名字
    ft_arr = pygame.font.Font(FONT_PATH, 72)      # "同学，到你了！"
    ft_under = pygame.font.Font(FONT_PATH, 44)    # 底部提示
    ft_log_t = pygame.font.Font(FONT_PATH, 38)    # 日志标题
    ft_log_l = pygame.font.Font(FONT_PATH, 34)    # 日志行
    ft_log_h = pygame.font.Font(FONT_PATH, 28)    # 日志辅助提示
    # 配色（浅紫背景）
    C_TITLE = (96, 82, 168)    # 紫：标题
    C_TEXT = (70, 62, 110)     # 深紫蓝：正文
    C_HL = (108, 92, 231)      # 亮紫：强调
    C_GRAY = (110, 105, 130)   # 灰：辅助
    C_WARN = (224, 118, 60)    # 橙：提示/警示
    clock = pygame.time.Clock()

    # 播放音乐（循环播放）
    pygame.mixer.music.play(-1)

    attention = ""

    black = pygame.Color(0,0,0)
    off_open = True
    run_condition = "preparing"
    show_log = False
    log_scroll = 0
    log_lines = []
    LOG_LINE_H = 46
    while off_open:
        # ---- 日志查看界面 ----
        if show_log:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    off_open = False
                    break
                elif event.type == KEYDOWN:
                    if event.key in (K_l, K_ESCAPE):
                        show_log = False
                    elif event.key in (K_PAGEUP, K_UP):
                        log_scroll = max(0, log_scroll - 10)
                    elif event.key in (K_PAGEDOWN, K_DOWN):
                        log_scroll += 10
                elif event.type == MOUSEWHEEL:
                    log_scroll = max(0, log_scroll - event.y * 3)
            if not off_open:
                continue
            draw_log_screen(screen, ft_log_t, ft_log_l, ft_log_h, log_lines, log_scroll, LOG_LINE_H)
            clock.tick(60)
            continue

        screen.blit(background, (0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                off_open = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    off_open = False
                    break
                # L 键打开日志查看
                if event.key == K_l:
                    show_log = True
                    log_scroll = 0
                    try:
                        with open(LOG_FILE, "r", encoding="utf-8") as log_f:
                            log_lines = [pretty_log_line(line) for line in reversed(log_f.readlines())]
                    except OSError:
                        log_lines = []
                # 空格只在"确定人数后"抽人/暂停音乐，准备界面误触无副作用
                if event.key == K_SPACE and run_condition == "ready":
                    condition = -condition
                    music_on = not music_on
                    try:
                        # 用静音代替 pause/unpause：绕开 SDL_mixer 暂停状态机的死锁风险
                        pygame.mixer.music.set_volume(0.2 if music_on else 0.0)
                    except pygame.error:
                        music_on = True
                if run_condition == "preparing":
                    if event.key == K_m:
                        # M 键切换模式
                        confirm_reset = False
                        mode = "round" if mode == "random" else "random"
                        attention = "已切换到" + ("轮次模式" if mode == "round" else "随机模式")
                    elif event.key == K_r and mode == "round":
                        # R 键请求重置本轮（轮次模式）
                        confirm_reset = True
                        attention = ""
                    elif confirm_reset:
                        # 确认重置状态：Y 确认，其他键取消
                        if event.key == K_y:
                            text_file.reset_round()
                            confirm_reset = False
                            attention = "已开始新一轮"
                        else:
                            confirm_reset = False
                            attention = "已取消重置"
                    else:
                        # 主键盘 1-9 与小键盘 1-9 都可以输入
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            if len(text_file.numbers) < 2:  # 最多2位，防止溢出屏幕
                                text_file.numbers.append(event.key - pygame.K_0)
                                attention = ""
                        elif 89 <= event.scancode <= 97:
                            # 小键盘 1-9（scancode=物理键位，NumLock 开关都有效）
                            if len(text_file.numbers) < 2:
                                text_file.numbers.append(event.scancode - 88)
                                attention = ""
                        elif event.key == K_BACKSPACE:
                            if text_file.numbers:  # 退格删除最后一位
                                text_file.numbers.pop()
                            attention = ""
                        elif event.key in (K_RETURN, K_KP_ENTER):
                            number = int(text_file.number)
                            if 1 <= number <= 6:
                                if mode == "round" and text_file.round_left() < number:
                                    attention = "本轮剩余%d人，不够抽%d个，按R重置" % (text_file.round_left(), number)
                                else:
                                    run_condition = "ready"
                            elif number == 0:
                                attention = "醒醒老师，没有人"
                            else:
                                attention = "老师，最多6个哦"
                                text_file.numbers = []

        if not off_open:
            continue
        # 名单抽空后重新读取（随机模式；运行中修改 name_list.txt 也会在此时生效）
        if len(text_file.clean_lines) == 0 and mode == "random":
            text_file.open_file()

        if run_condition == "preparing":
            text_file.addtion()
            center_text(screen, ft_title, "阿洛娜提醒你", 50, C_TITLE)
            draw_panel(screen, pygame.Rect(450, 230, 900, 430))
            center_text(screen, ft_ask, "老师，你今天想要几个呢？", 290, C_TEXT)
            center_text(screen, ft_num, "抽 " + str(text_file.number) + " 个", 400, C_HL)
            center_text(screen, ft_note, attention, 585, C_WARN)
            # 底部模式信息条
            if confirm_reset:
                center_text(screen, ft_small, "确认开始新一轮？按 Y 确认 / 其他键取消", 872, C_WARN)
            elif mode == "round":
                center_text(screen, ft_small,
                            "当前模式：轮次模式　本轮已抽 %d / %d　｜　M 切换模式　R 重置本轮" % (len(text_file.picked), len(text_file.all_names)),
                            872, C_GRAY)
            else:
                center_text(screen, ft_small, "当前模式：随机模式　｜　M 切换模式", 872, C_GRAY)
        elif run_condition == "ready":


            if condition == 1:
                text_under = "按空格键选人"
                text1 = ""
                text2 = ""
                name = []
                check_name = []

                if mode == "round":
                    # 轮次模式：只从"全名单 - 本轮已抽"里抽
                    available_names = [n for n in text_file.all_names if n not in text_file.picked]
                    target_count = min(int(text_file.number), len(available_names))
                else:
                    # 随机模式：从剩余名单里抽，不足时重新读取
                    if len(text_file.clean_lines) < int(text_file.number):
                        text_file.open_file()
                    available_names = text_file.clean_lines.copy()
                    target_count = min(int(text_file.number), len(available_names))

                # 随机选取不重复的名字
                if target_count > 0:
                    name = random.sample(available_names, target_count)
                else:
                    name = []

                if int(len(name)) > 3:
                    for z in range(3):
                        text1 = text1 + " " + name[z]
                    for z in range(3, len(name)):
                        text2 = text2 + " " + name[z]
                elif 0 < int(len(name)) < 4:
                    for z in range(len(name)):
                        text1 = text1 + " " + name[z]


                print(text1,text2)
                the_name = ""




            elif condition == -1:
                for i in range(len(name)):
                    the_name = name[i]
                    logged = False
                    if mode == "round":
                        # 轮次模式：加入本轮已抽并保存
                        if the_name not in text_file.picked:
                            text_file.picked.append(the_name)
                            text_file.save_picked()
                            logged = True
                    elif the_name in text_file.clean_lines:
                        # 随机模式：从剩余名单移除
                        text_file.clean_lines.remove(the_name)
                        logged = True
                    if logged:
                        text_under = "按空格键继续"
                        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                            log_file.write("北京时间"+str(datetime.now(LOG_TZ))+"抽到"+the_name+"\n")

            #screen.blit(background,(0,0))
            center_text(screen, ft_title, "阿洛娜提醒你", 50, C_TITLE)
            draw_panel(screen, pygame.Rect(450, 200, 900, 480))
            if text2.strip():
                center_text(screen, ft_name, text1.strip(), 270, C_TEXT)
                center_text(screen, ft_name, text2.strip(), 400, C_TEXT)
            else:
                center_text(screen, ft_name, text1.strip(), 330, C_TEXT)
            center_text(screen, ft_arr, "同学，到你了！", 735, C_HL)
            center_text(screen, ft_under, text_under, 870, C_GRAY)
        pygame.display.update()
