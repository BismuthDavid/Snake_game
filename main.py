import pygame
import sys
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
GRIDSIZE = 20
WHITE = (255, 255, 255)    # Background color.
RED = (255, 0, 0)   # Food color.
GREEN = (0, 255, 0)    # Snake color.

# Movement of the snake's head.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1    # Initial size of the snake.
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]    # Start from the middle of the grid.
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])    # Randomize the direction of the start.
        self.color = GREEN  # Set the color of the snake.

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRIDSIZE, GRIDSIZE))

# Food Class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE - 1)) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE - 1)) * GRIDSIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


def draw_objects(screen, snake, food):
    screen.fill(WHITE)
    snake.draw(screen)
    food.draw(screen)
    pygame.display.update()

# Main Function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    failures = 0  # Counter for failures


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()




        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        draw_objects(screen, snake, food)

        if (snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= WIDTH
                or snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= HEIGHT):
            snake.reset()
            # failures += 1
            # if failures >= 2:  # Check if the player failed more than 2 times
            #     screen.fill(WHITE)
            #     font = pygame.font.Font(None, 36)
            #     text = font.render("GAME OVER", True, RED)
            #     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            #     screen.blit(text, text_rect)
            #     pygame.display.update()
            #     pygame.time.wait(3000)  # Display "GAME OVER" for 3 seconds
            #     return

        clock.tick(10)


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    main()
