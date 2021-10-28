class ApplicationSettings:
    """
    The application's settings
    """

    def __init__(self, driver_path, is_headless):
        self.driver_path = driver_path
        self.is_headless = is_headless
