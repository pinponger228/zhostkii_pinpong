from pygame import *
from random import randint

'''Необходимые классы'''
lost = 0
image_bullet = "A.png"
# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
class Player(GameSprite):
    def update(self):
            keys = key.get_pressed()
            if keys[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_width - 50:
                self.rect.x += self.speed
    def fire(self):
            bullet = Bullet("A.jpg", self.rect.centerx, self.rect.top, -15)
            #bullet = Bullet("A.jpg", 80, 100, -15)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80) 
            self.rect.y = 0
            lost += 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 70) 
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_height = 900
win_width = 500

ship = Player("slide-3.jpg", 10, win_height - 270,15)
monsters = sprite.Group()
for i in range (1,6):
    monster = Enemy("666.jpg",randint(80, win_width - 80), -40, 20)
    monsters.add(monster)

monster = Enemy("boss.png",randint(90, win_width - 80), -30, 20)
monsters.add(monster)



bullets = sprite.Group()
                
# Игровая сцена:
win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Не стреляй в Светлану!!!")
background = transform.scale(image.load("pon.jpg"), (win_width, win_height))

font.init()
font1 = font.SysFont("Arial", 35)

game = True
finish = False
clock = time.Clock()
FPS = 60
 
# музыка
mixer.init()
mixer.music.load('OOO.mp3')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire() 

    if not finish:  
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()

        monster.update()
        monster.reset()

        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True , True)
        for c in collides:
            score = + 1
            monster = Enemy("666.jpg", randint(80, win_width - 80), -40, 20)
            monsters.add(monster)
            #monster = Enemy("boss.png", randint(80, win_width - 90), -50, 30)
            #monsters.add(monster)

            
        text_lose = font1.render(
"Пропущено Светлан:" + str(lost), 1, (255 , 255, 255)
)
        window.blit(text_lose, (0,0))
            
    time.delay(50)
    display.update()
    clock.tick(FPS)
