class WorkExperience:
    """
    Stores the information of a LinkedIn Work Experience entry
    """

    title: str
    desc: str

    def __init__(self, title: str, desc: str):
        self.title = title
        self.desc = desc
