#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('987654321.png', self.rect.centerx, self.rect.top, 50, 55, 10)
        bullets.add(bullet)





class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,700-80)
            lost += 1 






player = Player('123456789.png', 375, 400, 80, 100, 5)
bullet = Bullet('987654321.png', 375, 400, 10, 20, 5 )

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
    monster = Enemy('din.png', randint(0,700-80), 0, 80, 50, 3)
    monsters.add(monster)




mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Стрелялка-Убивалка')

#задай фон сцены
backgound = transform.scale(image.load('qwertyui.jpg'), (700,500))

#Счетчик фпс
clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont('Calibri', 30)
font2 = font.SysFont('Gabriola', 70)
win_text = font2.render('победа', True, (255, 255, 255))
lose_text = font2.render('поражение', True, (255, 255, 255))


game = True
score = 0
finish = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finish:
        text_lose = font1.render('Пропущено: ' + str(lost) , True, (255, 255, 255))
        text_score = font1.render('Счет: ' + str(score) , True, (255, 255, 255))
        sprite_list = sprite.spritecollide(player, monsters, False)


        if sprite.groupcollide(bullets, monsters, True, True):
            score += 1 
            monster = Enemy('din.png', randint(0, 700 - 80), 0, 80, 50, 3)
            monsters.add(monster) 

        if sprite.groupcollide(bullets, monsters, True, True):
            window.blit(win_text, (150, 250)) 
            finish = True


        window.blit(backgound, (0,0))
        window.blit(text_score, (0, 0))
        window.blit(text_lose, (0, 20))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()

        if sprite_list or lost >= 7:
            window.blit(lose_text, (250, 250))
            finish = True

        if score >= 10:
            window.blit(win_text, (250, 250))
            finish = True




    display.update()
    clock.tick(FPS)