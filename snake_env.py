import numpy as np
import matplotlib.pyplot as plt
import csv
import random

class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.reset()

    def reset(self):
        # Resets the environment with default values
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.prev_distance = abs(self.food_pos[0] - self.snake_pos[0]) + abs(self.food_pos[1] - self.snake_pos[1])
        self.reldir = self.relative_apple_location()
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        self.update_snake_position(action)
        self.game_over = self.check_game_over()
        reward = self.calculate_reward()
        self.update_food_position()
        state = self.get_state()
        return state, reward, self.game_over

    def get_state(self):
        # Here, you will calculate the state based on your actual state calculation logic
        rel_dir = self.relative_apple_location()
        danger_up = self.danger_ahead_up()
        danger_right = self.danger_ahead_right()
        danger_left = self.danger_ahead_left()
        state = [rel_dir, danger_up, danger_left, danger_right]
        row_index = (state[0]-1) *2*2*2+ state[1] *2*2 + state[2]*2 +state[3]
        return row_index
        
    def get_body(self):
        return self.snake_body

    def get_food(self):
        return self.food_pos

    def calculate_reward(self):
        if self.snake_pos == self.food_pos:
            return 50
        elif self.game_over:
            return -100
        elif self.rel_dist_inc():
            return 1
        else:
            return -10
        
    def check_game_over(self):
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
                
        return False

    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'
    
        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10
            
        self.direction = direction
        
        
        self.snake_body.insert(0, list(self.snake_pos))
        
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.snake_body.pop()
    
    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_x//10)) * 10]
        self.food_spawn = True

    def relative_apple_location(self):
        head_x, head_y = self.snake_pos
        apple_x, apple_y = self.food_pos

        if apple_y < head_y:
            if apple_x < head_x:
                return 1  # Up Left
            elif apple_x > head_x:
                return 2  # Up Right
            else:
                return 3  # Up
        elif apple_y > head_y:
            if apple_x < head_x:
                return 4  # Left Down
            elif apple_x > head_x:
                return 5  # Right Down
            else:
                return 6  # Down
        else:
            if apple_x < head_x:
                return 7  # Left
            elif apple_x > head_x:
                return 8  # Right
            else:
                return 9  # Residuals

    def danger_ahead_up(self):
        head_x, head_y = self.snake_pos
        if (head_y <= 10 and self.direction == "DOWN") or \
                (head_x <= 10 and self.direction == "LEFT") \
                or (head_x + 10 >= self.frame_size_x and self.direction == "RIGHT") \
                or (head_y + 10 >= self.frame_size_y and self.direction == "UP"):
            return True
        else:
            return False

    def danger_ahead_left(self):
        head_x, head_y = self.snake_pos
        if (head_x <= 10 and self.direction == "UP") or \
                (head_y + 10 >= self.frame_size_y and self.direction == "RIGHT") \
                or (head_y <= 10 and self.direction == "LEFT") \
                or (head_x + 10 >= self.frame_size_x and self.direction == "DOWN"):
            return True
        else:
            return False

    def danger_ahead_right(self):
        head_x, head_y = self.snake_pos
        if (head_x + 10 >= self.frame_size_x and self.direction == "LEFT") or \
                (head_y <= 10 and self.direction == "UP") \
                or (head_y + 10 >= self.frame_size_y and self.direction == "LEFT") \
                or (head_x <= 10 and self.direction == "DOWN"):
            return True
        else:
            return False

    def rel_distance_discrete(self):
        x_segments = (self.frame_size_x - 10) // 10
        y_segments = (self.frame_size_y - 10) // 10

        x_distance_segments = (self.food_pos[0] - self.snake_pos[0]) // x_segments
        y_distance_segments = (self.food_pos[1] - self.snake_pos[1]) // y_segments

        x_discrete = min(max(1, abs(x_distance_segments)), 10)
        y_discrete = min(max(1, abs(y_distance_segments)), 10)

        # Combine the distances into a single number
        # A simple way to combine them is by averaging or summing
        combined_distance = (x_discrete + y_discrete) // 2  # Average them and round down

        # Ensure the combined result is within the 1-10 range
        combined_distance = min(max(1, abs(combined_distance)), 10)

        return combined_distance

    def proximity_walls(self):
        if self.snake_pos[1] <= 10:
            return True
        elif self.snake_pos[1] >= self.frame_size_y - 10:
            return True
        elif self.snake_pos[0] <= 10:
            return True
        elif self.snake_pos[0] >= self.frame_size_x - 10:
            return True
        else:
            return False

    def rel_dist_inc(self):
        # Calculate the Euclidean distance between the snake and the food
        distance = abs(self.food_pos[0] - self.snake_pos[0]) + abs(self.food_pos[1] - self.snake_pos[1])
        # If this is the first calculation, just store the distance and return 1

        # Check if the distance has improved
        if distance < self.prev_distance:
            self.prev_distance = distance
            return 1
        elif distance >= self.prev_distance:
            self.prev_distance = distance
            return 0
        else:
            return 0



