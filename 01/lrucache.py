from collections import deque, OrderedDict


class CoordsURLPair(object):
    def __init__(self, coords, url):
        self.value = url
        self.key = str(coords)

    def __repr__(self):
        return f"CoordsURLPair: key '{self.key}', value '{self.value}''"

    def __str__(self):
        return self.key

    def __hash__(self):
        return hash(self.key)
    
class LRUCache(object):
    def __init__(self, capacity):
        self.list_of_nodes = deque(maxlen=capacity)
        self.capacity = 3000
        self.ordered = OrderedDict()

    def add(self, coords, url):
        """
        Inserts a node into the deque and list
        """
        if coords in self.ordered:
        entry = CoordsURLPair(coords, url)
        self.list_of_nodes.appendleft(entry)
        self.ordered[coords] = entry


    def get(self, key):
        """
        Returns the value of the given key if it exists
        Will also update it so the last node is most recent
        Most recent will be the left side (so it's a logical
        order when reading)

        Parameters:
        key: the key of the object

        Returns:
        node_value (str): Value pulled from the node
        """

        if 