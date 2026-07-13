import hashlib
import math
import mmh3


class HyperLogLog:

    def __init__(self, precision=14):
        self.precision = precision
        self.registers = [0] * (2 ** precision)
        self.size = 2 ** precision

    def _hash(self, value):
        return mmh3.hash(
            str(value),
            signed=False
        )

    def add(self, item):
        x = self._hash(item)
        index = x >> (32 - self.precision)
        remaining = (x << self.precision) & 0xffffffff
        rank = self._leading_zeroes(
            remaining,
            32 - self.precision
        )
        self.registers[index] = max(
            self.registers[index],
            rank
        )

    def _leading_zeroes(
        self,
        value,
        max_bits
    ):
        binary = bin(value)[2:].zfill(max_bits)
        zeros = 0
        for bit in binary:
            if bit == "0":
                zeros += 1
            else:
                break
        return zeros + 1

    def count(self):
        m = self.size
        alpha = 0.7213 / (1 + 1.079 / m)
        estimate = (
            alpha *
            m *
            m /
            sum(
                2 ** (-r)
                for r in self.registers
            )
        )
        return int(estimate)