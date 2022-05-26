import pygame
import os
#Game font - initializes pygame font module.
pygame.font.init()

#Sound effects.
pygame.mixer.init()

#Dimensions for the screen.
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#Background color. - not white
COLOR = (205, 255, 200)

#Colour for border.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#BORDER TO HINDER CHARACTERS.
#BORDER = pygame.Rect(WIDTH, HEIGHT//2 -5)
BORDER = pygame.Rect(0, HEIGHT//2, WIDTH, 10)
HEALTH_FONT = pygame.font.SysFont("Arial", 25)
WINNER_FONT = pygame.font.SysFont("Arial", 100)

#DICTIONARY - SOUND TABLE FOR SOUND EFFECTS.
sound_tb ={"grenade_sound":pygame.mixer.Sound(os.path.join("gamages", "Assets_Grenade+1.mp3")),
    "gun_sound":pygame.mixer.Sound(os.path.join("gamages", "Assets_Gun+Silencer.mp3"))
}
#Name of the window
pygame.display.set_caption("T-A-C-T-I-C-A-L    C_O_M_B_A_T")
#Frames per Second
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 155, 140

#PLAY SOUND FUNCTION - PLAYS SELECTED VALUE FROM DICTIONARY.
def PS(sound):
    pygame.mixer.Sound.play(sound)


YELLOW_HIT = pygame.USEREVENT + 1 #pygame.userevent is just a number.
RED_HIT = pygame.USEREVENT + 2

LEFT_CHARACTER_IMAGE = pygame.image.load(os.path.join("gamages", "robo-1.png"))
#Resizing and rotating image character.
#No need to rotate images since they are in required position.
#LEFT_CHARACTER_IMAGE = pygame.transform.rotate()
LEFT_CHARACTER_IMAGE = pygame.transform.scale(LEFT_CHARACTER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RIGHT_CHARACTER_IMAGE = pygame.image.load(os.path.join("gamages", "robo-2.png"))
#Resize and rotate.
RIGHT_CHARACTER_IMAGE = pygame.transform.scale(RIGHT_CHARACTER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

#BACKGROUND IMAGE.
ZONE = pygame.transform.scale(pygame.image.load(os.path.join("gamages", "background-warzone.png")), (WIDTH, HEIGHT))

#FUNCTION FOR BACKGROUND WITH COLOUR.
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(ZONE, (0, 0))
    #WIN.fill(COLOR)
    pygame.draw.rect(WIN, BLACK, BORDER)

    #DISPLAYS "LIVES" FONT ON SCREEN.
    red_health_text = HEALTH_FONT.render("lives: " + str(red_health), 1, COLOR)
    yellow_health_text = HEALTH_FONT.render("lives: " + str(yellow_health), 1, COLOR)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))


    WIN.blit(LEFT_CHARACTER_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RIGHT_CHARACTER_IMAGE, (red.x, red.y))
    
    for bullet in red_bullets: 
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets: 
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#FUNCTION FOR LEFT GAME CHARACTER MOVEMENTS - CONTROLS.
def yellow_movement(keys_pressed, yellow):
    #Tells keys that are currently being pressed.
    #LEFT CHARACTER INPUT CONTROL KEYS.
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x +  VEL + yellow.width < WIDTH: #Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Top
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #Bottom
        yellow.y += VEL

#FUNCTION FOR RIGHT GAME CHARACTER MOVEMENTS - CONTROLS.
def red_movement(keys_pressed, red):
    #Tells keys that are currently being pressed.
    #RIGHT CHARACTER INPUT CONTROL KEYS.
    if keys_pressed[pygame.K_LEFT] and red.x - VEL < WIDTH: #BORDER.x + BORDER.width: #Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL  > 0: #Top
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 5: #Bottom
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.y += BULLET_VEL
        if red.colliderect(bullet): #colliderect is a function in pygame for collision.
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

#Function - "WIN" message.
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, COLOR)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


#MAIN CODE - BRAIN.
def main():
    #Creates a rectangular container that possess the game characters,
    #and sets them at specific positions on the canvas.
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    #Character bullets
    red_bullets = []
    yellow_bullets =[]

    #Health of game characters.
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        #Clock makes game not run pass 60 fps.
        clock.tick(FPS)
        #Gets a list of all events and loops through them.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #Quits game.
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(-60 + yellow.x + yellow.width//2,yellow.y + yellow.height // 2, 10, 5) #bullet is a pygame rect; however, can use a bullet image. 10 is b-width and 5 is b-height.
                    yellow_bullets.append(bullet)
                    
                    
                    #PLAY GUN SOUND
                    #Call to "play sound" function.
                    PS(sound_tb["gun_sound"])

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width//2, red.y + red.height//3 - 2, 10, 5) 
                    red_bullets.append(bullet)
                    #PLAY GUN SOUND
                    PS(sound_tb["gun_sound"])


            #Computation for character's health.
            #Decreases character's health when hit.
            if event.type == RED_HIT:
                red_health -= 1
                #PLAY BOMB SOUND
                PS(sound_tb["grenade_sound"])
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #PLAY BOMB SOUND
                PS(sound_tb["grenade_sound"])

        win_msg = ""
        if red_health <= 0:
            win_msg = "Robot 1 Wins!"
        if yellow_health <= 0:
            win_msg = "Robot 2 Wins!"
        if win_msg != "":
            draw_winner(win_msg)
            break
            
        #PREVENTS TOP ROBOT FROM CROSSING THE BORDER.
        if yellow.y + yellow.height > BORDER.y:
            yellow.y = yellow.y - yellow.height
        #PREVENTS BOTTOM ROBOT FROM CROSSING THE BORDER.
        if red.y < BORDER.y:
            red.y = red.y + red.height
        
        #elif red == 736:
           # pass
        #print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        
        #Function that handles bullets. Checks to see if any bullet collides with each of the characters.
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        #Game character moves forward.
        #yellow.x += 1
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    #Ends the game.
    #pygame.quit()
    #Restarts the game.
    main()
if __name__ == "__main__":
    main()

"""
PERSONAL NOTES:
 yellow.x is the x coordinate of the character, thus the top left.
 yellow.width is the full length(width) of the character, beginning 
 from the start(top left of x coordinate) to the end of the character's width.
 yellow.y is the y coordinate of the character, thus the top left
 yellow.height is the full length(height) of the character, beginning 
 from the start(top left of y coordinate) to the end of the character's height.


 if y coord + height of image > border y coord:
     image.y coord = y coord + or - height of image
"""