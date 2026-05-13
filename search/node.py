
# healthcare-navigation/search/node.py

class Node:
    """
    Representation of a node in the search tree.
    """
    __slots__ = ['osmid', 'g_cost', 'parent']

    def __init__(self, osmid, g_cost=0.0, parent=None):
        self.osmid = osmid
        self.g_cost = g_cost  # Cumulative distance in meters
        self.parent = parent

    def path(self):
        """
        Reconstructs the path from the root to this node.
        Returns:
            list: List of OSMID integers.
        """
        node = self
        path_list = []
        while node:
            path_list.append(node.osmid)
            node = node.parent
        return path_list[::-1]

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.osmid == other.osmid
        return self.osmid == other

    def __hash__(self):
        return hash(self.osmid)
    
    def __lt__(self, other):
        # Tie-breaking for priority queues
        return self.osmid < other.osmid
