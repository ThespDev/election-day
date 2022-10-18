class GreenAgent:

    def __init__(self, voteOpinion:bool, certainty:float,neighbours:list,id:int, upperbound:float):
        self.voteOpinion = voteOpinion
        self._certainty = certainty
        self.ignoreRed = False
        self.neighbors = neighbours
        self.id = id
        self.certaintyUpperBound = upperbound

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
        return self.neighbors

    def addCertainty(self,certaintyBonus:float) -> None:
        self.certainty += certaintyBonus
        if self.certainty < 0:
            self.certainty = 0
        elif self.certainty > self.certaintyUpperBound:
            self.certainty = self.certaintyUpperBound

    def switchOpinion(self) -> None:
        self.voteOpinion = not self.voteOpinion
     
    def switchIgnore(self) -> None:
        self.ignoreRed = not self.ignoreRed

