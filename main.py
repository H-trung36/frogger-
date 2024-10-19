import pygame, sys, random
from object import *
from frog import *
from lane import *
import sys
import tkinter as tk


class Game:
    def __init__(self, screen_dimensions, screen_caption, screen_color):
        pygame.init()
        pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption(screen_caption)

        self.screen_color = screen_color
        self.DISPLAY = pygame.display.get_surface()

        # sprite group
        self.object_group = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()
        self.frog_group = pygame.sprite.Group()

        self.all_group = [self.object_group, self.car_group, self.river_group, self.frog_group]

        self.river_speed = {}
        self.assetSetup()  # Setup assets for game objects

        # Bắt đầu phát nhạc nền
        self.play_music("assets/mango-sundive-249556.mp3") 

    def assetSetup(self):
        Object((0, 0), (672, 768), "assets/background.png", self.object_group)

        # lane
        speeds = [-1.25, -1, -.75, -.5, -.25, .25, .5, .75, 1, 1.25]
        random.shuffle(speeds)

        # river lanes
        for y in range(5):
            y_pos = y * 48 + 144
            new_lane = Lane((0, y_pos), self.river_group, speeds.pop(), "river")
            self.river_speed[y_pos // 48] = new_lane.speed

        # street lanes
        for y in range(5):
            y_pos = y * 48 + 432
            Lane((0, y_pos), self.car_group, speeds.pop(), "street")

        # Frog
        self.frog = Frog((336, 672), (48, 48), "assets/frog/up.png", self.frog_group, [self.car_group, self.river_group], self.river_speed)

    def play_music(self, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  

    def run(self):
        while True:
            self.frog.keyups = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    self.frog.keyups.append(event.key)

            for group in self.all_group:
                for sprite in group:
                    sprite.update()

                group.draw(self.DISPLAY)

            pygame.display.update()


def start_game():
    root.destroy()  # Đóng cửa sổ giao diện khởi động
    game = Game((672, 768), "Frogger!!", (0, 0, 0))  # Khởi tạo game
    game.run()  # Bắt đầu vòng lặp game

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Frogger!")


# Đặt kích thước cửa sổ
window_width = 400
window_height = 300
root.geometry(f"{window_width}x{window_height}")

# Tính toán vị trí để hiển thị ở giữa màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")



# Thêm tiêu đề
label = tk.Label(root, text="Frogger!", font=("Helvetica", 20))
label.pack(pady=20)

# Thêm nút bắt đầu game
start_button = tk.Button(root, text="Bắt đầu", command=start_game, font=("Helvetica", 14))
start_button.pack(pady=10)

# Thêm nút thoát
exit_button = tk.Button(root, text="Thoát", command=sys.exit, font=("Helvetica", 14))
exit_button.pack(pady=10)

# Chạy vòng lặp chính
root.mainloop()

