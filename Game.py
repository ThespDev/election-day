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
        greenNode = GreenAgent.GreenAgent(opinion,currCertainty,graph.neighbors(i))
        greenArray.append(greenNode)
    return greenArray
        
def nodeInteraction(node1: GreenAgent.GreenAgent ,node2: GreenAgent.GreenAgent) -> None:
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

def greenTurn():
    pass

    
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
    g = ig.Graph.Erdos_Renyi(n=args.numGreen,p=args.probabilityGreen,directed=False,loops=False)
    red = RedAgent.RedAgent()
    blue = BlueAgent.BlueAgent()
    greenArray = generateGreenArray(args.numGreen, interval, args.greenvotePercentage,g)
    
    for i in range(100):
        red.TakeTurn(greenArray)
        blue.TakeTurn(greenArray)
        greenTurn()


if (__name__ == "__main__"):
    main()
    

