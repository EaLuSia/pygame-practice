import pygame
pygame.font.init()
pygame.mixer.init()

#colors
white = (255,255,255)
black=(0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)

#font
hp_font = pygame.font.SysFont('comicsans',40)
winner_font = pygame.font.SysFont('comicsans',100)

#parameters
width, height = (800,600)
spaceship_width,spaceship_height = 55,44
FPS = 60
VEL = 3
bullet_vel = 7
max_bullets = 3

#create window
win = pygame.display.set_mode((width,height))
pygame.display.set_caption('First Game!')
border = pygame.Rect(width/2-5,0,10,height)

#load Assets
yellow_spaceship_image = pygame.image.load('Assets\spaceship_yellow.png')
yellow_spaceship = pygame.transform.rotate (
    pygame.transform.scale(yellow_spaceship_image,(spaceship_width,spaceship_height)),90)
red_spaceship_image = pygame.image.load('Assets\spaceship_red.png')
red_spaceship = pygame.transform.rotate (
    pygame.transform.scale(red_spaceship_image,(spaceship_width,spaceship_height)),270)
space = pygame.transform.scale(pygame.image.load('Assets\space.png'),(width,height))
fire_sound = pygame.mixer.Sound('Assets\Gun+Silencer.mp3')

#create event
yellow_hit = pygame.USEREVENT+ 1
red_hit = pygame.USEREVENT + 2


#keybinding
def yellow_spaceship_movement(key_pressed,yellow):
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0 :
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + spaceship_width < height:
        yellow.y += VEL
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + spaceship_height < border.x:
        yellow.x += VEL


def red_spaceship_movement(key_pressed,red):
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + spaceship_width < height:
        red.y += VEL
    if key_pressed[pygame.K_LEFT] and red.x - VEL > border.x + 10:
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + spaceship_height < width:
        red.x += VEL


#bullet function
def handle_bullet(yellow_bullet,red_bullet,yellow,red):
    for bullet in yellow_bullet:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            yellow_bullet.remove(bullet)
            pygame.event.post(pygame.event.Event(red_hit))
        elif bullet.x > width:
            yellow_bullet.remove(bullet)
    for bullet in red_bullet:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            red_bullet.remove(bullet)
            pygame.event.post(pygame.event.Event(yellow_hit))
        elif bullet.x + 10 < 0:
            red_bullet.remove(bullet)


#update frames

def draw_window(yellow,red,yellow_bullet,red_bullet):
    win.blit(space,(0,0))
    pygame.draw.rect(win, black, border)
    win.blit(yellow_spaceship,(yellow.x,yellow.y))
    win.blit(red_spaceship,(red.x,red.y))

    for bullet in yellow_bullet:
        pygame.draw.rect(win,YELLOW,bullet)
    for bullet in red_bullet:
        pygame.draw.rect(win,RED,bullet)


def draw_hp(yellow_hp,red_hp):
    yellow_hp_text = hp_font.render(str(yellow_hp), 1, white)
    red_hp_text = hp_font.render(str(red_hp), 1, white)
    win.blit(yellow_hp_text, (10, 10))
    win.blit(red_hp_text, (width - 10 - red_hp_text.get_width(), 10))
    i=1
    while i<=yellow_hp:
        hp_block = pygame.Rect(10+yellow_hp_text.get_width()+5*i,10,4,yellow_hp_text.get_height())
        pygame.draw.rect(win,YELLOW,hp_block)
        i += 1
    i=1
    while i <= red_hp:
        hp_block = pygame.Rect(width - 10 - red_hp_text.get_width() - 5 * i, 10, 4, red_hp_text.get_height())
        pygame.draw.rect(win, RED, hp_block)
        i += 1
    pygame.display.update()


def draw_winner(text):
    winner_text = winner_font.render(text,1,white)
    win.blit(winner_text,(width//2-winner_text.get_width()//2,height//2-winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(50,250,spaceship_height,spaceship_width)
    red = pygame.Rect(700,250,spaceship_height,spaceship_width)
    yellow_bullet = []
    red_bullet = []
    yellow_hp = 10
    red_hp = 10
    winner_text=''
    clock = pygame.time.Clock()
    clock.tick(FPS)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j and len(yellow_bullet) <= max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2-2,10,4)
                    yellow_bullet.append(bullet)
                    fire_sound.play()
                if event.key == pygame.K_KP1 and len(red_bullet) <= max_bullets:
                    bullet = pygame.Rect(red.x,red.y+red.height//2-2,10,4)
                    red_bullet.append(bullet)
                    fire_sound.play()

            if event.type == yellow_hit:
                yellow_hp -= 1
            if event.type == red_hit:
                red_hp -= 1

        if yellow_hp <= 0:
            draw_hp(yellow_hp, red_hp)
            winner_text = 'Red Win!'
        if red_hp <= 0:
            draw_hp(yellow_hp, red_hp)
            winner_text = 'Yellow Win!'
        if winner_text != '':
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_spaceship_movement(key_pressed,yellow)
        red_spaceship_movement(key_pressed,red)
        handle_bullet(yellow_bullet,red_bullet,yellow,red)
        draw_hp(yellow_hp, red_hp)
        draw_window(yellow, red, yellow_bullet, red_bullet)


    main()


if __name__ == '__main__':
    main()


