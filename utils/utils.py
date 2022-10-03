import os
from pathlib import Path

import random_name


class Utilities:
    BASE_PATH = Path(os.path.abspath(random_name.__file__)).parent
    DATA_DIR_PATH = os.path.join(BASE_PATH, "data")

    @staticmethod
    def get_app_dir() -> str:
        """
        Gets the app directory where all data related to the script is stored

        :return:
        """

        app_dir = os.path.join(os.path.expanduser("~"), ".generator_mail")
        if not os.path.isdir(app_dir):
            # If the app data dir does not exist create it
            os.mkdir(app_dir)
        return app_dir
