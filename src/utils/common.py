import re

def email_isvalid(email):   
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  
    if(re.search(regex,email)):   
        # print("Valid Email")   
        return True

    else:   
        # print("Invalid Email") 
        return False