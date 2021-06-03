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

def findWord(filename:str, word:str):
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

def dataSorter(filename:str):
    """
    Used to sort data acquired from csv file broken up into Category and Value columns. 
    Sorted data is placed in sorteddata.csv file.
    For each column, unique values are recorded in each row. 
    The columns in the output csv are in alphabetical order (left to right). 
    the entries for each category also in alphabetical order (top to bottom).
    Numbers sorted as strings.
    """
    import csv

    # dictionary to store unique values for each category. categories are the keys for dictionary
    dict = {}

    # read specified csv file
    with open(filename,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        category_list = []
        category_value_list = []
        # identify different categories and values for those categories
        for row in reader:
            category_list.append(row["Category"])
            category_value_list.append((row["Category"],row["Value"]))
        # condense down to unique and remove duplicates
        category_set = set(category_list)
        category_list = list(category_set)
        category_list.sort()
        category_value_set = set(category_value_list)
        category_value_list = list(category_value_set)
        category_value_list.sort()
        for category in category_list:
            dict[category] = []
        for tuple in category_value_list:
            dict[tuple[0]].append(tuple[1])
    
    # determine which category has the most unique values from 
    d_keys = list(dict.keys())
    most_vals = max([len(dict[k]) for k in d_keys])

    # write sorted data into sorteddata.csv
    with open('sorteddata.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(dict))
        writer.writeheader()
        csv_row = {}
        # update csv_row dictionary for every row, insert None if no value is available 
        for index in range(most_vals):
            for key in d_keys:
                try:
                    csv_row[key] = dict[key][index]
                except IndexError:
                    csv_row[key] = None
            writer.writerow(csv_row)
            

dataSorter("answer.csv")