class GreenAgent:

    def __init__(self, voteOpinion:bool, certainty:float,neighbours:list,id):
        self.voteOpinion = voteOpinion
        self._certainty = certainty
        self.ignoreRed = False
        self.neighbors = neighbours
        self.id = id
        
    def TakeTurn(self):
        pass

    def getOpinion(self) -> bool:
        return self.voteOpinion
    
    @property
    def certainty(self) -> float:
        return self._certainty
    
    @certainty.setter
    def certainty(self,certaintyValue):
        self._certainty = certaintyValue
    
    def getNeighbours(self) -> list:
        return self.neighbours

    def addCertainty(self,certaintyBonus:float) -> None:
        self.certainty += certaintyBonus

    def switchOpinion(self) -> None:
        self.voteOpinion = not self.voteOpinion
     
    def switchIgnore(self) -> None:
        self.ignoreRed = not self.ignoreRed

