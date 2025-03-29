import pygame
import random

pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Load the sound
flap_sound = pygame.mixer.Sound("sound.mp3")

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 30)

bird_width, bird_height = 80, 80
bird_x, bird_y = 100, HEIGHT // 2
bird_velocity = 0
gravity = 0.5

pipe_width = 60
pipe_gap = 250
pipe_speed = 3
pipes = []
score = 0

bird_image = pygame.image.load("flappy.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

pipe_image = pygame.image.load("green_pipes.png")
pipe_image = pygame.transform.scale(pipe_image, (pipe_width, HEIGHT))

def display_score(score):
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    SCREEN.blit(score_text, (10, 10))

def restart_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0

def main():
    global bird_y, bird_velocity, pipes, score
    running = True
    last_pipe_time = pygame.time.get_ticks()

    passed_pipes = []

    top_collision_tolerance = 50  
    bottom_collision_tolerance = -25  

    while running:
        SCREEN.fill((135, 206, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -8
                    flap_sound.play()  # Play the sound when space is pressed
                    if score == -1:
                        restart_game()

        bird_velocity += gravity
        bird_y += bird_velocity

        if pygame.time.get_ticks() - last_pipe_time > 2500:
            pipe_height = random.randint(100, 400)
            pipes.append({'x': WIDTH, 'top': pipe_height, 'bottom': pipe_height + pipe_gap})
            last_pipe_time = pygame.time.get_ticks()

        for pipe in pipes:
            pipe['x'] -= pipe_speed
            flipped_top_pipe = pygame.transform.flip(pipe_image, False, True)
            SCREEN.blit(flipped_top_pipe, (pipe['x'], pipe['top'] - HEIGHT))
            SCREEN.blit(pipe_image, (pipe['x'], pipe['bottom']))

        SCREEN.blit(bird_image, (bird_x, bird_y))

        for pipe in pipes:
            if (pipe['x'] < bird_x + bird_width and pipe['x'] + pipe_width > bird_x):
                if bird_y < pipe['top'] and bird_y + bird_height - top_collision_tolerance < pipe['top']:
                    running = False
                if bird_y + bird_height > pipe['bottom'] and bird_y + bird_height + bottom_collision_tolerance > pipe['bottom']:
                    running = False

        if bird_y + bird_height >= HEIGHT:
            running = False

        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

        for pipe in pipes:
            if pipe['x'] + pipe_width < bird_x and pipe not in passed_pipes:
                score += 1
                passed_pipes.append(pipe)

        display_score(score)

        pygame.display.update()
        CLOCK.tick(30) 

    pygame.quit()

if __name__ == "__main__":
    main()
