from pygame import *
#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Calling the class constructor (Sprite):
        sprite.Sprite.__init__(self)
        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
    
        # each sprite must store the rect property - the rectangle which it's inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # the method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   #the method where the sprite is controlled by the arrow keys of the keyboard
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Calling the class constructor (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
    
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):       
        ''' moves the character by applying the current horizontal and vertical speed'''
        # horizontal movement first
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: 
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
    
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # turun
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # naik ke atas
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
        side = 'left'
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
            GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
            self.speed = player_speed
        def update(self):
            if self.rect.x <= 420: 
                self.side = "right"
            if self.rect.x >= win_width - 85:
                self.side = "left"
            if self.side == "left":
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
class Bullet(GameSprite):
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
            GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
            self.speed = player_speed
        def update(self):
            self.rect.x += self.speed
            if self.rect.x > win_width+10:
                self.kill()

#Creating a window
win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#setting the color according to the RGB color scheme
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
barriers.add(w1)
barriers.add(w2)
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
#creating sprites
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)
monster1 = Enemy('cyborg.png', win_width - 80, 180, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)
finish = False
run = True
while run:
    #the loop is triggered every 0.05 seconds
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
            elif e.key == K_SPACE:
                packman.fire()
    #draw objects
    #  w1.reset()
    #  w2.reset()
    if not finish:
        window.fill(back) 
        packman.update()
        bullets.update()
        packman.reset() 
        bullets.draw(window)           
        barriers.draw(window)
        final_sprite.reset()
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        #turning on the movement
        
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #calculate the ratio
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height, win_height)), (90, 0))
    display.update()
