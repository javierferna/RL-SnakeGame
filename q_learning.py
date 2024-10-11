import numpy as np
import random
import json
import time

class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9, epsilon=0.01, epsilon_min=0.01, epsilon_decay=0.999999):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.load_q_table()

    def choose_action(self, state, allowed_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(allowed_actions)  # Explore
        else:
            action = np.argmax(self.q_table[state])  # Exploit
            
        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)
        return action

    def update_q_table(self, state, action, reward, next_state):
        # Update the current Q-value using the Q-learning formula
        # if terminal_state:
        # Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        # else:
        # Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))
        # Retrieve the current Q-value for the (state, action) pair
        current_q_value = self.q_table[state][action]

        if next_state is None:
            new_q_value = (1 - self.alpha) * current_q_value + self.alpha * (reward + 0)
        else:
            max_next_q_value = max(self.q_table[next_state])
            new_q_value = (1 - self.alpha) * current_q_value + self.alpha * (reward + self.gamma * max_next_q_value)

        self.q_table[state][action] = new_q_value

    def save_q_table(self, filename="q_table.txt"):
        np.savetxt(filename, self.q_table)

    def load_q_table(self, filename="q_table.txt"):
        try:
            self.q_table = np.loadtxt(filename)
        except IOError:
            # If the file doesn't exist, initialize Q-table with zeros as per dimensions
            self.q_table = np.zeros((self.n_states, self.n_actions))
