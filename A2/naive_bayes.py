# TO BE COPIED INTO THE program.py FILE IN THE Naive Bayes SECTION OF THE ASSIGNMENT

import sys
import os
import csv
import math

def classify_nb(training_filename, testing_filename):

    # file checks
    if not os.path.exists(training_filename):
        print("training file not found", file=sys.stderr)
        return []
    elif not os.path.exists(testing_filename):
        print("testing file not found", file=sys.stderr)
        return []
    
    #training

    # gets means
    n_columns = 0
    means = []
    n_rows = 1
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')
        # the file I submitted has a blank line at the beginning :(
        first_line = reader_training.__next__()
        while first_line == []:
            first_line = reader_training.__next__()

        n_columns = len(first_line) - 1
        for i in range(n_columns):
            means.append(float(first_line[i]))
        
        for row in reader_training:
            n_rows += 1
            for i in range(n_columns):
                means[i] = ( float(means[i]) * (n_rows - 1) + float(row[i]))/n_rows

    # gets stdev
    stdev = [0] * n_columns
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')
        sigma = [0] * n_columns # sum of square of differences
        for row in reader_training:
            if row == []:
                continue
            for i in range(n_columns):
                val = float(row[i])
                sigma[i] += (val - means[i])**2

        for i in range(n_columns): stdev[i] = math.sqrt(sigma[i]/(n_rows - 1))


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    

print(classify_nb("A2/pima-indians-diabetes-normalized.csv", "A2/pima-indians-diabetes-test-discrete.csv"))