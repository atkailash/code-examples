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
        return isinstance(other, CoordsURLPair) and (hash(self) == hash(other))


class LRUCache(object):
    def __init__(self, capacity):
        self.pair_dq = deque(maxlen=capacity)
        self.capacity = capacity
        self.dict_of_pairs = {}  # Acts as a map
        self.num_hits = 0
        self.num_miss = 0

    def add(self, coords, url):
        """
        Inserts a node into the deque (pair_dq) and cache (dict_of_pairs)
        If it's already there, it will remove it and update it (to account
        for changed URLs). Should be faster than checking if they're the same,
        or at least less memory intensive.

        Parameters:
        coords (str): the string representation of list [lat, long]
        url (str): the URL value
        """
        coords = str(coords)
        if len(self.pair_dq) == self.capacity:
            # Pop and save it so we can remove from dict
            least_recent = self.pair_dq.pop().key  # We use left for append so this needs to be normal
            del self.dict_of_pairs[least_recent]  # Frees memory, faster than popitem and doesn't return
        entry = CoordsURLPair(coords, url)
        self.pair_dq.appendleft(entry)
        self.dict_of_pairs[coords] = entry
        self.num_miss += 1

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
            the_pair = self.dict_of_pairs[coords]
            url = the_pair.value
            self._dqupdate(the_pair)
            self.num_hits += 1
            return url
        except KeyError:
            return False

    def clear_counters(self):
        self.num_hits = 0
        self.num_miss = 0

    def clear_all(self):
        self.clear_counters()
        self.pair_dq.clear()
        self.dict_of_pairs.clear()

    def show_counters(self):
        return f"Hits: {self.num_hits}, Misses: {self.num_miss}"
