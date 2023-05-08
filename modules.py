"""
https://www.geeksforgeeks.org/python-data-structures/

Modules provide containers that let us see 
each one of the data points in detail

Counters are a subclass of a dictionary
used to keep count of elements in an iterable

dicts can be ordered

Chain map
encapsulates multiple dictionaries into a single unit
    from collections import ChainMap

NamedTuple
I belive a named tuple can be used to call an element 
in a list from an element within the element
    from collections import namedTuple
    namedTuple("Name of tuple", (tuple with in tuple))

Deque
is optimized for appending and poping from 
both the left side of the list and the right
    import collections
    de = collections.deque()
        must call deque
    append = right
    appendleft = left

UserDicts
dictionary like container acts 
as wrapper around dictioinary objects
you are able to add your own functionality
    from collections import UserDict 
    create a class for your dict


"""
