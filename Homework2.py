def gen_code_file(secretword: str, freq:int = 0, maxlength:int = 100000):
    """
    That generate a file containing maxlength random english letters (a to z and A to Z) and places the secretword in the file freq number of times at random locations 
    First occurence of the word is concatenated with today’s date as yyyy-mm-dd. File created is “random_letters_new.txt”
    The freq can be 0.  No word gets written. File with only random characters gets generated.
    """
    import string
    import random
    from datetime import date

    # checks and error handling 
    try:
        freq = int(freq)
        maxlength = int(maxlength)
    except ValueError:
        print("frequency and maxlength must be integers")
        exit(-1)

    if freq < 0:
        print("unable to do negative frequencies")
        return -1

    if len(secretword) > 16:
        print("secret word needs to be 16 characters long or less")
        return -1

    if len(secretword) >= maxlength:
        print("secret word cannot be as large or larger than max file length")
        return -1

    # file to write to
    file_name = 'random_letters_new.txt'

    # if frequency of word is not 0
    if freq != 0:
        # to avoid cut off words
        boundaries = [i for i in range(maxlength) if i%200 == 0 and i != 0]
        restricted = []
        restricted_boundary = 0
        for val in boundaries:
            restricted_boundary = 1
            while restricted_boundary <= len(secretword):
                restricted.append(val - (len(secretword)-restricted_boundary))
                restricted_boundary += 1
        restricted.sort()

        random_locations = list() 
        while freq != 0:
            random_location = random.randint(0,maxlength-1)
            while random_location + len(secretword) > maxlength:
                random_location = random.randint(0,maxlength-1)
            if len(random_locations) > 0:
                valid_loc = len(list(filter(lambda x: abs(x - random_location) <= len(secretword),random_locations)))
                while random_location + len(secretword) > maxlength or valid_loc != 0 or random_locations in restricted:
                    random_location = random.randint(0,maxlength-1)
                    valid_loc = len(list(filter(lambda x: abs(x - random_location) <= len(secretword),random_locations)))
                random_locations.append(random_location)
            elif len(random_locations) == 0:
                random_locations.append(random_location)
            freq -= 1
        random_locations.sort()

        secret_word_list = [] 
        for i in range(len(random_locations)):
            if i == 0:
                secret_word_list.append(secretword + str(date.today()))
            else:
                secret_word_list.append(secretword)

        col = 0
        with open(file_name,'w') as f:
            while f.tell() < maxlength:
                if f.tell() + 1 in random_locations:
                    i = random_locations.index(f.tell() + 1)
                    f.write(secret_word_list[i])
                    print(secret_word_list[i])
                    col += len(secret_word_list[i])

                else:
                    if col < 199:
                        f.write(random.choice(string.ascii_letters))
                        col += 1
                    else:
                        f.write("\n")
                        col = 0

    # if frequency of word is zero, just fill in txt file with random ascii characters
    else:
        col = 0 
        with open(file_name,'w') as f:
            while f.tell() < maxlength:
                if col < 199:
                    f.write(random.choice(string.ascii_letters))
                    col += 1
                else:
                    f.write("\n")
                    col = 0

def findWord (filename:str, word:str):
    """
    Returns a list of integers with all the locations the word appears.
    From earliest to latest positions.
    Returns an empty list if the word is not in the file then.
    If the input file doesn’t exist, print a warning and return -1. 
    """
    try:
        with open(filename) as f:
            text = f.read()
    except FileNotFoundError:
        print("File was not found.")
        return -1

    occurances = list()
    i = 0
    i = text.find(word,i)+1
    if i != 0:
        occurances.append(i)
        while i != 0:
            i = text.find(word,i)+1
            if i == 0:
                break
            occurances.append(i)
    print(occurances)
    return occurances


# used for testing functions above
# gen_code_file("star",3)
gen_code_file("star", 4,maxlength=1000)
findWord("random_letters_new.txt","star")