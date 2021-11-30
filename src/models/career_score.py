class CareerScore:
    """
    Holds the information of a Career
    """

    occupation: str
    code: str
    score: int

    def __init__(self, occupation: str, code: str, score: int):
        self.occupation = occupation
        self.code = code
        self.score = score

