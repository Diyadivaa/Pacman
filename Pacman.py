import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Clone")
icon = pygame.image.load("pacman_icon.png")
pygame.display.set_icon(icon)

# Load game resources (graphics and sounds)
pacman_sprite = pygame.image.load("pacman.png")
dot_sprite = pygame.image.load("dot.png")
ghost_sprites = {
    "red": pygame.image.load("ghost_red.png"),
    "pink": pygame.image.load("ghost_pink.png"),
    "blue": pygame.image.load("ghost_blue.png"),
    "orange": pygame.image.load("ghost_orange.png")
}
waka_sound = pygame.mixer.Sound("waka.wav")
death_sound = pygame.mixer.Sound("death.wav")

# Set up game objects
class GameObject:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

class PacMan(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, pacman_sprite)
        self.speed = 5
        self.direction = "right"

    def update(self):
        # Move in the current direction
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Wrap around the screen
        if self.x < 0:
            self.x = SCREEN_WIDTH - self.sprite.get_width()
        elif self.x > SCREEN_WIDTH - self.sprite.get_width():
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT - self.sprite.get_height()
        elif self.y > SCREEN_HEIGHT - self.sprite.get_height():
            self.y = 0

class Ghost(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, ghost_sprites[color])
        self.speed = 3
        self.direction = "left"
    
    def update(self):
        # Move in the current direction
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

class Dot(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, dot_sprite)

class Wall(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)

# Set up the game world
world = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W................W",
    "W.WWWW.WWWWWWWW.W",
    "W.W....W.......W.W",
    "W.WWWW.W.WWWWW.WWW",
    "W................W",
    "WWWWWWWWWW.WWWWWWW",
    "W..........W.....W",
    "W.WWWWWWWWWWWWWW.W",
    "W.W.........W...W.W",
    "W.WWWWWWWWW.W.WWWW",
    "W.....W...W......W",
    "WWWWWWWWWWWWWWWWWW"
]

game_objects = []

for y, row in enumerate(world):
    for x, cell in enumerate(row):
        if cell == "W":
            # Create a wall at this position
            game_objects.append(Wall(x * 40, y * 40, wall_sprite))
        elif cell == ".":
            # Create a dot at this position
            game_objects.append(Dot(x * 40, y * 40))

# Create Pac-Man and the ghosts
pacman = PacMan(400, 300)
red_ghost = Ghost(400, 240, "red")
pink_ghost = Ghost(360, 240, "pink")
blue_ghost = Ghost(440, 240, "blue")
orange_ghost = Ghost(400, 280, "orange")

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = "left"
            elif event.key == pygame.K_RIGHT:
                pacman.direction = "right"
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"

    # Update game objects
    pacman.update()
    red_ghost.update()
    pink_ghost.update()
    blue_ghost.update()
    orange_ghost.update()

    # Check for collisions
    for ghost in [red_ghost, pink_ghost, blue_ghost, orange_ghost]:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            # Pac-Man collided with a ghost
            death_sound.play()
            running = False
            break

    # Draw game objects
    screen.fill((0, 0, 0))
    for game_object in game_objects:
        game_object.draw(screen)
    pacman.draw(screen)
    red_ghost.draw(screen)
    pink_ghost.draw(screen)
    blue_ghost.draw(screen)
    orange_ghost.draw(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
