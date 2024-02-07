import pygame    # Import the Pygame library for creating the game.
import sys  # Import the system module for system-specific functionality.
import random   # Import the random module for generating random numbers.

pygame.init()   # Initialize Pygame.


WIDTH, HEIGHT = 800, 600     # Set the dimensions of the game window.
GRIDSIZE = 20   # how many pixels represent every objects.
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
        self.failures = 0   # Set the initial number of failures to zero.

    def get_head_position(self):
        return self.positions[0]     # Get the position of the snake's head.

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
        # Calculate the new position of the snake's head based on the current position and direction.
        if len(self.positions) > 2 and new in self.positions[2:]:
            # If the snake collided with itself update the number of failures by +1.
            self.failures += 1
            if self.failures <= 2:  # If the player had failed less than 3 times.
                self.reset()    # Reset the game if the snake collides with itself.
            else:   # If the player had failed more than 3 times.
                screen.fill(WHITE)  # Delete all items filling all the screen with white color.
                font = pygame.font.Font(None, 36)   # Determinate the font and size.
                text = font.render("GAME OVER", True, RED)  # Determinate the message of "game over".
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))    # placing the message
                screen.blit(text, text_rect)
                pygame.display.update()
                pygame.time.wait(3000)  # Display "GAME OVER" for 3 seconds
                pygame.quit()
                sys.exit()
        else:
            self.positions.insert(0, new)   # extend the length of the snake by 1.
            if len(self.positions) > self.length:
                self.positions.pop()     # Remove the last element if the snake exceeds its length.

    def reset(self):
        self.length = 1    # Reset the snake size
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]    # Reset the snake's position.
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])    # Reset the snake's direction.

    def draw(self, surface):
        # Draw the snake on the game surface.
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRIDSIZE, GRIDSIZE))


# Food Class
class Food:
    def __init__(self):
        self.position = (0, 0)   # Initial position of the food.
        self.color = RED    # Color of the food.
        self.randomize_position()   # Set a random initial position for the food.

    def randomize_position(self):
        # Set a random place for the food within the game grid.
        self.position = (random.randint(0, (WIDTH // GRIDSIZE - 1)) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE - 1)) * GRIDSIZE)

    def draw(self, surface):
        # Draw the food on the game surface.
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


# Draw Game Objects
def draw_objects(screen, snake, food):
    screen.fill(WHITE)  # Fill the entire screen with the color white.
    snake.draw(screen)  # Draw the snake on the screen.
    food.draw(screen)   # Draw the food on the screen.
    pygame.display.update()   # Update the display to show the changes.


# Main Function
def main():
    clock = pygame.time.Clock()  # Create a clock obj. to control the game's frame rate.
    snake = Snake()  # Create an instance of the snake class.
    food = Food()  # Create an instance of the food class.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user quits the game.
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Check if a key is pressed.
                # Check if the UP arrow key is pressed and the snake is not moving downwards
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                # Check if the DOWN arrow key is pressed and the snake is not moving upwards
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                # Check if the LEFT arrow key is pressed and the snake is not moving rightwards
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                # Check if the RIGHT arrow key is pressed and the snake is not moving leftwards
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()  # Move the snake
        if snake.get_head_position() == food.position:  # Check if the snake eats the food
            snake.length += 1  # Increase the length of the snake
            food.randomize_position()  # Set a new position for the food

        draw_objects(screen, snake, food)  # Draw the game objects on the screen

        clock.tick(10)  # Control the frame rate of the game


if __name__ == "__main__":
    # Set up the game window with the specified dimensions
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")  # Set the title of the game window
    main()  # Call the main function to start the game
