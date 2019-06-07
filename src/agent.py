import random
import numpy as np
import keras as k
import tensorflow as tf
import model

# REGUL_CONST = 0.5
HIDDEN_LAYERS = 7

class OurAgent:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.memory = []
        # low discount rate since we expect our agent to
        #   take a lot of actions to get to a terminal state:
        self.discount = 0.98
        # epsilon rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.nnet = model.NNet(
            # REGUL_CONST,
            self.learning_rate,
            input_dim,
            output_dim,
            HIDDEN_LAYERS
        )
        self.target_nnet = model.NNet(
            # REGUL_CONST,
            self.learning_rate,
            input_dim,
            output_dim,
            HIDDEN_LAYERS
        )
        self.target_nnet.model.set_weights(self.nnet.model.get_weights())

    def act(self, state):
        """"""
        if random.random() <= self.epsilon:
            return random.randint(0, self.output_dim - 1)
        act_values = self.nnet.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def store_state(self, state, action, reward, next_state, done):
        """"""
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):
        """"""
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = self.nnet.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                next_qvals = self.target_nnet.model.predict(next_state)[0]
                target[0][action] = reward + self.discount * np.argmax(next_qvals)
            self.nnet.model.fit(state, target, epochs=1, verbose=0)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
