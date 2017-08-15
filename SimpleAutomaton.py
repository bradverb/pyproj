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

a = np.array([1,2,3,4,5,6,7,8,9])
print(a)
b = np.concatenate(([0], a, [6]), axis = 0)
print(b)

for x in np.nditer(a.reshape((3,3))):
    print(x)


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

'''
individual rules
want a funtion that takes the rule as an integer and returns a function to calc the next cell
second (returned) function takes an input of 3 numbers (array) and returns a single value, 0 or 1
'''


def nextcell(rule):
    binrule = np.array(list(np.binary_repr(rule).zfill(8)), np.uint8)
    print('binrule: {}'.format(binrule))
    def getcell(previous_cells):
        selector = {
                '000': binrule[0],
                '001': binrule[1],
                '010': binrule[2],
                '011': binrule[3],
                '100': binrule[4],
                '101': binrule[5],
                '110': binrule[6],
                '111': binrule[7],
                }
        func = selector.get(np.array2string(previous_cells, separator='')[1:4], "nothing")
        #print('binrule: {}'.format(binrule))
        #print('previous cells: {}'.format(str(previous_cells)))
        #print('previous cells as string: {}'.format((np.array2string(previous_cells, separator='')[1:4])))
        return func
    return getcell

def draw_cells(rule, size_x, size_y, padding_style):
    start = mybits(size_x)
    print('starting array: {}'.format(start))
    print('length: {}'.format(len(start)))
    print('padded: {}'.format(mypadding(start, padding_style)))
    bits = np.zeros(shape=(size_y, size_x + 2), dtype=np.uint8)
    bits[0,:] = mypadding(start, padding_style)
    print('nd array bits: {}'.format(bits))    
    cell_func = nextcell(rule)
    '''Starting off with the slow way, try vectorizing and fancy stuff later'''
    print('cell funct of [0, 1, 0]: {}'.format(cell_func(np.array([0, 1, 0]))))
    for y in range(1, size_y):
        for x in range(1, size_x):
            #print('first bits in row: {}.'.format(bits[(y-1), (x-1):(x+2)]))
            bits[y, x] = cell_func(bits[(y-1), (x-1):(x+2)])
        bits[y, :] = mypadding(bits[y, 1:-1], padding_style)
    plt.imshow(bits[:, 1:-2])
    plt.xticks([]), plt.yticks([])
    #fig_size = [6, 6]
    #plt.figure(figsize=fig_size)
    plt.show
draw_cells(84, 32, 32, 'mirror')
   
'''
Seems like a lot of time/operations wasted going to/from strings
What about doing whole calculation as a flat array then reshaping at the very end?
Append new row -> append new row -> append new row -> reshape
...
Any way to do it recursively?
'''
