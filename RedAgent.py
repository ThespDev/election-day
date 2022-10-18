import random
import torch
import numpy as np


class RedAgent:
    
    def __init__(self,interval: list,automated: bool):
        self.certainty = 0
        self.certaintyUpperBound = interval[1]
        self.ignorechance = 0
        self.voteOpinion = False
        self.automated =  automated
        self.model = torch.load('finished_models/Red500.pth')
        self.model.eval()

    def Message(self,potency):
        if potency == 10:
            print("The government wants to steal your freedom!")
            influence = 0.5 * self.certaintyUpperBound
            ignoreChance =0.2
        elif potency == 9:
            print("This decision is harmful for our country!")
            influence = 0.45 * self.certaintyUpperBound
            ignoreChance = 0.18
        elif potency == 8:
            print("Exercise your rights to protest, don't vote!")
            influence = 0.4 * self.certaintyUpperBound
            ignoreChance = 0.16
        elif potency == 7:
            print("It's your choice to not vote!")
            influence = 0.35 * self.certaintyUpperBound
            ignoreChance = 0.14
        elif potency == 6:
            print("Don't be influenced by the left, don't vote")
            influence = 0.3 * self.certaintyUpperBound
            ignoreChance = 0.12
        elif potency == 5:
            print("Experts say voting will raise taxes")
            ignoreChance = 0.1
            influence = 0.25 * self.certaintyUpperBound
        elif potency == 4:
            print("Trust in God, don't vote")
            ignoreChance = 0.08 
            influence = 0.2 * self.certaintyUpperBound
        elif potency == 3:
            print("We believe you shouldn't vote")
            ignoreChance = 0.06
            influence = 0.15 * self.certaintyUpperBound
        elif potency == 2:
            print("We're not fake news I swear, don't vote!")
            ignoreChance = 0.04
            influence = 0.1 * self.certaintyUpperBound
        else:
            print("You shouldn't vote because uhhh, don't vote!")
            ignoreChance = 0.02
            influence = 0.05 * self.certaintyUpperBound
        self.certainty = influence
        self.ignorechance = ignoreChance
    
    def get_state(self,state):
        return np.array(state,dtype=float)
    
    def get_action(self,state):
        state0 = torch.tensor(state, dtype=torch.float)
        print(f"STATE: {state0}")
        prediction = self.model(state0)
        move =  torch.argmax(prediction).item()
        print(f"RedMove {move}")
        return move


    def nodeInteraction(self,node) -> None:
        if (node.voteOpinion == self.voteOpinion):
            effect = random.uniform(0, self.certainty)
            node.addCertainty(effect)
        else:
            if node.certainty <= self.certainty:
                effect = (-1) * random.uniform(0,self.certainty)
                node.addCertainty(effect)

       
    #Returns Gameoverstate    
    def takeTurn(self,greenArray,state):
        nodesInfluenced = 0
        if self.automated:
            npState = self.get_state(state)
            selection = self.get_action(npState)
        else:
            selection = -1
            while selection not in range(1,11):
                selection = int(input("Select the potency of your message (1-10)\n"))
        self.Message(selection)
        redFollowers = 0
        nodesInfluenced = 0
        for node in greenArray:
            if not node.voteOpinion:
                redFollowers += 1
            ignoreTolerance = random.random()
            if self.ignorechance > ignoreTolerance:
                node.ignoreRed = True
            if not node.ignoreRed:
                nodesInfluenced += 1
                self.nodeInteraction(node)
        if nodesInfluenced == 0:
            return True, redFollowers
        else:
            return False, redFollowers
    

