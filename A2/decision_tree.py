import csv
import math

print_tree = False
nominals = ["low", "medium", "high", "very high"]

class Node:
    def __init__(self, name, idx = None, isleaf = False, value = None):
        self.name = name
        self.idx = idx
        self.children = []
        self.isleaf = isleaf
        self.value = value

class Tree:
    def __init__(self, root : Node, idx : int = None):
        self.root = root
        self.idx = idx

def classify_dt(training_filename, testing_filename):

    # training
    data = []
    n_yes = 0
    n_total = 0
    with open(training_filename, newline="") as training_file:
        reader_training = csv.reader(training_file)
        # gets only the first line, which is useless anyway coz its just data
        first_line = reader_training.__next__()
        n_columns = len(first_line) - 1
        
        # gets the data into an array so we don't have to play with the files
        # also gets the total nyes and nno
        for row in reader_training:
            n_total += 1
            if row[n_columns] == "yes":
                n_yes += 1
            data.append((row))

    # gets the first node
    tree = construct_tree(n_columns, data, first_line, first=True)

    if print_tree:
        display_tree()
            
    # testing
    ret = []
    with open(testing_filename, newline="") as testing_file:
        reader_testing = csv.reader(testing_file)
        for row in reader_testing:
            ret.append(search(tree, row))
    return ret

def display_tree():
    pass

def num(val : str):
    """
    :param val: the value of nominal variable; low, medium, high or very high
    :return: the associated numerical value
    """
    if val == "low":
        return 0
    elif val == "medium":
        return 1
    elif val == "high":
        return 2
    elif val == "very high":
        return 3
    else:
        print(f"unknown variable {val}")

def entropy(data : list):
    """
    :param data: csv data
    :param idx: list index of the attribute we are deciding for
    :return: the entropy H given we split by hte attribute
    """
    n_yes = 0
    n_total = len(data)
    for row in data:
        if row[-1] == "yes":
            n_yes += 1
    return -float(n_yes)/n_total*math.log(float(n_yes)/n_total) - float(n_total - n_yes) * math.log(float(n_total)-n_yes)

def info_gain(data, idx):
    """
    :param data: csv data
    :param idx: list index of the attribute we are deciding for
    :return: the information gain
    """
    t1 = entropy(data)
    pop_spread = [0] * 4
    split_data = [[]*4]

    for row in data:
        if row[idx] == "low":
            pop_spread[0] += 1
            split_data[0].append(row)
        elif row[idx] == "medium":
            pop_spread[1] += 1
            split_data[1].append(row)
        elif row[idx] == "high":
            pop_spread[2] += 1
            split_data[2].append(row)
        elif row[idx] == "very high":
            pop_spread[3] += 1
            split_data[3].append(row)
        else:
            print("something weird")
    
    n_total = sum(pop_spread)
    ret = 0, split_data

    for i in range(4):
        ret -= float(pop_spread[i])/n_total * entropy(split_data[i])
    return ret

def construct_tree(n_columns, data, attr_lst, first = False):
    idx = -1
    lowest_entropy = entropy(data)
    split_data = []

    # base cases
    uniform_class = True
    uniform_attr = True
    for row in data:
        if row[n_columns] != data[0][n_columns]:
            uniform_class = False
            break
        elif row[:-1] != data[0][:-1]:
            uniform_attr = False
            break
    if uniform_class or uniform_attr:
        n = Node(majority(data), isleaf=True, value=majority(data))
        if first:
            return Tree(n)
        return
    
    for i in range(n_columns):
        d, t2 = info_gain(data, i)
        gain = entropy(data) - t2
        if gain < lowest_entropy:
            idx = i
            lowest_entropy = gain
            split_data = d

    n = Node(attr_lst[idx], idx)

    if first:
        tree = Tree(n, idx)

    for i in range(4):
        # the last base case
        if split_data[i] == []:
            n.children.append(Node(majority(data), isleaf=True, value=majority(data)))
        else:
            n.children.append(construct_tree(n_columns, split_data[i], attr_lst))

    if first:
        return tree
    else:
        return n
    
def majority(data : list):
    n_yes = 0
    n_no = 0
    for row in data:
        if row[-1] == "yes":
            n_yes += 1
        else:
            n_no += 1
    if n_yes >= n_no:
        return "yes"
    else:
        return "no"
    
def search(tree : Tree, v : list):
    n = tree.root
    if n.isleaf:
        return n.value
    idx = num(v[tree.idx])

    while not n.isleaf:
        n = n.children[idx]
        idx = num(v[n.idx])

    return n.value
            
#print(classify_dt("A2/pima-indians-diabetes-discrete.csv", "A2/pima-indians-diabetes-test-discrete.csv"))