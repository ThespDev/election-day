import random

class BlueAgent:
    
    def __init__(self,interval: list, automated:bool):
        self.certainty = 0
        self.intervalUpperBound = interval[1]
        self.energy = 50
        self.voteOpinion = True
        self.automated = automated



    def Message(self,potency):
        if potency == 1:
            self.energy -= 5
            influence = 0.5 * self.intervalUpperBound
        elif potency == 2:
            self.energy -= 4
            influence = 0.4 * self.intervalUpperBound
        elif potency == 3:
            self.energy -= 3
            influence = 0.3 * self.intervalUpperBound
        elif potency == 4:
            self.energy -= 2
            influence = 0.2 * self.intervalUpperBound
        else:
            self.energy -= 1
            influence = 0.1 * self.intervalUpperBound
        self.certainty = influence

    def nodeInteraction(self,node) -> None:
        if (node.voteOpinion == self.voteOpinion):
            effect = random.uniform(0, self.certainty)
            node.addCertainty(effect)
        else:
            if node.certainty <= self.certainty:
                effect = (-1) * random.uniform(0,self.certainty)
                node.addCertainty(effect)

       
        
    def takeTurn(self,greenArray) -> bool:
        if self.automated:
            selection = random.randint(1,5)
        else:
            agentOrMessage = -1
            while agentOrMessage not in (1,2):
                agentOrMessage = int(input("Send a message or introduce a Grey Agent?\n[1] - Send Message\n[2] - Introduce Grey Agent\n"))
                if agentOrMessage == 1:
                    selection = -1
                    while selection not in range(1,6):
                        selection  = int(input("Select the potency of your message (1-5)\n"))
        self.Message(selection)
        print(f"Blue's energy {self.energy}")
        if self.energy <= 0:
            return True
        for node in greenArray:
            self.nodeInteraction(node)
        return False
                





