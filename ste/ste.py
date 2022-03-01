import pygame
import random
import sys
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60

show_menu = True
show_game = False
show_game_lose = False


# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Saving the Earth")
clock = pygame.time.Clock()
img_dir = path.join(path.dirname(__file__), 'img')
background = pygame.image.load("data/back.png")
background_rect = background.get_rect()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/hero.png')
        pygame.mixer.init()
        pygame.mixer.music.load("data/normil.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/meteorite.png')
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 1.5 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/vistrel123.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


def terminate():
    sys.exit()

def main():
    if show_menu is True:
        start_screen()
    if show_game is True:
        game()
    if show_game_lose:
        lose()


def start_screen():
    global show_menu, show_game
    screen.fill((222, 189, 78))
    # здесь надо написать название файла и всё
    fon = pygame.transform.scale(pygame.image.load('data/fon123.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    draw_text(screen, 'Saving-the-Earth', 30, 250, 20)
    draw_text(screen, 'Для старты игры нажмите на экран', 20, 150, 100)
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                show_menu = False
                show_game = True
                return ''
        pygame.display.flip()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def game():
    global show_game, show_game_lose
    score = 0
    # Цикл игры
    running = True
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    pygame.mixer.music.pause()
                    # pygame.mixer.music.stop()
                elif event.key == pygame.K_2:
                    pygame.mixer.music.unpause()
                    # pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(0.1)
                elif event.key == pygame.K_3:
                    pygame.mixer.music.unpause()
                    # pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(1)

        # Обновление
        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        # Проверка, не ударил ли моб игрока
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            show_game_lose = True
            show_game = False
            running = False
            return ''

        # Рендеринг
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

def lose():
    global show_game_lose
    screen.fill((222, 189, 78))
    fon = pygame.transform.scale(pygame.image.load('data/gameover.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    draw_text(screen, 'Saving-the-Earth', 30, 250, 20)
    while show_game_lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()

main()