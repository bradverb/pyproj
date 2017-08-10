# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 20:37:31 2017

@author: brad
"""

import numpy as np
from matplotlib import pyplot as plt

#get some random bits
def mybits(nbits = 32):
    mybytes = np.random.bytes(nbits)
    bitstring = list(map(lambda byte: bin(byte)[2:].zfill(8), mybytes))
    bits = np.array((list(''.join(bitstring))), np.uint8)
    return bits[0:nbits]

def get_a_func(arg, *args):
    selector = {
            'plus': np.add,
            'minus': np.subtract,
            }
    func = selector.get(arg, "nothing")
    return func(*args)

a = np.array([1,2,3,4,5])
print(a)
b = np.concatenate(([0], a, [6]), axis = 0)
print(b)


def mypadding(a, style):
    selector = {
            'mirror': lambda array: np.concatenate(([array[0]], array, [array[-1]]), axis = 0),
            'wrap': lambda array: np.concatenate(([array[-1]], array, [array[0]]), axis = 0),
            'zeros': lambda array: np.concatenate(([0], array, [0]), axis = 0),
            'ones': lambda array: np.concatenate(([1], array, [1]), axis = 0),
            '01': lambda array: np.concatenate(([0], array, [1]), axis = 0),
            '10': lambda array: np.concatenate(([1], array, [0]), axis = 0),
            }
    func = selector.get(style, "nothing")
    return func(a)

''' next up: implement the individual automoton operations:
    *check previous row n-1, n, n+1
    *determin new value
    *add next row
'''