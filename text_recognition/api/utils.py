import json
import re


def check_password(password:str)->bool:
    if (len(password)<8):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$]", password):
        return False
    elif re.search("\s", password):
        return False
    else:
        return True


