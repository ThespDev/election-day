import GreenAgent
import igraph as ig
import random
import math
class TrainingGame:
    def __init__(self,numGreen,certaintyUpperBound,numGrey):
        self.numGreen = numGreen
        self.numGrey = numGrey
        self.certaintyUpperBound = certaintyUpperBound
        self.reset()

    def reset(self):
        self.pSpy = random.random()
        self.pGreen = random.uniform(0.4,0.7)
        self.greenvotePercentage = random.uniform(0.4,0.7)
        self.opinionChange = 0
        self.blueEnergy = 100
        self.g = ig.Graph.Erdos_Renyi(n=self.numGreen,p=self.greenvotePercentage,directed=False,loops=False)
        self.greenArray = self.generateGreenArray(self.g)
        self.turnCount = 0
        self.score = 0

    def generateGreenArray(self,graph) -> list:
        greenArray = []
        numVoters = self.greenvotePercentage* self.numGreen
        numVoters = math.floor(numVoters)
        for i in range(self.numGreen):
            currCertainty = random.uniform(0,self.certaintyUpperBound)
            if numVoters > 0:
                opinion = True
                numVoters -= 1
            else:
                opinion = False
            #print(f"ASSIGNED CERTAINTY: {currCertainty}")
            greenNode = GreenAgent.GreenAgent(opinion,currCertainty,graph.neighbors(i),i,self.certaintyUpperBound)
            greenArray.append(greenNode)
        return greenArray
            
    def greenNodeInteraction(self,node1 ,node2) -> None:
        if (node1.getOpinion() == node2.getOpinion()):
            effectNode1 = random.uniform(0,node1.certainty) * 0.1
            effectNode2 = random.uniform(0,node2.certainty) * 0.1
            node1.addCertainty(effectNode2)
            node2.addCertainty(effectNode1)
            #print(f"NODE 1 CERTAINTY{node1.certainty} NODE2 CERTAINTY {node2.certainty}")
        else:
            if node1.certainty < node2.certainty:
                effect = (-1) * random.uniform(0,node2.certainty)
                node1.addCertainty(effect)
            elif node1.certainty > node2.certainty:
                effect = (-1) * random.uniform(0,node1.certainty)
                node2.addCertainty(effect)
            else:
                pass
    
    def redNodeInteraction(self,node,certainty,opinion) -> None:
        if (node.voteOpinion == opinion):
            effect = random.uniform(0, certainty)
            node.addCertainty(effect)
        else:
            if node.certainty <= certainty:
                effect = (-1) * random.uniform(0,certainty)
                node.addCertainty(effect)


    def greenTurn(self):
        interactions  = []
        for node in self.greenArray:
            for neighbor in node.neighbors:
                interaction = tuple(sorted((node.id,neighbor)))
                if interaction not in interactions:
                    interactions.append(interaction)
                    self.greenNodeInteraction(node,self.greenArray[neighbor])
            if (node.certainty < (0.2*self.certaintyUpperBound)):
                #print("NODE OPINION SWITCHED")
                node.voteOpinion = not node.voteOpinion
                
                


    def Message(self,potency):
        if potency == 5:
            ignoreChance = 0.1
            influence = 0.25 * self.certaintyUpperBound
        elif potency == 4:
            ignoreChance = 0.08 
            influence = 0.2 * self.certaintyUpperBound
        elif potency == 3:
            ignoreChance = 0.06
            influence = 0.15 * self.certaintyUpperBound
        elif potency == 2:
            ignoreChance = 0.04
            influence = 0.1 * self.certaintyUpperBound
        else:
            ignoreChance = 0.02
            influence = 0.05 * self.certaintyUpperBound
        return influence,ignoreChance
    
    def blueTurn(self,potency):
        oldOpinionCount = 0     
        opinion = True
        if potency == 0:
            self.numGrey -=1
            if random.random() < self.pSpy:
                opinion = False
                influence =  0.1 * self.certaintyUpperBound
            else:
                opinion = True
                influence = 0.1 * self.certaintyUpperBound
        if self.numGrey < 0:
            potency = random.randint(1,5)
            opinion = True
        elif potency == 5:
            influence = 0.1 * self.certaintyUpperBound
            self.blueEnergy -= 5
        elif potency == 4:
            influence = 0.08 * self.certaintyUpperBound
            self.blueEnergy -= 4
        elif potency == 3:
            influence = 0.06 * self.certaintyUpperBound
            self.blueEnergy -= 3
        elif potency == 2:
            influence = 0.04 * self.certaintyUpperBound
            self.blueEnergy -= 2
        elif potency == 1:
            influence = 0.02 * self.certaintyUpperBound
            self.blueEnergy -= 1
        for node in self.greenArray:
            if node.voteOpinion == True:
                oldOpinionCount += 1
            self.redNodeInteraction(node,influence,opinion)
        return oldOpinionCount


    def redTurn(self):
        randomPotency = random.randint(1,5)
        nodesInfluenced = 0
        moveVars = self.Message(randomPotency)
        for node in self.greenArray:
            ignoreTolerance = random.random()
            if moveVars[1] > ignoreTolerance:
                node.ignoreRed = True
            if not node.ignoreRed:
                nodesInfluenced += 1
                self.redNodeInteraction(node,moveVars[0],False)
        return nodesInfluenced


    def simulateTurn(self,potency):  
        reward = 0
        gameOver = False
        newOpinionCount = 0
        numRedInfluence = self.redTurn()
        oldOpinionCount = self.blueTurn(potency)
        self.greenTurn()
        for node in self.greenArray:
            if node.voteOpinion == True:
                newOpinionCount += 1
        self.opinionChange = newOpinionCount - oldOpinionCount
        blueWinner = False
        if numRedInfluence == 0:
            reward = 100
            gameOver = True
            blueWinner = True
        elif newOpinionCount == 0:
            reward = -100
            gameOver = True
        elif self.blueEnergy <= 0:
            reward = -100
            gameOver = True
        elif newOpinionCount == self.numGreen:
            gameOver = True
            reward = 100
        elif newOpinionCount > oldOpinionCount:
            reward = 10
        elif newOpinionCount < oldOpinionCount:
            reward = -10
        return reward, gameOver, newOpinionCount, blueWinner


if __name__ == "__main__":
    game = TrainingGame(20,1,10)
    gameover = False
    while not gameover:
        print("--------------------------------------------------------------------------------------------")
        a = game.simulateTurn(2)
        gameover =  a[1]


    

