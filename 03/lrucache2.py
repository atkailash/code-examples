from collections import deque


class CoordsURLPair(object):
    def __init__(self, coords, url):
        self.value = url
        self.key = str(coords)

    def __repr__(self):
        return f"CoordsURLPair('{self.key}', '{self.value}')"

    def __str__(self):
        return f"('{self.key}', '{self.value}')"

    def __hash__(self):
        return hash((self.key, self.value))

    def __eq__(self, other):
        if isinstance(other, CoordsURLPair):
            return hash(self) == hash(other)
        if type(other) == list:
            return self.key == str(other) # To save using a separate map
        else:
            return False

    
class LRUCache(object):
    def __init__(self, capacity):
        self.pair_dq = deque(maxlen=capacity)
        self.num_hits = 0
        self.num_miss = 0

    def add(self, coords, url):
        """
        Inserts a node into the deque (pair_dq) and cache (dict_of_pairs)
        If it's already there, it will remove it and update it (to account
        for changed URLs). Should be faster than checking if they're the same,
        or at least less memory intensive.

        Since using deque it will automatically remove the oldest

        Parameters:
        coords (str): the string representation of list [lat, long]
        url (str): the URL value
        """
        coords = str(coords)
        entry = CoordsURLPair(coords, url)
        self.pair_dq.appendleft(entry)

    def _dqupdate(self, a_pair):
        """
        Takes the given pair and removes it to add to the most recent

        Parameters:
        a_pair (CoordsURLPair): the pair to remove/readd
        """
        self.pair_dq.remove(a_pair)
        self.pair_dq.appendleft(a_pair)

    def get(self, coords):
        """
        Returns the value of the given key if it exists
        Will also update it so the last node is most recent
        Most recent will be the left side (so it's a logical
        order when reading)

        Parameters:
        coords: the key of the object

        Returns:
        url (str): Value pulled from the pair object
        """
        str(coords)
        try:
            the_pair = self.pair_dq[self.pair_dq.index(coords)]
            url = the_pair.value
            self._dqupdate(the_pair)
            self.num_hits += 1
            return url
        except ValueError:
            self.num_miss += 1
            return False

    def clear_counters(self):
        self.num_miss = 0
        self.num_hits = 0
    
    def get_stats(self):
        return(f"Hits: {self.num_hits}; Misses: {self.num_miss}")