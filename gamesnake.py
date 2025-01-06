import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import pygame, sys, random
from pygame.math import Vector2

# إعدادات قاعدة البيانات
def connect_db():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        score INTEGER DEFAULT 0
                    )''')
    conn.commit()
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'score' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN score INTEGER DEFAULT 0")
    conn.commit()
    conn.close()

def load_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, score FROM users")
    users = {row[0]: {'password': row[1], 'score': row[2]} for row in cursor.fetchall()}
    conn.close()
    return users

def save_users(username, password, score=0):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, score) VALUES (?, ?, ?)", (username, password, score))
    conn.commit()
    conn.close()

def update_score(username, score):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET score = ? WHERE username = ?", (score, username))
    conn.commit()
    conn.close()

def get_score(username):
    users = load_users()
    if username in users:
        return users[username]['score']
    return 0

def login(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True
    return False

def sign_up(username, password):
    users = load_users()
    if username in users:
        return False
    save_users(username, password)
    return True

# نافذة اللعبة باستخدام Pygame
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        image_size = (20, 20)
        self.head_up = pygame.transform.scale(pygame.image.load('GIF/head_up.png').convert_alpha(), image_size)
        self.head_down = pygame.transform.scale(pygame.image.load('GIF/head_down.png').convert_alpha(), image_size)
        self.head_right = pygame.transform.scale(pygame.image.load('GIF/head_right.png').convert_alpha(), image_size)
        self.head_left = pygame.transform.scale(pygame.image.load('GIF/head_left.png').convert_alpha(), image_size)
        self.tail_up = pygame.transform.scale(pygame.image.load('GIF/tail_up.png').convert_alpha(), image_size)
        self.tail_down = pygame.transform.scale(pygame.image.load('GIF/tail_down.png').convert_alpha(), image_size)
        self.tail_right = pygame.transform.scale(pygame.image.load('GIF/tail_right.png').convert_alpha(), image_size)
        self.tail_left = pygame.transform.scale(pygame.image.load('GIF/tail_left.png').convert_alpha(), image_size)
        self.body_vertical = pygame.transform.scale(pygame.image.load('GIF/body_vertical.png').convert_alpha(), image_size)
        self.body_horizontal = pygame.transform.scale(pygame.image.load('GIF/body_horizontal.png').convert_alpha(), image_size)
        self.body_tr = pygame.transform.scale(pygame.image.load('GIF/body_tr.png').convert_alpha(), image_size)
        self.body_tl = pygame.transform.scale(pygame.image.load('GIF/body_tl.png').convert_alpha(), image_size)
        self.body_br = pygame.transform.scale(pygame.image.load('GIF/body_br.png').convert_alpha(), image_size)
        self.body_bl = pygame.transform.scale(pygame.image.load('GIF/body_bl.png').convert_alpha(), image_size)
        self.crunch_sound = pygame.mixer.Sound('crunch.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play()
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple1, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self, username):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.username = username
        self.score = get_score(self.username)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fall()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1

    def check_fall(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
         #pygame.quit()
         #sys.exit()
         self.snake.reset()
         update_score(self.username, self.score)
       

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 60)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple1.get_rect(midright=(score_rect.left, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(apple1, apple_rect)

def start_game(username):
    pygame.init()
    global cell_size, cell_number, screen, clock, apple1, game_font
    cell_size = 20
    cell_number = 20
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    apple1 = pygame.image.load('GIF/apple3.jpg').convert_alpha()
    apple1 = pygame.transform.scale(apple1, (cell_size, cell_size))
    game_font = pygame.font.Font('Winter Minie.ttf', 25)
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    main_game = MAIN(username)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
        screen.fill((127, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def handle_login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    if login(username, password):
        messagebox.showinfo("Succès", "Connexion réussie!")
        root.destroy()
        start_game(username)
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def handle_sign_up():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    if sign_up(username, password):
        messagebox.showinfo("Succès", "Inscription réussie! Vous pouvez maintenant vous connecter.")
    else:
        messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")

# نافذة تسجيل الدخول
root = tk.Tk()
root.title("Connexion ou Inscription")
root.geometry("500x500")

image = Image.open("sanke.png")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

tk.Label(root, text="Snake Game", font=("Arial", 24), bg="white", fg="black").pack(pady=10)
tk.Label(root, text="Nom d'utilisateur:", bg="white", fg="black").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)
tk.Label(root, text="Mot de passe:", bg="white", fg="black").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)
login_button = tk.Button(root, text="Se connecter", command=handle_login)
login_button.pack(pady=10)
sign_up_button = tk.Button(root, text="S'inscrire", command=handle_sign_up)
sign_up_button.pack(pady=10)
create_table()
root.mainloop()