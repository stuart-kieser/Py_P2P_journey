"""
Loops and functions are the building blocks of any program

loops in python allows for functions to run multiple times in a row. 
"""
for x in range(10):
    print(x)

"""
output: 
0
1
2
3
4
5
6
7
8
9

x represents each number in a data set
"""
list = ["barty", "anne", "gloop"]
while True:
    for y in list:
        print(list[1])

    break
"""
this while loop interates indefinetly until interrupted
if it werent for the break keyword

break is used to break out of loops, note this doesnt end 
the program from running it just breaks this one instance 

pass and continue are used to execute commands depending on criteria supplied in the above code
"""

s = "geeks"
# Pass statement
for i in s:
    if i == "k":
        print("Pass executed")
        pass
    print(i)

print()

# Continue statement
for i in s:
    if i == "k":
        print("Continue executed")
        continue
    print(i)
