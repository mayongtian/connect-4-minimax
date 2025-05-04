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
    means_yes = []
    means_no = []
    n_rows = 1
    n_yes = 1
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')
        # the file I submitted has a blank line at the beginning :(
        try:
            first_line = reader_training.__next__()
        except StopIteration:
            return []
        while first_line == []:
            first_line = reader_training.__next__()

        n_columns = len(first_line) - 1

        if first_line[n_columns] == "yes":
            for i in range(n_columns):
                means_yes.append(float(first_line[i]))
                means_no.append(0)
        else:
            for i in range(n_columns):
                means_no.append(float(first_line[i]))
                means_yes.append(0)
        
        for row in reader_training:
            n_rows += 1
            if row[n_columns] == "yes":
                n_yes += 1
                for i in range(n_columns):
                    means_yes[i] = ( float(means_yes[i]) * (n_yes - 1) + float(row[i]))/n_yes
            else:
                for i in range(n_columns):
                    means_no[i] = ( float(means_no[i]) * (n_rows-n_yes - 1) + float(row[i]))/(n_rows - n_yes)

    # gets stdev and n_yes
    var_yes = [0] * n_columns
    var_no = [0] * n_columns
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file, delimiter=',', quotechar='|')
        sigma_yes = [0] * n_columns # sum of square of differences
        sigma_no = [0] * n_columns
        for row in reader_training:
            if row == []:
                continue
            if row[n_columns] == "yes":
                for i in range(n_columns):
                    val = float(row[i])
                    sigma_yes[i] += (val - means_yes[i])**2
            else:
                for i in range(n_columns):
                    val = float(row[i])
                    sigma_no[i] += (val - means_no[i]) ** 2

    # getting bayes probability for each testing thing
    prob_yes = []
    prob_no = []
    evidence_yes = float(n_yes)/n_rows
    evidence_no = float(n_rows - n_yes)/n_rows
    ret = []
    with open(testing_filename, newline="") as testing_file:
        reader_testing = csv.reader(testing_file, delimiter=',', quotechar='|')
        for row in reader_testing:
            prob_yes.append(float(n_yes)/n_rows)
            prob_no.append(float(n_rows - n_yes)/n_rows)
            if row == []:
                continue
            for i in range(n_columns):
                prob_yes[-1] *= (bayes_gauss(float(row[i]), var_yes[i], means_yes[i]))
                prob_no[-1] *= (bayes_gauss(float(row[i]), var_no[i], means_no[i]))
                evidence_yes *= (bayes_gauss(float(row[i]), var_yes[i], means_yes[i]))
                evidence_no *= (bayes_gauss(float(row[i]), var_no[i], means_no[i]))
    for i in range(len(prob_no)):
        prob_yes[i] /= evidence_yes + evidence_no
        prob_no[i] /= evidence_yes + evidence_no
        if prob_yes[i] >= prob_no[i]:
            ret.append("yes")
        else:
            ret.append("no")
    return ret


def bayes_gauss(x : float, var : float, mu : float) -> float:
    """
    :param x: the feature value
    :param var: the standard deviation
    :param mu: the mean
    :ret: the probability P(x|H)
    """
    return 1/(math.sqrt(var * math.pi * 2)) * math.exp(-(x - mu)**2 / (2 * var))