import random

import random_name
import utils
from random_name import UniqueName


class EmailGen:
    SEPARATORS = ["_", "-", ".", "!", "$", "%", "&", "'", "*", "+", "/", "=", "?", "^", "`", "{", "|"]

    def __init__(self, domain: str = "gmail.com"):
        if len(domain) == 0:
            raise ValueError("Domain cannot be empty")
        elif len(domain) > 253:
            raise ValueError("Domain cannot be longer than 253 characters")
        else:
            self.domain = domain
        self.unique_name_gen=UniqueName(utils.Utilities.DATA_DIR_PATH)

    def _generate_n_emails(self, n) -> list:
        '''
        Generates n emails
        '''
        return [self._generate_email() for _ in range(n)]

    def _generate_email(self) -> str:
        '''
        Generates a single email
        '''

        while True:
            chosen_list = random.choice(self.unique_name_gen.LISTS)

            chosen_list_number = [random.randint(0, 9) for _ in range(random.randint(1, 3))]

            first_email_segment = "".join(
                random.choice(chosen_list) + random.choice(self.SEPARATORS) + random.choice(chosen_list))
            print(chosen_list_number)
            if len(first_email_segment) + len(chosen_list_number) <= 64:

                # generate random list of integers and append chosen_list_number ints to first_email_segment
                random_index_list = [random.randint(1, len(first_email_segment) - 1) for _ in
                                     range(len(chosen_list_number))]
                for i in range(len(chosen_list_number)):
                    first_email_segment = first_email_segment[:random_index_list[i]] + str(chosen_list_number[i]) + \
                                          first_email_segment[random_index_list[i]:]

                return first_email_segment + "@" + self.domain
