import pygame
import random
from datetime import datetime, timezone

utc_time = datetime.now(timezone.utc)
pygame.init()
pygame.mixer.init()
from pygame.locals import *

class NameManager:
    def __init__(self):
        self.clean_lines = []
        self.numbers = []
        self.number = "0"
        self.all_names = []

    def open_file(self):
        try:
            with open("name_list.txt", "r", encoding="utf-8") as f:
                self.all_names = [line.strip().strip('"') for line in f.readlines()]
                self.clean_lines = self.all_names.copy()
        except Exception as e:
            print(f"读取文件失败: {e}")
            self.all_names = []
            self.clean_lines = []

    def update_number(self):
        self.number = "".join(map(str, self.numbers)) or "0"

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((1800, 1000))
        pygame.display.set_caption("抽人")
        self.background = pygame.image.load("background.png")
        self.font = pygame.font.Font('STKAITI.TTF', 100)
        self.clock = pygame.time.Clock()

        # 初始化音乐
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # 数据初始化
        self.name_manager = NameManager()
        self.name_manager.open_file()
        self.run_condition = "preparing"
        self.attention = ""
        self.text_under = "按空格键选人"
        self.text1 = ""
        self.text2 = ""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.run_condition == "ready":
                        # 重置状态
                        self.run_condition = "preparing"
                        self.name_manager.clean_lines = self.name_manager.all_names.copy()
                elif self.run_condition == "preparing":
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        self.name_manager.numbers.append(event.key - pygame.K_0)
                    elif event.key == K_BACKSPACE:
                        self.name_manager.numbers = []
                    elif event.key in (K_RETURN, K_KP_ENTER):
                        self._handle_enter()
        return True

    def _handle_enter(self):
        self.name_manager.update_number()
        target = int(self.name_manager.number)

        if 1 <= target <= 6:
            if len(self.name_manager.clean_lines) >= target:
                self.run_condition = "ready"
            else:
                self.attention = "名字不足，已重置"
                self.name_manager.clean_lines = self.name_manager.all_names.copy()
        else:
            self.attention = "请输入1-6之间的数字"

    def draw_ui(self):
        self.screen.blit(self.background, (0, 0))
        if self.run_condition == "preparing":
            self._draw_prepare_ui()
        else:
            self._draw_result_ui()
        pygame.display.update()

    def _draw_prepare_ui(self):
        self._render_text([900, 65], "阿洛娜提醒你")
        self._render_text([700, 265], "老师，你今天想要几个呢？")
        self._render_text([1100, 465], f"抽{self.name_manager.number}个")
        self._render_text([900, 665], self.attention)

    def _draw_result_ui(self):
        if self.name_manager.number.isdigit():
            target = int(self.name_manager.number)
            available = self.name_manager.clean_lines
            if len(available) < target:
                available = self.name_manager.all_names.copy()

            names = random.sample(available, min(target, len(available)))
            self.name_manager.clean_lines = [n for n in available if n not in names]

            # 分割显示
            self.text1 = " ".join(names[:3])
            self.text2 = " ".join(names[3:])

            # 记录日志
            with open("log.txt", "a", encoding="utf-8") as f:
                for name in names:
                    f.write(f"UTC时间 {datetime.now(timezone.utc)} 抽到 {name}\n")

        self._render_text([900, 65], "阿洛娜提醒你")
        self._render_text([700, 250], self.text1)
        self._render_text([700, 350], self.text2)
        self._render_text([1100, 635], "到你了")

    def _render_text(self, pos, text):
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, pos)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw_ui()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()

