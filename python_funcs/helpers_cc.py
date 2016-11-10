#!/usr/bin/env python2
''' 
- Common functions required in coding challenges will be placed here. 
- Also contains my own versions of stuff already found in the Python stdlib (for fun)
- Warning: A lot of this will likely be rough and unoptimized
'''

#import ipdb
from time import sleep
from random import randrange

def sort_asc(list_):
    ''' My custom sorting algo - from lowest to highest (dog slow)'''
    list_ = list_[:]
    if len(list_) <= 1:
        return list_
    sorted_list = []
    while list_:
        lowest = list_[0]
        for i in list_:
            if i < lowest:
                lowest = i
        count = list_.count(lowest)
        _ = 0
        while _ < count:
            list_.remove(lowest)
            sorted_list.append(lowest)
            _ += 1
    
    return sorted_list


def sort_desc(list_):
    return sort_asc(list_)[::-1] # lol


def qsort(array=[12,4,5,6,7,3,1,15]):
    ''' Shamelessly stolen from http://stackoverflow.com/a/18262384 ''' 
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return qsort(less)+equal+qsort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array


def power(x,y):
    '''Raise x to power y'''
    orig_y = y
    if y < 0:
        y *= -1
    i = 0
    a = 1
    while i < y:
        a = a * x
        i += 1

    if orig_y < 0:
        return 1.0/a
    else:
        return a
    

def convert_to_binary(dn):
    ''' Convert decimel integer to binary string'''
    if dn == 0:
        return dn
    powers_collected = []
    exponent = 0
    while True:
        if power(2, exponent) == dn:
            dn = 0
            powers_collected.append(exponent)
            break
        elif power(2, exponent) > dn:
            exponent -= 1
            dn -= power(2,exponent)
            powers_collected.append(exponent)
            exponent = 0
        else:
            exponent += 1

    binary_number_list = [0] * (powers_collected[0]+1)
    for i in powers_collected:
        index = powers_collected[0] - i
        binary_number_list[index] = 1
    
    _ = [str(i)  for i in binary_number_list]
    binary_number_str = "".join(_)
    return binary_number_str


def check_algo(range_=10000000):
    '''To inductively check the veracity of my binary conversion function'''        
    while True:
        number = randrange(range_)
        actual_binary = str(bin(number))[2:]
        my_binary = convert_to_binary(number)
        correct = (actual_binary == my_binary)
        print("Number: %d\tActual Binary: %s\tMy Binary: %s\tResult: %s" % (number, actual_binary, my_binary, str(correct)))
        if not correct:
            print("Error")
            break
        sleep(0.1)

