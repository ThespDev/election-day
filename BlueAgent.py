import random
from Model import Linear_QNet
import torch
import numpy as np


class BlueAgent:
    
    def __init__(self,interval: list, automated:bool,numGrey:int,pSpy:float):
        self.certainty = 0
        self.certaintyUpperBound = interval[1]
        self.blueEnergy = 500
        self.voteOpinion = True
        self.automated = automated
        self.numGrey = numGrey
        self.pSpy = pSpy
        self.model = torch.load('finished_models/Blue500.pth')
        self.model.eval()


    def Message(self,potency):
        opinion = True
        if potency == 0 and self.numGrey <= 0:
            potency = random.randint(1,10)
        if potency == 0:
            self.numGrey -=1
            print("A Grey agent has been brought in")
            if random.random() < self.pSpy:
                opinion = False
                influence =  0.5 * self.certaintyUpperBound
            else:
                influence = 0.5 * self.certaintyUpperBound
        elif potency == 10:
            print("Vote for your freedom! Remember the past")
            influence = 0.5 * self.certaintyUpperBound
            self.blueEnergy -= 20
        elif potency == 9:
            print("Do it for your family, vote on the decision!")
            influence = 0.45 * self.certaintyUpperBound
            self.blueEnergy -= 18       
        elif potency == 8:
            print("Don't be influenced by the Red propaganda")
            influence = 0.4 * self.certaintyUpperBound
            self.blueEnergy -= 16     
        elif potency == 7:
            print("Make sure to vote! Exercise your rights")
            influence = 0.35 * self.certaintyUpperBound
            self.blueEnergy -= 14
        elif potency == 6:
            print("Voting is important")
            influence = 0.3 * self.certaintyUpperBound
            self.blueEnergy -= 12
        elif potency == 5:
            print("Think of our democracy!")
            influence = 0.25 * self.certaintyUpperBound
            self.blueEnergy -= 10
        elif potency == 4:
            print("Please vote people!")
            self.blueEnergy -= 8 
            influence = 0.2 * self.certaintyUpperBound
        elif potency == 3:
            print("Make sure to vote please")
            self.blueEnergy -= 6
            influence = 0.15 * self.certaintyUpperBound
        elif potency == 2:
            print("You should uhhh, vote!")
            influence = 0.1 * self.certaintyUpperBound
            self.blueEnergy -= 4
        else:
            print("Make sure to not vote, I mean um, please vote!")
            influence = 0.05 * self.certaintyUpperBound
            self.blueEnergy -= 2
        self.certainty = influence
        return opinion

    def nodeInteraction(self,node,voteOpinion) -> None:
        if (node.voteOpinion == voteOpinion):
            effect = random.uniform(0, self.certainty)
            node.addCertainty(effect)
        else:
            if node.certainty <= self.certainty:
                effect = (-1) * random.uniform(0,self.certainty)
                node.addCertainty(effect)
    
    def get_state(self,state):
        return np.array(state,dtype=float)

    def get_action(self,state):
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move =  torch.argmax(prediction).item()
        print(f"BLUE MOVE {move}")
        return move

           
        
    def takeTurn(self,greenArray,state):
        if self.automated:
            #npState = self.get_state(state)
            #validSelection = self.get_action(npState)
            validSelection = random.randint(1,10)
        else:
            validSelection = -1
            while validSelection not in range(0,11):
                selection  = int(input("Select the potency of your message (1-10) or bring a Grey agent into the network (0)\n"))
                if selection == 0 and self.numGrey == 0:
                    print("No Grey agents left!")
                else:
                    validSelection = selection
                    
        opinion = self.Message(validSelection)
        print(f"Blue's energy {self.blueEnergy}")
        blueFollowers = 0
        if self.blueEnergy <= 0:
            return True, blueFollowers
        for node in greenArray:
            if node.voteOpinion:
                blueFollowers += 1
            self.nodeInteraction(node,opinion)
        return False, blueFollowers
                





