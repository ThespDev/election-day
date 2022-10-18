import random
import torch
import numpy as np
from collections import deque
from RedGame import TrainingGame
from Model import Linear_QNet, QTrainer
from plothelper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class RedTraining:
    def __init__(self) -> None:

        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(6,10)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)


    def get_state(self,game):
        state = [game.opinionChange,game.numGrey,game.pSpy,game.pGreen,game.greenvotePercentage,game.followers]
        return np.array(state,dtype=float)
    
    def remember(self,state,action,reward,next_state,gameOver):
        if (len(self.memory) >= MAX_MEMORY):
            self.memory.popleft()
        self.memory.append((state,action,reward,next_state,gameOver))
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,gameOvers =  zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,gameOvers)



    def train_short_memory(self,state,action,reward,next_state,gameover):
        self.trainer.train_step(state,action,reward,next_state,gameover)

    def get_action(self,state):
        self.epsilon = 400 - self.n_games
        if random.randint(0,80) < self.epsilon:
            move =  random.randint(1,10)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move =  torch.argmax(prediction).item()
        print(f"MOVE MADE: {move}")
        return move

def test():
    agent = RedTraining()
    game = TrainingGame(1000,1,5)
    state_old = agent.get_state(game)
    #print(state_old)

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    wins = 0
    agent = RedTraining()
    game = TrainingGame(100,1,10)
    while True:
        state_old = agent.get_state(game)

        move = agent.get_action(state_old)
        reward,gameOver,score,win = game.simulateTurn(move)
        state_new = agent.get_state(game)
        
        

        agent.train_short_memory(state_old,move,reward,state_new,gameOver)
        
        agent.remember(state_old,move,reward,state_new,gameOver)
        if gameOver:
            if win:
                wins += 1
            
            agent.model.save()
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            print('Game',agent.n_games,'Score',score,'Record',record,'Wins',wins)
            plot_scores.append(score)
            total_score += score 
            mean_score = total_score/ agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores,plot_mean_scores)


if __name__ == "__main__":
    train()
    #test()


