import numpy as np
import random


class policy():
    def __init__(self, epsilon, action_space):
        
        self.epsilon=epsilon
        self.nA=action_space

    def probs(self,q_table,observation):
        A_probs = np.ones(self.nA, dtype=float) * self.epsilon / self.nA
        best_action = np.argmax(q_table[observation])
        A_probs[best_action] += (1 - self.epsilon)

        return A_probs


class q_learning_agent():
    
    def __init__(self, epsilon, discount_factor, alpha, action_space, obs_space):
        self.q_table = np.zeros(obs_space,action_space)
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.action_space = action_space
        self.alpha = alpha
        self.policy = policy(self.epsilon, self.action_space)

    def learn(self, action, reward, state, next_state):
        next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def select_action(self,state):
        A_probs = self.policy.probs(self.q_table,state)
        return np.random.choice(np.arange(len(A_probs)), p=A_probs)
    
    def select_reproduction_candidate(self,population_rank,generation_factor):
        if(generation_factor > random.random()):
            return np.argmax(population_rank)
        else:
            np.random.randint(len(population_rank))


    def get_q_table(self):
        return self.q_table

    def set_q_table(self, q_table):
        self.q_table = q_table
