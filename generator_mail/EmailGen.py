import random

import random_name


class EmailGen:
    def __init__(self, domain :str, separator="."):
        if len(domain) == 0:
            raise ValueError("Domain cannot be empty")
        elif len(domain) > 253:
            raise ValueError("Domain cannot be longer than 253 characters")
        else:
            self.domain = domain
            self.separator = separator


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
            chosen_list = random.choice(random_name.LISTS)
            print(type(random.choice(random_name.NAMES)))
            first_email_segment = "".join(
                random.choice(random_name.NAMES) + self.separator + random.choice(chosen_list))
            if len(first_email_segment) <= 64:
                return first_email_segment + "@" + self.domain


if __name__ == "__main__":
    email_gen = EmailGen("gmail.com")
    print(email_gen._generate_email())
