import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self,input_size,output_size) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size,output_size)
    def forward(self,x):
        x = F.relu(self.linear1(x))
        return x

    def save(self,file_name='Blue500.pth'):
        model_folder_path = './finished_models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path,file_name)
        torch.save(self,file_name)

class QTrainer:
    def __init__(self,model,lr,gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self,state,action,reward,nextState,gameOver):
        state = torch.tensor(state,dtype=torch.float)
        nextState = torch.tensor(nextState,dtype=torch.float)
        action = torch.tensor(action,dtype=torch.float)
        reward = torch.tensor(reward,dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state,0)
            nextState = torch.unsqueeze(nextState,0)
            action = torch.unsqueeze(action,0)
            reward = torch.unsqueeze(reward,0)
            gameOver = (gameOver,)

        prediction = self.model(state)

        target = prediction.clone()
        for i in range(len(gameOver)):
            Q_new = reward[i]
            if not gameOver[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(nextState[i]))
            target[i][torch.argmax(action[i]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target,prediction)
        loss.backward()
        self.optimizer.step()


