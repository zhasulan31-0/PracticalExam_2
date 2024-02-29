import pygame
from pygame.locals import *
import random

pygame.init()

# Window setup
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game Enhanced')

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Road setup
road_width = 300
marker_width = 10
marker_height = 50
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

lane_marker_move_y = 0  # For animating lane markers
player_x, player_y = 250, 400  # Player start position

clock = pygame.time.Clock()
fps = 120
speed = 2
score = 0
gameover = False

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = pygame.transform.scale(image, (45, 80))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y, 0)

player_group = pygame.sprite.GroupSingle(PlayerVehicle(player_x, player_y))

vehicle_images = [pygame.image.load(f'images/{img}') for img in ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']]
crash_image = pygame.image.load('images/crash.png')
crash_rect = crash_image.get_rect()

def add_vehicle():
    lane = random.choice(lanes)
    speed = random.randint(2, 4)
    vehicle = Vehicle(random.choice(vehicle_images), lane, -50, speed)
    vehicle_group.add(vehicle)
    return vehicle

vehicle_group = pygame.sprite.Group()

# Game loop
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in (K_LEFT, K_RIGHT):
                player = player_group.sprite
                new_lane = max(left_lane, min(right_lane, player.rect.centerx + (100 if event.key == K_RIGHT else -100)))
                player.rect.centerx = new_lane

    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    lane_marker_move_y = (lane_marker_move_y + speed * 2) % (marker_height * 2)
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (center_lane - 5, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (right_lane - 55, y + lane_marker_move_y, marker_width, marker_height))

    if len(vehicle_group) < 3 and random.randint(1, 30) == 1:
        add_vehicle()

    for vehicle in vehicle_group:
        vehicle.rect.y += vehicle.speed
        if vehicle.rect.top > height:
            vehicle.kill()
            score += 1
            if score % 5 == 0:
                speed += 0.5

    vehicle_group.draw(screen)
    player_group.draw(screen)

    if pygame.sprite.spritecollideany(player_group.sprite, vehicle_group):
        gameover = True
        screen.blit(crash_image, crash_rect)
        crash_image_x, crash_image_y = 250, 250


    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f'Score: {score}', True, white)
    screen.blit(score_text, (10, 10))

    if gameover:
        restart_text = font.render('Game Over! Press R to Restart or Q to Quit.', True, white)
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
        pygame.display.flip()
        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                    running = False
                    waiting = False
                if event.type == KEYDOWN and event.key == K_r:
                    vehicle_group.empty()
                    player_group.sprite.rect.center = (player_x, player_y)
                    score, speed, gameover = 0, 2, False
                    waiting = False

    pygame.display.flip()

pygame.quit()
