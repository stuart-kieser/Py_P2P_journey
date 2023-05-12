# Data structures
"""
Method of organizing data
instead of a=1 b=2 c=3
list = 1, 2, 3

linked list 
pointers to different node

each data element has a pointer to the net data element

types of data structures:

linear data structures:

    arrays are an example of this
        data is stored sequentialy after each other

    stack data structures 
        add the latest bit of data to the top of the file there fore it is likely to be removed first

    queue data structures
        opperate on FIFO
        first in first out

    linked list data structure
        data is connected through a series of nodes
        each node contains data items of previous node        

Non linear data structures
    no sequence is required
    arranged in hierarchical manner

    graph data structure
        each node is a vertex and is connected to other nodes through verticies

    Trees Data Structure
        in a tree structure each node can only have two children. 
        there are different types of trees

"""
"""
Dictionary operations in python

unordered collection of data values

store data values like map
    has key:value pair
    indexing of a dictionary is done with keys

    a dictionary basically lets you create an 
    sql like stucture where you can tie data, 
    variables or strings to a specific number or id

    
Set operations in python

unordered collection of data that doesnt allow duplicates. 


Bytearray operations in python
    gives a mutable sequence of integers in the range 0 <= x < 256

"""
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
