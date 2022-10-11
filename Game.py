import BlueAgent,RedAgent,GreenAgent,GreyAgent
import igraph as ig
import argparse
import random
import math

def generateGreenArray(numGreen, interval, votePercent,graph ) -> list:
    greenArray = []
    numVoters = votePercent * numGreen
    numVoters = math.floor(numVoters)
    for i in range(numGreen):
        currCertainty = random.uniform(interval[0],interval[1])
        if numVoters > 0:
            opinion = True
            numVoters -= 1
        else:
            opinion = False
        greenNode = GreenAgent.GreenAgent(opinion,currCertainty,graph.neighbors(i),i)
        greenArray.append(greenNode)
    return greenArray
        
def nodeInteraction(node1 ,node2) -> None:
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

def greenTurn(greenArray):
    interactions  = []
    for node in greenArray:
        for neighbor in node.neighbors:
            interaction = tuple(sorted((node.id,neighbor)))
            if interaction not in interactions:
                interactions.append(interaction)
                nodeInteraction(node,greenArray[neighbor])

    
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
    parser.add_argument('probabilitySpy',type=int,help='Probability of Grey Spy')
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
    while playing not in (1,2):
        playing = int(input("Please select automated or player mode\n [1] - Player\n [2] - Automated\n"))
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
    g = ig.Graph.Erdos_Renyi(n=args.numGreen,p=args.probabilityGreen,directed=False,loops=False)
    red = RedAgent.RedAgent(interval,redAutomated)
    blue = BlueAgent.BlueAgent(interval,blueAutomated)
    greenArray = generateGreenArray(args.numGreen, interval, args.greenvotePercentage,g)
    
    for i in range(100):
        gameover = red.takeTurn(greenArray)
        if gameover:
            print("Every citizen is ignoring Red, Blue has won")
            return 1
        gameover = blue.takeTurn(greenArray)
        if gameover:
            print("Blue has spent all of their energy, Red has won")
            return 0
        greenTurn(greenArray)


if (__name__ == "__main__"):
    blueWins = 0
    redWins = 0
    result = main()
    if result == 1:
        blueWins += 1
    else:
        redWins += 1
    print(f"Blue wins: {blueWins}")
    print(f"Red wins: {redWins}")
    

