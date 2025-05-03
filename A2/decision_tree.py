

class node:
    def __init__(self, n_yes, n_no, parent = None, isleaf = False, ):
        self.isleaf = isleaf
        self.children = {}
        self.parent = parent
        self.n_yes = n_yes
        self.n_no = n_no