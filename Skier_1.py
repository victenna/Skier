import pygame, random
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
penalty = 0
N = 10 # Number of flags
font = pygame.font.Font(None, 50)
T = 60  # Time limit in seconds
k=1.1

class Skier():
    def __init__(self):
        super().__init__()
        self.image_forward = pygame.image.load('skier_forward.png')
        self.image_forward=pygame.transform.scale(self.image_forward,(int(55*k),int(55*k)))
        self.image_left = pygame.image.load('skier_left.png')
        self.image_left=pygame.transform.scale(self.image_left,(int(65*k),int(65*k)))
        self.image_right = pygame.image.load('skier_right.png')
        self.image_right=pygame.transform.scale(self.image_right,(int(65*k),int(65*k)))
        self.rect = self.image_forward.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2)
        self.rect.y = (SCREEN_HEIGHT // 2)
        self.change_x = 0

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x < 350:
            self.rect.x = 350
        if self.rect.x > 650:
            self.rect.x = 650
        if self.change_x < 0:
            self.image = self.image_left
        elif self.change_x > 0:
            self.image = self.image_right
        else:
            self.image = self.image_forward
        screen.blit(self.image,self.rect)
  

class Tree(pygame.sprite.Sprite):
    def __init__(self, area, y=None):
        super().__init__()
        self.image = pygame.image.load('tree.png')
        self.rect = self.image.get_rect()
        if area == 'left':
            self.rect.x = random.randint(0, 300)
        elif area == 'right':
            self.rect.x = random.randint(700, 1000)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)

    def update(self):
        self.rect.y -= 5  # Trees move up
        if self.rect.y < 0:  # Check if tree is above the screen
            self.rect.y = SCREEN_HEIGHT
            if self.rect.x < 350:  # Tree is on the left side
                self.rect.x = random.randint(0, 300)
            else:  # Tree is on the right side
                self.rect.x = random.randint(700, 1000)

class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('flag.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(300, 700)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)

    def update(self):
        self.rect.y -= 5  # Trees move up
        if self.rect.y + self.rect.height < 0:  # Check if tree is above the screen
            self.rect.y = SCREEN_HEIGHT
            self.rect.x = random.randint(300, 700)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Skier Game')
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()
flags = pygame.sprite.Group()

trees = pygame.sprite.Group()
trees1 = pygame.sprite.Group()

# Create the skier
skier = Skier()
q,q1=0,0

# Create trees and flags
for i in range(N):
    flag = Flag()
    flags.add(flag)
    all_sprites.add(flag)
  
for y in range(100):
    tree = Tree('left', y)
    trees.add(tree)
    all_sprites.add(tree)
    
for y in range(100):
    tree = Tree('right', y)
    trees.add(tree)  # You can add all trees to the same group
    all_sprites.add(tree)
    
# Initialize the start time
start_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()  # Get the current time
    elapsed_time = (current_time - start_time) // 1000  # Calculate elapsed time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                skier.change_x = -3
            elif event.key == pygame.K_RIGHT:
                skier.change_x = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                skier.change_x = 0

    if elapsed_time >= T:
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))
        pygame.display.flip()  # Update the screen to show the game over text
        pygame.time.wait(3000)  # Display the final message for 3 seconds
        running = False  # End the game

    all_sprites.update()
    flag_hits = pygame.sprite.spritecollide(skier, flags, False)
    if flag_hits:
        q = 1
        if q - q1 > 0: penalty = penalty + 1
        #print('Collision Numbers=',penalty)
        if q == 1: q1 = 1
    else:
        q, q1 = 0, 0
    screen.fill('light blue')
    skier.update()
    trees.update()
    trees.draw(screen)
    
    trees1.update()
    trees1.draw(screen)
    all_sprites.draw(screen)
    

    penalty_text = font.render('Collision Numbers with Flags='+str(penalty), True, 'red')
    time_text = font.render(f"Time in sec= {elapsed_time}", True, (0, 0, 0))

    screen.blit(penalty_text, (10, 10))
    screen.blit(time_text, (SCREEN_WIDTH - 400, 10))

    pygame.display.flip()
    clock.tick(100)

pygame.display.flip()
pygame.time.wait(6000) # Display the final message for 3 seconds
pygame.quit()
