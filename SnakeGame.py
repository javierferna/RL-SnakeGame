from snake_env import SnakeGameEnv
from q_learning import QLearning
import pygame
import sys

def main():
    # Window size
    FRAME_SIZE_X = 150
    FRAME_SIZE_Y = 150
    
    # Colors (R, G, B)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    
    difficulty = 15 # Adjust as needed
    render_game = True # Show the game or not
    growing_body = False # Makes the body of the snake grow
    training = False # Defines if it should train or not
    overall = 0

    # Initialize the game window, environment and q_learning algorithm
    # Your code here.
    # You must define the number of possible states.

    number_states = 72
    pygame.init()
    env = SnakeGameEnv(FRAME_SIZE_X, FRAME_SIZE_Y, growing_body)
    ql = QLearning(n_states=number_states, n_actions=4)  
    num_episodes = 20

    if render_game:
        game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
        fps_controller = pygame.time.Clock()
    
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        game_over = False
        
        while not game_over:
            # Choose the best action for the state and possible actions from the q_learning algorithm

            legal_actions = [0, 1, 2, 3]  # Ensure these actions are valid
            act = ql.choose_action(state, legal_actions)

            # Call the environment step with that action and get next_state, reward and game_over variables
            next_state, reward, game_over = env.step(act)

            if training:
                #update the q table using those variables.
                ql.update_q_table(state, act, reward, next_state)

            # Update the state and the total_reward.
            state = next_state
            total_reward += reward

            # Render
            if render_game:
                game_window.fill(BLACK)
                snake_body = env.get_body()
                food_pos = env.get_food()
                for pos in snake_body:
                    pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
                pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
            
            if env.check_game_over():
                break

            if render_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                pygame.display.flip()
                fps_controller.tick(difficulty)
        
        ql.save_q_table()
        print(f"Episode {episode+1}, Total reward: {total_reward}")
        overall += total_reward

    print(overall/num_episodes)



if __name__ == "__main__":
    main()
