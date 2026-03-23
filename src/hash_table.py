import math


class HashTable:

    DEFAULT_CAPACITY = 10007

    def __init__(self, capacity=None):
        self._capacity = capacity or self.DEFAULT_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def _hash(self, key):
        return int(key * 2654435761) % self._capacity

    def insert(self, key, value):
        index = self._hash(key)
        self._buckets[index].append((key, value))
        self._size += 1

        if self.load_factor() > 0.75:
            self._resize()

    def lookup(self, key):
        index = self._hash(key)
        values = []

        for f_key, value in self._buckets[index]:
            if key == f_key:
                values.append(value)

        return values

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def load_factor(self):
        if self._capacity == 0:
            return 0
        return round(self._size / self._capacity, 4)

    def stats(self):
        empty_buckets = 0
        max_chain_length = 0
        avg_chain_length = 0

        for bucket in self._buckets:
            if len(bucket) == 0:
                empty_buckets += 1

            max_chain_length = max(max_chain_length, len(bucket))
            avg_chain_length += len(bucket)

        return {
            "capacity": self.capacity(),
            "size": self.size(),
            "load_factor": self.load_factor(),
            "empty_buckets": empty_buckets,
            "max_chain_length": max_chain_length,
            "avg_chain_length": round(avg_chain_length / self._capacity, 4)
        }

    @staticmethod
    def _next_prime(n):
        if n <= 2:
            return 2

        prime = n
        if prime % 2 == 0:
            prime += 1

        for i in range(3, math.floor(math.sqrt(prime))):
            if prime % i == 0:
                prime += 2

        return prime

    def _resize(self):
        new_capacity = self._next_prime(self._capacity * 2)
        old_buckets = self._buckets

        self._capacity = new_capacity
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)