class GreenAgent:

    def __init__(self, voteOpinion:bool, certainty:float,neighbours:list):
        self.voteOpinion = voteOpinion
        self.certainty = certainty
        self.ignoreRed = False
        self.neighbours = neighbours
        
    def TakeTurn(self):
        pass

    def getOpinion(self) -> bool:
        return self.voteOpinion
    
    @property
    def certainty(self) -> float:
        return self.certainty
    
    @certainty.setter
    def certainty(self,certaintyValue):
        self.certainty = certaintyValue
    
    def getNeighbours(self) -> list:
        return self.neighbours

    def addCertainty(self,certaintyBonus:float) -> None:
        self.certainty += certaintyBonus

    def switchOpinion(self) -> None:
        self.voteOpinion = not self.voteOpinion
     
    def switchIgnore(self) -> None:
        self.ignoreRed = not self.ignoreRed

