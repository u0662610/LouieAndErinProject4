# A5 Assignment
# Authors: Louis Jensen (u0662610) and Erin Zhang (u0889650)

import pygame, sys, math, random

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap

# A basic Sprite class that can draw itself, move, and test collisions
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


class Enemy:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        # Add code to
        # 1. Set the rectangle center to a random x and y based
        #    on the screen width and height
        # 2. Set a speed instance variable that holds a tuple (vx, vy)
        #    which specifies how much the rectangle moves each time.
        #    vx means "velocity in x".
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))
        self.speed = (5, 3)

        self.width = width
        self.height = height
        # Storing these here so that we can use them in the bounce function easily
    def move(self):
        # Add code to move the rectangle instance variable in x by
        # the speed vx and in y by speed vy. The vx and vy are the
        # components of the speed instance variable tuple.
        # A useful method of rectangle is pygame's move_ip method.
        # Research how to use it for this task.
        self.rectangle.move_ip(self.speed)

    def bounce(self):
        # This method makes the enemy bounce off of the top/left/right/bottom
        # of the screen. For example, if you want to check if the object is
        # hitting the left side, you can test
        # if self.rectangle.left < 0:
        # The rectangle.left tests the left side of the rectangle. You will
        # want to use .right .top .bottom for the other sides.
        # The height and width parameters gives the screen boundaries.
        # If a hit of the edge of the screen is detected on the top or bottom
        # you want to negate (multiply by -1) the vy component of the speed instance
        # variable. If a hit is detected on the left or right of the screen, you
        # want to negate the vx component of the speed.
        # Make sure the speed instance variable is updated as needed.
        if self.rectangle.left < 0 or self.rectangle.right > self.width:
            self.speed = (self.speed[0] * -1, self.speed[1])
        if self.rectangle.top < 0 or self.rectangle.bottom > self.height:
            self.speed = (self.speed[0], self.speed[1] * -1)


    def draw(self, screen):
        # Same draw as Sprite
        screen.blit(self.image, self.rectangle)

class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)

class Fast_Enemy(Enemy):
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

    # this part will randomize what side the big boy comes from
        self.rand_descision = random.randint(1, 2)
        if self.rand_descision == 1:
            self.rectangle.center = (0, random.randint(0, height))
            self.speed = (7, random.randint(-10, 10))
        else:
            self.rectangle.center = (width, random.randint(0, height))
            self.speed = (-7, random.randint(-10, 10))

        self.width = width
        self.height = height

def main():
    # Setup pygame
    pygame.init()

    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    # Load image assets
    # Choose your own image
    enemy = pygame.image.load("bullet2.png").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []
    # Make some number of enemies that will bounce around the screen.
    # Make a new Enemy instance each loop and add it to enemy_sprites.
    for enemy in range(0,10):
        enemy_sprites.append(Enemy(enemy_image, width, height))

    # This is the character you control. Choose your image.
    player_image = pygame.image.load("FireBoy.GIF").convert_alpha()

    player_image = pygame.transform.smoothscale(player_image, (100, 100)) #this is to scale the player sprite - Louie
    player_sprite = Sprite(player_image)

    life = 5

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("Little_Flame.png").convert_alpha()
    powerup_image = pygame.transform.smoothscale(powerup_image, (50, 50))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    # Adding in our new stuff here!!
    enemy2 = pygame.image.load("bullet1.png").convert_alpha()
    enemy2_image = pygame.transform.smoothscale(enemy2, (110, 110))

    enemy2_sprites = []

    #Additional power up creation
    powerup_image2 = pygame.image.load("WoodLog.png").convert_alpha()
    powerup_image2 = pygame.transform.smoothscale(powerup_image2, (50, 50))

    powerups_2 = []

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing:# while is_playing is True, repeat
    # Modify the loop to stop when life is <= to 0.
        if life <= 0:
            break

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.
        for enemy in enemy_sprites:
            if player_sprite.is_colliding(enemy):
                life = life - 0.1

        # Loop over the powerups. If the player sprite is colliding, add
        # 1 to the life.

        for powerup in powerups:
            if pixel_collision(powerup.mask, powerup.rectangle,player_sprite.mask,player_sprite.rectangle):
                life = life + 1

        # Make a list comprehension that removes powerups that are colliding with
        # the player sprite.
        powerups = [powerup for powerup in powerups if not player_sprite.is_colliding(powerup)]

        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce()

        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        random_number = random.randint(0,25)
        if random_number == 6:
            powerups.append(PowerUp(powerup_image, width, height))

        # Erase the screen with a background color
        screen.fill((188,202,205)) # fill the window with a color

        # Adding code for our new stuff here (new enemy)!!
        random_number = random.randint(0, 40)
        if random_number == 2:
            enemy2_sprites.append(Fast_Enemy(enemy2_image, width, height))

        for enemy in enemy2_sprites:
            enemy.move()

        for enemy_sprite in enemy2_sprites:
            enemy_sprite.draw(screen)

        for enemy in enemy2_sprites:
            if player_sprite.is_colliding(enemy):
                life = life - 0.4

        #Additional code for an additional power up
        for powerup in powerups_2:
            if pixel_collision(powerup.mask, powerup.rectangle,player_sprite.mask,player_sprite.rectangle):
                life = life + 2

        powerups_2 = [powerup for powerup in powerups_2 if not player_sprite.is_colliding(powerup)]

        random_number = random.randint(0, 80)
        if random_number == 8:
            powerups_2.append(PowerUp(powerup_image2, width, height))

        for powerup in powerups_2:
            powerup.draw(screen)


        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Life: " + str('%.1f'%life)
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))

        # Additional code implementing a win condition
        if life >= 40:
            break

        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    # Additional code to show text of whether player won or died
    if life <= 0:
        dead_text = "You Died, Better Luck Next Time!"
        dead_label = myfont.render(dead_text, True, (239, 0, 0),(255,255,255))
        screen.blit(dead_label, (90, 175))
        pygame.display.update()

    if life >= 40:
        life_text = "You Win! Congratulations!!!"
        life_label = myfont.render(life_text, True, (19, 118, 9),(255,255,255))
        screen.blit(life_label, (125, 175))
        pygame.display.update()

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
