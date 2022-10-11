import json


class CommonFN:
    @staticmethod
    def save_email_pass_as_json(emails: list, passws:list, file_path: str) -> None:
        """
        Save email and password to file
        :param emails:
        :param passws:
        :param file:
        :return:
        """
        with open(file_path, "w") as f:
            json.dump({"emails": emails, "passwords": passws}, f,indent=4)


    @staticmethod
    def load_email_pass( file: str) -> dict:
        """
        Load email and password from file
        :param file:
        :return:
        """
        with open(file, "r") as f:
            data = json.load(f)
        return data


