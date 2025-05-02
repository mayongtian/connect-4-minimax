# TO BE COPIED INTO THE program.py FILE IN THE Naive Bayes SECTION OF THE ASSIGNMENT

import sys
import os
import csv

def classify_nb(training_filename, testing_filename):
    print(training_filename)

    # file checks
    if not os.path.exists(training_filename):
        print("training file not found", file=sys.stderr)
        return []
    elif not os.path.exists(testing_filename):
        print("testing file not found", file=sys.stderr)
        return []
    
    #training
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')

        """
        training_data = []
        for row in reader_training:
            if row != []:
                new_row = []
                for i in row:
                    if isfloat(i):
                        new_row.append(float(i))
                    else:
                        new_row.append(i)
                training_data.append(new_row)
        """
        # the file I submitted has a blank line at the beginning :(
        next_line = reader_training.__next__()
        while next_line == "":
            next_line = reader_training.__next__()

    # checks if it is discrete or normalised - normalised data will haeve the first entry start with a "0"
    n_columns = len(next_line) - 1
    if next_line == "0":
        normalized = True
    else:
        normalized = False
        return classifier_discrete(training_filename, testing_filename, n_columns)
    
    print(normalized)
        

def classifier_discrete(training_filename, testing_filename, n_columns):
        n_E_array, n_EandH_array, n_total, n_yes = training_discrete(training_filename, n_columns)

        return testing_discrete(testing_filename, n_columns, n_total, n_E_array, n_EandH_array, n_yes)

def training_discrete(training_filename, n_columns):
    # converts the csv into an array of n(E) where n gives the number of appearances the evidence has

    n_E_array = [
        [0] * n_columns,
        [0] * n_columns,
        [0] * n_columns,
        [0] * n_columns
    ]
    # n_EandH_array[0] represents low, 2nd row represents med, then high, then very high. The i, jth entry represents the number of times that the variable j is equal to i

    n_EandH_array = [
        [0] * n_columns,
        [0] * n_columns,
        [0] * n_columns,
        [0] * n_columns
    ]
    # similar but also must be yes
    n_total = 0
    n_yes = 0

    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')
        for row in reader_training:
            print(row)
            if row == []:
                continue
            n_total += 1
            for i in range(n_columns):
                if row[i] == "low":
                    n_E_array[0][i] += 1
                elif row[i] == "medium":
                    n_E_array[1][i] += 1
                elif row[i] == "high":
                    n_E_array[2][i] += 1
                elif row[i] == "very high":
                    n_E_array[3][i] += 1
                else:
                    # print(f"unknown discrete variable {row[i]}", file=sys.stderr)
                    pass

            if row[n_columns] == "yes":
                n_yes += 1
                for i in range(n_columns):
                    if row[i] == "low":
                        n_EandH_array[0][i] += 1
                    elif row[i] == "medium":
                        n_EandH_array[1][i] += 1
                    elif row[i] == "high":
                        n_EandH_array[2][i] += 1
                    elif row[i] == "very high":
                        n_EandH_array[3][i] += 1
    return n_E_array, n_EandH_array, n_total, n_yes

def testing_discrete(testing_filename, n_columns, n_total, n_E_array, n_EandH_array, n_yes):
    # list of probabilities P(yes|Etotal)
    probabilities = []
    with open(testing_filename, newline="") as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            row_prob = []
            
            if row == []:
                continue
            for i in range(n_columns):
                prob = 0 # p(Ei|yes)
                if row[i] == "low":
                    prob = bayes(n_yes, n_EandH_array[0][i], n_E_array[0][i], n_total)
                elif row[i] == "medium":
                    prob = bayes(n_yes, n_EandH_array[1][i], n_E_array[0][i], n_total)
                elif row[i] == "high":
                    prob = bayes(n_yes, n_EandH_array[2][i], n_E_array[0][i], n_total)
                elif row[i] == "very high":
                    prob = bayes(n_yes, n_EandH_array[3][i], n_E_array[0][i], n_total)
                row_prob.append(prob)
            probabilities.append(bayes_flexible(n_yes, n_total, row_prob))
    ret = []
    for i in probabilities:
        if i >= 0.5:
            ret.append("yes")
        else:
            ret.append("no")
        
    return ret


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def bayes(n_E, n_EandH, n_H, n_total):
    """returns P(H|E)"""
    return (float(n_EandH)/n_H * float(n_H)/n_total)/(float(n_E)/n_total)

# returns p(H|E) for multiple variables
def bayes_flexible(n_yes : int, n_E : int, Ei : list[int]):
    """
    :param Ei: list of bayes probability P(Ei|H) for each variable
    """
    ret = float(n_yes)/n_E
    for i in Ei:
        ret *= i
    return ret

print(classify_nb("A2/pima-indians-diabetes-discrete.csv", "A2/pima-indians-diabetes-test-discrete.csv"))