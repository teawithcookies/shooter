#Создай собственный Шутер!
from random import randint
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Шутер')
mixer.init()
# mixer.music.load('space.ogg') # Закомментировал, чтобы код запускался без файлов

win_width = 700
win_height = 500
font.init()
font2 = font.SysFont('Arial', 42)
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = width
        self.height = height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        b = Bullet('bullet.png', 10, self.rect.x + 30, self.rect.y, 20, 100)
        bullets.add(b)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -100
            self.rect.x = randint(100, 600)
            global lose
            lose += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -100
            self.rect.x = randint(100, 600)
            health = 2

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


# Переменные
lose = 0
score = 0
health = 2
finish = False

# --- ПЕРЕМЕННЫЕ ДЛЯ КУЛДАУНА ---
num_fire = 0          # Счетчик выстрелов
rel_time = False      # Флаг перезарядки
# ------------------------------

rocket = Player('rocket.png', 5, 100, 400, 60, 100)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    m = Enemy('ufo.png', randint(200, 300) / 100, randint(100, 600), -100, 100, 60)
    monsters.add(m)
for i in range(2):    
    a = Asteroid('asteroid.png', 5, randint(100, 600),-100, 100, 100)
    asteroids.add(a)


bullets = sprite.Group()
clock = time.Clock()
FPS = 60

game = True
while game:
    window.blit(background, (0, 0))
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # Проверка: если выстрелов < 5 и мы не на перезарядке
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    rocket.fire()
                
                # Если сделали 5 выстрелов, включаем таймер
                if num_fire >= 10 and rel_time == False:
                    last_time = time.get_ticks() # Засекаем время
                    rel_time = True

    if not finish:
        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        rocket.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)

        # ЛОГИКА ПЕРЕЗАРЯДКИ
        if rel_time == True:
            now_time = time.get_ticks() # Текущее время
            if now_time - last_time < 3000: # Пока не прошло 3 секунды
                reload_text = font2.render('RELOADING...', True, (255, 0, 0))
                window.blit(reload_text, (260, 450))
            else:
                num_fire = 0   # Сбрасываем счетчик
                rel_time = False # Выключаем перезарядку

       
        text_lose = font2.render(f'Пропущено: {lose}', True, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        text_score = font2.render(f'Сбито: {score}', True, (255, 255, 255))
        window.blit(text_score, (10, 60))

        
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        monster_list = sprite.groupcollide(asteroids, bullets, False, True)
        for s in sprites_list:
            score += 1
            m = Enemy('ufo.png', randint(200, 300) / 100, randint(100, 600), -100, 100, 60)
            monsters.add(m)
        for s in sprites_list:
            health -= 1
            if health == 0:
                score += 1
                
                
            
        sprite_list = sprite.spritecollide(rocket, monsters, False)
        
    
        if score >= 10:
            finish = True
            window.blit(font2.render('YOU WIN!', True, (255, 255, 255)), (255, 255))
        
        if len(sprite_list) > 0 or lose >= 3:
            finish = True
            window.blit(font2.render('YOU LOSE!', True, (255, 255, 255)), (255, 255))

        display.update()
    
    clock.tick(FPS)