import csv
import math

print_tree = True
n_nominals = 4
nominals = ["low", "medium", "high", "very high"]
min_threshold_tentative = 0.75


# implements pruning

class Node:
    def __init__(self, name, idx = None, value = None):
        self.name = name
        self.idx = idx
        self.value = value
        self.children = {}
        self.prunable = True # new variable so that the pruner doesnt get stuck
    
    def search(self, v, training_data : list):
        """
        :param v: a test vector
        """
        if self.value != None:
            return self.value
        attr_val = v[self.idx]
        if attr_val in self.children:
            return self.children[attr_val].search(v, training_data)
        else:
            return majority(training_data)
        
    def validate(self, data : list):
        n_total = len(data)
        n_success = 0
        for row in data:
            n_success += row[-1] == self.search(row[:-1], data)
        return n_success / n_total
    
    def is_max_depth(self):
        for c in self.children.values():
            if c.value == None:
                return False
        return True
    
def prune(root : Node, n: Node, data : list):
    # finds some prunable max-depth non-leaf node
    prunable = False
    split_data = split(n.idx, data)
    for c in n.children.keys():
        child = n.children[c] # type: Node

        if child.value != None:
            continue
        elif not child.prunable:
            continue
        elif child.is_max_depth():
            # base case
            init_validity = root.validate(data)
            idx = nominals.index(c)
            nom = majority(split_data[idx])
            n.children[c] = Node(nom, value=nom)
            if root.validate(data) < init_validity:
                n.children[c] = child
            else:
                print("pruned")
            return
        else:
            prunable = True
            idx = nominals.index(c)
            prune(root, child, split_data[idx])
    n.prunable = prunable

def classify_dt(training_filename, testing_filename):
    # training
    data = []
    n_yes = 0
    n_total = 0

    # gets data from csv
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
        
    # gets the tree from training data
    tree = construct_tree(n_columns, data, first_line, [])
    if print_tree:
        display_tree([tree])

    # subtree replacement
    prune(tree, tree, data)

    if print_tree:
        print("brah")
        display_tree([tree])

    # testing
    ret = []
    with open(testing_filename, newline="") as testing_file:
        reader_testing = csv.reader(testing_file)
        for row in reader_testing:
            ret.append(tree.search(row, data))

    return ret

def display_tree(active_nodes : list[Node], depth : int = 1):
    line = ""
    next_layer = []
    # base case
    if active_nodes == []:
        return
    # recursing
    for i in active_nodes:
        if i == None:
            continue
        line += i.name + " " * int(50 / depth) + "|" + " " * int(50/depth)
        for c in i.children.values():
            next_layer.append(c)
    print(line)
    display_tree(next_layer, depth + 1)


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

    if n_yes == 0 or n_yes == n_total:
        return 0
    p = n_yes/n_total
    h = -p * math.log2(p) - (1-p) * math.log2(1-p)
    return h

def info_gain(data, idx):
    """
    :param data: csv data
    :param idx: list index of the attribute we are deciding for
    :return: the information gain
    """
    t1 = entropy(data)
    n_total = len(data)
    split_data = split(idx, data)

    
    t2 = 0
    for i in range(n_nominals):
        if split_data[i] == []:
            continue
        t2 += len(split_data[i])/n_total * entropy(split_data[i])
    return t1 - t2, split_data

def split(idx : int, data : list):
    split_data = [[] for _ in range(n_nominals)]
    for row in data:
        for i in range(n_nominals):
            if row[idx] == nominals[i]:
                split_data[i].append(row)
                break
        else:
            print(f"something weird: {row[idx]} and {nominals[i]}")
    return split_data

def construct_tree(n_columns : int, data : list, attr_list : list, used_attr : list):
    # Edge case
    if data == []:
        return None
    
    # Base case 1: if they are all yes or all no
    clas = data[0][n_columns]
    for i in data:
        if i[-1] != clas:
            break
    else:
        return Node(clas, value=clas)
    
    # base case 2: if nodes have been constructed for all attrs
    mode = majority(data)
    if len(used_attr) == n_columns:
        return Node(mode, value=mode)
    
    # splitting
    idx = None
    best_gain = -1
    new_data = []
    for i in range(n_columns):
        if i in used_attr:
            continue
        gain, split_data = info_gain(data, i)
        if gain > best_gain:
            best_gain = gain
            idx = i
            new_data = split_data

    # base case 3: finding nothing
    if idx == None:
        return Node(mode, value=mode)
    
    n = Node(attr_list[idx], idx)

    for i in range(len(new_data)):
        # base case 4: the list is empty
        if new_data[i] == []:
            n.children[nominals[i]] = Node(mode, value=mode)
        else:
            n.children[nominals[i]] = construct_tree(n_columns, new_data[i], attr_list, used_attr + [idx])
    return n
        
def majority(data : list)->str:
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
    
