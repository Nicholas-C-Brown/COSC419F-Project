class ApplicationSettings:
    """
    The application's settings
    """

    DRIVER_PATH = 'assets/driver/chromedriver.exe'
    IS_HEADLESS = True

    # Number of skills to process when predicting jobs (-1 = ALL)
    NUM_SKILLS = 5

    # Number of job predictions to list (Must be at least 1)
    NUM_PREDICTIONS = 5
