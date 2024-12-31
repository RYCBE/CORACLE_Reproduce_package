
class UnionFindSet(object):
    """ Union-Find Set """

    def __init__(self, data_list):
        """ Initialize two dictionaries, one storing the parent node of the node and 
            the other storing the size of the parent node.
            When initializing, set the parent node of the node to itself and set the size to 1 """
        self.father_dict = {}
        self.size_dict = {}

        for node in data_list:
            self.father_dict[node] = node
            self.size_dict[node] = 1

    def __str__(self) -> str:
        return str(self.father_dict)

    def find_head(self, node):
        father = self.father_dict[node]
        if (node != father):
            father = self.find_head(father)
        self.father_dict[node] = father
        return father

    def is_same_set(self, node_a, node_b):
        return self.find_head(node_a) == self.find_head(node_b)

    def union(self, node_a, node_b):
        if node_a is None or node_b is None:
            return

        a_head = self.find_head(node_a)
        b_head = self.find_head(node_b)

        if (a_head != b_head):
            a_set_size = self.size_dict[a_head]
            b_set_size = self.size_dict[b_head]
            if (a_set_size >= b_set_size):
                self.father_dict[b_head] = a_head
                self.size_dict[a_head] = a_set_size + b_set_size
            else:
                self.father_dict[a_head] = b_head
                self.size_dict[b_head] = a_set_size + b_set_size

    def out_set(self):
        out = {}
        for i in self.father_dict.items():
            if out.get(i[1]) == None:
                out[i[1]] = []
            out[i[1]].append(i[0])
        return out.values()
