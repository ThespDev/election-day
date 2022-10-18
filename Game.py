import BlueAgent,RedAgent,GreenAgent
import igraph as ig
import argparse
import random
import math

def generateVoters(votePercent,numGreen):
    numVoters = votePercent * numGreen
    numVoters = math.floor(numVoters)
    return numVoters

def generateGreenArray(numGreen, interval,graph,numVoters ) -> list:
    greenArray = []
    for i in range(numGreen):
        currCertainty = random.uniform(interval[0],interval[1])
        if numVoters > 0:
            opinion = True
            numVoters -= 1
        else:
            opinion = False
        greenNode = GreenAgent.GreenAgent(opinion,currCertainty,graph.neighbors(i),i,interval[1])
        greenArray.append(greenNode)
    return greenArray
        
def nodeInteraction(node1 ,node2) -> None:
    if (node1.getOpinion() == node2.getOpinion()):
        effectNode1 = random.uniform(0,node1.certainty) * 0.05
        effectNode2 = random.uniform(0,node2.certainty) * 0.05
        node1.addCertainty(effectNode2)
        node2.addCertainty(effectNode1)
        #print(f"NODE 1 CERTAINTY{node1.certainty} NODE2 CERTAINTY {node2.certainty}")
    else:
        if node1.certainty < node2.certainty:
            effect = (-1) * random.uniform(0,node2.certainty) * 0.05
            node1.addCertainty(effect)
        elif node1.certainty > node2.certainty:
            effect = (-1) * random.uniform(0,node1.certainty) * 0.05
            node2.addCertainty(effect)
        else:
            pass

def greenTurn(greenArray):
    interactions  = []
    voting_count = 0
    for node in greenArray:
        for neighbor in node.neighbors:
            interaction = tuple(sorted((node.id,neighbor)))
            if interaction not in interactions:
                interactions.append(interaction)
                nodeInteraction(node,greenArray[neighbor])
        if (node.certainty < (0.2*node.certaintyUpperBound)):
            node.voteOpinion = not node.voteOpinion
        if node.voteOpinion:
            voting_count += 1
    return voting_count


    
def positiveInterval(negInterval: list) -> list:
    if negInterval[1] < 0:
        negInterval[0] += (-1*negInterval[1])
        negInterval[1] += (-1*negInterval[1])
    if negInterval[0] < 0:
        negInterval[1] += (-1*negInterval[0])
        negInterval[0] += (-1*negInterval[0])
    return negInterval

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('numGreen',type=int,help='Nubmer of green agents')
    parser.add_argument('probabilityGreen',type=float,help='Probability of green connections')
    parser.add_argument('numGrey',type=int,help='Number of grey agents')
    parser.add_argument('probabilitySpy',type=float,help='Probability of Grey Spy')
    parser.add_argument('certainty',type=str,help='Certainty Interval')
    parser.add_argument('greenvotePercentage',type=float,help='percentage of Green agents ready to vote')
    args = parser.parse_args()
    return args

def main():
    args = getArgs()
    uc = args.certainty
    uc = uc[1:-1]
    uc = uc.split(',')
    for i in range(2):
        uc[i] = float(uc[i])
    interval = positiveInterval(uc)
    playing = -1
    numGreen = args.numGreen
    pGreenVote = args.greenvotePercentage
    pGreenConnection = args.probabilityGreen
    pSpy = args.probabilitySpy
    numGrey = args.numGrey
    while playing not in (1,2):
        #playing = int(input("Please select automated or player mode\n [1] - Player\n [2] - Automated\n"))
        playing = 2
    if playing == 1:
        team = -1
        while team not in (1,2):
            team = int(input("Please select which team you'd like to play\n [1] - Red\n [2] - Blue\n"))
        if team == 1:
            redAutomated = False
            blueAutomated =  True
        else:
            redAutomated = True
            blueAutomated = False
    else:
        redAutomated = True
        blueAutomated = True
    g = ig.Graph.Erdos_Renyi(n=numGreen,p=pGreenConnection,directed=False,loops=False)
    red = RedAgent.RedAgent(interval,redAutomated)
    blue = BlueAgent.BlueAgent(interval,blueAutomated,numGrey,pSpy)
    numVoters = generateVoters(pGreenVote,numGreen)
    greenArray = generateGreenArray(numGreen, interval,g,numVoters)
    
    blueOpinionChange = 0
    redOpinionChange = 0
    blueFollowers = numVoters
    redFollowers = numGreen - numVoters
    while True:
        blueState = [blueOpinionChange,numGrey,pGreenConnection,pGreenVote,blueFollowers]
        redState = [redOpinionChange,numGrey,pSpy,pGreenConnection,pGreenVote,redFollowers]
        redTurnVars = red.takeTurn(greenArray,redState)
        gameover,redMoveFollowers = redTurnVars
        if gameover:
            print("Every citizen is ignoring Red, Blue has won")
            return 1
        blueTurnVars = blue.takeTurn(greenArray,blueState)
        gameover,blueMoveFollowers = blueTurnVars
        if gameover:
            print("Blue has spent all of their energy, Red has won")
            return 0
        voting_count = greenTurn(greenArray)
        redFollowers = numGreen - voting_count
        blueFollowers = voting_count
        print (f"red followers: {redFollowers}")
        print(f"blue followers {blueFollowers}")
        print (f"red move followers {redMoveFollowers}")
        print(f"blue move followers {blueMoveFollowers}")
        blueOpinionChange = blueFollowers - blueMoveFollowers
        redOpinionChange = redFollowers - redMoveFollowers  
        print(f"RED OPINON CHANGE {redOpinionChange} BLUE OPINION CHANGE {blueOpinionChange}")
        if redFollowers == numGreen:
            print("Red has all the followers and has won")
            return 0
        elif blueFollowers == numGreen:
            print("Blue has all the followers and has won")

        


if (__name__ == "__main__"):
    blueWins = 0
    redWins = 0
    for i in range(50):
        result = main()
        if result == 1:
            blueWins += 1
        else:
            redWins += 1
        print(f"Blue wins: {blueWins}")
        print(f"Red wins: {redWins}")
    

