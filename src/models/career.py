class Career:
    """
    Holds the information of a Career
    """

    occupation: str
    code: str
    weight: int

    def __init__(self, occupation: str, code: str, weight: int):
        self.occupation = occupation
        self.code = code
        self.weight = weight

    def to_string(self):
        """
        :return: The career information formatted to a string
        """
        return "Occupation: " + self.occupation + ", Code: " + self.code + ", Weight: " + str(self.weight)
