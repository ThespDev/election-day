import random

class RedAgent:
    
    def __init__(self,interval: list,automated: bool):
        self.certainty = 0
        self.intervalUpperBound = interval[1]
        self.ignorechance = 0
        self.voteOpinion = False
        self.automated =  automated

    def Message(self,potency):
        if potency == 5:
            ignoreChance = 0.4
            influence = 0.5 * self.intervalUpperBound
        elif potency == 4:
            ignoreChance = 0.3 
            influence = 0.4 * self.intervalUpperBound
        elif potency == 3:
            ignoreChance = 0.2
            influence = 0.3 * self.intervalUpperBound
        elif potency == 2:
            ignoreChance = 0.1
            influence = 0.2 * self.intervalUpperBound
        else:
            ignoreChance = 0.05
            influence = 0.1 * self.intervalUpperBound
        self.certainty = influence
        self.ignorechance = ignoreChance

    def nodeInteraction(self,node) -> None:
        if (node.voteOpinion == self.voteOpinion):
            effect = random.uniform(0, self.certainty)
            node.addCertainty(effect)
        else:
            if node.certainty <= self.certainty:
                effect = (-1) * random.uniform(0,self.certainty)
                node.addCertainty(effect)

       
    #Returns Gameoverstate    
    def takeTurn(self,greenArray) -> bool:
        nodesInfluenced = 0
        if self.automated:
            selection = random.randint(1,5)
        else:
            selection = -1
            while selection not in range(1,6):
                selection = int(input("Select the potency of your message (1-5)\n"))
        self.Message(selection)
        for node in greenArray:
            ignoreTolerance = random.random()
            if self.ignorechance > ignoreTolerance:
                node.ignoreRed = True
            if not node.ignoreRed:
                nodesInfluenced +=1
                self.nodeInteraction(node)
        print(f"Nodes influenced by Red: {nodesInfluenced}")
        if nodesInfluenced == 0:
            return True
        else:
            return False
                




