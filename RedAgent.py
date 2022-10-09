import random

class RedAgent:
    
    def __init__(self):
        pass

    def sendMessage(self,potency,node):
        if potency == 1:
            ignoreChance = 0.5
            influence = 0.5
        elif potency == 2:
            ignoreChance = 0.4
            influence = 0.4
        elif potency == 3:
            ignoreChance = 0.3
            influence = 0.3
        elif potency == 4:
            ignoreChance = 0.2
            influence = 0.2
        elif potency == 5:
            ignoreChance = 0.1
            influence = 0.1

    def TakeTurn(self,greenArray: list) -> None:
        for node in greenArray:
            if not node.ignoreRed:
                randomPotency = random.randint(1,5)
                self.sendMessage(randomPotency,node)
                


