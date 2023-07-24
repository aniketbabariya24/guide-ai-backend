import bcrypt
import re


class InfluencersModel:
    def __init__(self, name, email, password):

        if self.email_validator(email) == False:
            raise ValueError("Invalid email format")

        if self.name_validator(name) == False:
            raise ValueError("Invalid name format")

        if self.password_validator(password) == False:
            raise ValueError("Invalid password format")

        hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.name = name
        self.email = email
        self.password = hashedPass

    # regex

    def email_validator(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.search(regex, email):
            return True
        else:
            return False

    def name_validator(self, name):
        regex = '^[a-zA-Z ]+$'
        if re.search(regex, name):
            return True
        else:
            return False

    def password_validator(self, password):
        if len(password) < 6:
            return False
        regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        if re.search(regex, password):
            return True
        else:
            return False
