
from random import randint
from pygame import *
window = display.set_mode((700,500))
galaxy = transform.scale(image.load('galaxy.jpg'),(700,500))
class GameSprite(sprite.Sprite):
    def __init__(self,image_name,x,y,speed,size_x,size_y):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(image_name),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed[K_RIGHT] and self.rect.right < 700:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullets('bullet.png',self.rect.centerx,self.rect.y,10,5,10)
        bullets.add(bullet)




class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            lost += 1

            self.rect.x = randint(0,650)



class Bullets(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()





bullets = sprite.Group()



lost = 0
score = 0




enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png',randint(0,650),0,randint(1,3),100,50)
    enemies.add(enemy)


player = Player('rocket.png',400,400,5,65,100)
font.init()
main_font = font.SysFont('Arial',35)
finish = False
result_font = font.SysFont('Arial',70)
game = True
clock = time.Clock()
while game:
    display.update()
    clock.tick(60)
    if not finish:

        window.blit(galaxy,(0,0))
        player.draw()
        player.update()
        bullets.draw(window)
        bullets.update()
        if sprite.spritecollide(player,enemies,False) or lost >= 3:
           finish = True
           lose_text = result_font.render('Вы Проиграли!',True,(255,255,255))
           window.blit(lose_text,(150,200))
        collide_enemies = sprite.groupcollide(enemies,bullets,True,True)
        for i in collide_enemies:
            enemy = Enemy('ufo.png',randint(0,650),0,randint(1,3),100,50)
            enemies.add(enemy)   
            score += 1
        if score >= 10:
            finish = True
            win_text = result_font.render('Вы победили!',True,(255,255,255))
            window.blit(win_text,(150,200))
        score_text = main_font.render('Счет:' + str(score),True,(255,255,255))
        window.blit(score_text,(0,10))
        lose_text = main_font.render('Пропущено:' + str(lost),True,(255,255,255))
        window.blit(lose_text,(0,50))
        enemies.draw(window)
        enemies.update()
    for e in event.get():
        
        if e.type == KEYDOWN:
            
            if e.key == K_SPACE:
                player.shoot()
        if e.type == QUIT:
            game = False