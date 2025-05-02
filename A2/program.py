# for sandboxing


import csv

def normalise(path : str):
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # gets the min and max val for each column
        minvals = [float("inf")]*9
        maxvals = [float("-inf")]*9
        for col in range(9):
            for row in reader:
                if row[col].isnumeric():
                    i = float(row[col])
                    if i < minvals[col]:
                        minvals[col] = i
                    if i > maxvals[col]:
                        maxvals[col] = i
                        

        for row in reader:
            print(', '.join(row))

def bayes_flexible(n_yes : int, n_E : int, *args : int):
    """
    :param *args: the bayes probability for each variable
    """
    ret = float(n_yes)/n_E
    for i in args:
        ret *= i
    return ret