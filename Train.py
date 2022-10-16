import GreenAgent
import igraph as ig
import random
import math
class TrainingGame:
    def __init__(self,numGreen,pGreen,certaintyUpperBound,greenvotePercentage):
        self.numGreen = numGreen
        self.pGreen = pGreen
        self.certaintyUpperBound = certaintyUpperBound
        self.greenvotePercentage = greenvotePercentage
        self.g = ig.Graph.Erdos_Renyi(n=numGreen,p=greenvotePercentage,directed=False,loops=False)
        self.reset()

    def reset(self):
        self.greenArray = self.g.Graph.Erdos_Renyi(n=self.numGreen,p=self.greenvotePercentage,directed=False,loops=False)
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
            greenNode = GreenAgent.GreenAgent(opinion,currCertainty,graph.neighbors(i),i,self.certaintyUpperBound)
            greenArray.append(greenNode)
        return greenArray
            
    def greenNodeInteraction(self,node1 ,node2) -> None:
        if (node1.getOpinion() == node2.getOpinion()):
            effectNode1 = random.uniform(0,node1.certainty)
            effectNode2 = random.uniform(0,node2.certainty)
            node1.addCertainty(effectNode2)
            node2.addCertainty(effectNode1)
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
            if (node.certainty < (0.1*self.certaintyUpperBound)):
                node.voteOpinion = not node.voteOpinion
                
                


    def Message(self,potency):
        if potency == 5:
            ignoreChance = 0.4
            influence = 0.5 * self.certaintyUpperBound
        elif potency == 4:
            ignoreChance = 0.3 
            influence = 0.4 * self.certaintyUpperBound
        elif potency == 3:
            ignoreChance = 0.2
            influence = 0.3 * self.certaintyUpperBound
        elif potency == 2:
            ignoreChance = 0.1
            influence = 0.2 * self.certaintyUpperBound
        else:
            ignoreChance = 0.05
            influence = 0.1 * self.certaintyUpperBound
        return influence,ignoreChance
    
    def simulateTurn(self,potency):  
        moveVars = self.Message(potency)
        nodesInfluenced = 0
        reward = 0
        gameOver = False
        oldOpinionCount = 0
        newOpinionCount = 0
        for node in self.greenArray:
            if node.voteOpinion == False:
                oldOpinionCount += 1
            ignoreTolerance = random.random()
            if moveVars[1] > ignoreTolerance:
                node.ignoreRed = True
            if not node.ignoreRed:
                nodesInfluenced +=1
                self.redNodeInteraction(node,moveVars[0],False)
        self.greenTurn()
        if nodesInfluenced == 0:
            reward = -100
            gameOver = True
        for node in self.greenArray:
            if node.voteOpinion == False:
                newOpinionCount += 1
        if newOpinionCount == self.numGreen:
            gameOver = True
            reward = 100
        elif newOpinionCount >= oldOpinionCount:
            reward = 10
        else:
            reward = -10

        return reward, gameOver




    

