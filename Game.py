import BlueAgent,RedAgent,GreenAgent,GreyAgent
import igraph as ig
import argparse



def generateGreenArray(connections,numGreen):
    greenArray = []
    for i in range(numGreen):
        greenNode = GreenAgent.GreenAgent()
        
        
    


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('numGreen',type=int,help='Nubmer of green agents')
    parser.add_argument('probabilityGreen',type=float,help='Probability of green connections')
    parser.add_argument('numGrey',type=int,help='Nubmer of grey agents')
    parser.add_argument('uncertainty',type=str,help='Uncertainty Interval')
    parser.add_argument('greenvotePercentage',type=float,help='percentage of Green agents ready to vote')
    args = parser.parse_args()
    return args

def main():
    args = getArgs()
    print("Arg values")
    print(args.numGreen)
    print(args.numGrey)
    uc = args.uncertainty
    uc = uc[1:-1]
    uc = uc.split(',')
    for i in range(2):
        uc[i] = float(uc[i])
    print(uc)
    print(args.greenvotePercentage)

    g = ig.Graph.Erdos_Renyi(n=args.numGreen,p=args.probabilityGreen,directed=False,loops=False)
    red = RedAgent.RedAgent()
    blue = BlueAgent.BlueAgent()
    greenArray = generateGreenArray(g.get_edgelist,args.numGreen)
    print(g)
    print(g.get_edgelist())

    for i in range(100):
        red.TakeTurn()
        blue.TakeTurn()



if (__name__ == "__main__"):
    main()
    

