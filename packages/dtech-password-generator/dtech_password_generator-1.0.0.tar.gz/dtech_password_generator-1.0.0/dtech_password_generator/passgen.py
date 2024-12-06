### Password Generator
import string
import random
import math



#Lower case alphabets
lowercase_letters = string.ascii_lowercase

#Upper Case alphabets
uppercase_letters = string.ascii_uppercase

#Special Characters
punctuation = string.punctuation

# Define Digits
digits = string.digits


all_options = [lowercase_letters,uppercase_letters,punctuation,digits]

#Define the password Limits
min_length = 7
max_length = 35
default_length = 10

def password(length=default_length):
    try:
        # Ensure that the lenght is an integer.
        length = int(length)
        if length not in (range(min_length,max_length+1)):
            message = f"Length must be within {min_length} and {max_length}"
            # print(message)
            return message
        #calculate expected input of each category and round it up!
        share_index = math.ceil(length/len(all_options)) + 1

        #Get a suggested password!
        suggested_password = []
        for option in all_options:
            suggested_password.append(random.sample(option,share_index))

        
        #Select the password and clean it
        clean_suggested_password = [item for sublist in suggested_password for item in sublist]
        # print(clean_suggested_password)
        final_password = ''.join(random.sample(clean_suggested_password,length))
        # print(final_password)
        return final_password

    except:
        message = 'You Must pass an interger! Try again'
        # print(message)
        return message
    

# password(15)
# password(20)
