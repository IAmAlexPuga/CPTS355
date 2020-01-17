# Alex Puga
# ------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
opstack = []  # assuming top of the stack is the end of the list


# Now define the helper functions to push and pop values on the opstack
# (i.e, add/remove elements to/from the end of the Python list)
# Remember that there is a Postscript operator called "pop" so we choose 
# different names for these functions.
# Recall that `pass` in python is a no-op: replace it with your code.

def opPop():
    return opstack.pop()
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.


def opPush(value):
    opstack.append(value)


# -------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  # assuming top of the stack is the end of the list


# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    dictstack.pop()
    # dictPop pops the top dictionary from the dictionary stack.


def dictPush(d):
    for var in d:
        if var[0] =='/':
            d[var[1:]] = d.pop(var)
    dictstack.append(d)
    # dictPush pushes the dictionary ‘d’ to the dictstack.
    # Note that, your interpreter will call dictPush only when Postscript
    # “begin” operator is called. “begin” should pop the empty dictionary from
    # the opstack and push it onto the dictstack by calling dictPush.


def define(name, value):
    if not dictstack:
        dictstack.append({})
    dictstack[-1][name[1:]] = value
    # if name not in dictstack[-1]:
    #   dictstack[-1][name] = value
    # else:
    #   dictstack[-1][name] = value
    # add name:value pair to the top dictionary in the dictionary stack.
    # Keep the '/' in the name constant.
    # Your psDef function should pop the name and value from operand stack and
    # call the “define” function.

def lookup(name):
    for dict in reversed(dictstack):
        if name in dict:
            return dict[name]
    return None
    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.

# --------------------------- 10% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters 
# and types of the parameters are correct.

# adds two given numbers by grabbing the top two items in stack.
# checks to see if they are variable names or numbers and gets its true
# value if a variable name.  Throws error if two objects cannon be added together.
def add():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num1 + num2)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")

    # divides two given numbers by grabbing the top two items in stack.
    # checks to see if they are variable names or numbers and gets its true
    # value if a variable name.  Throws error if two objects cannon be divided.
def div():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num1 / num2)
        except:
            raise ValueError("Objects cannot be divided.")
    except:
        raise ValueError("Not enough objects in stack")

# subtracts two given numbers by grabbing the top two items in stack.
# checks to see if they are variable names or numbers and gets its true
# value if a variable name.  Throws error if two objects cannon be subtracted.
def sub():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num2 - num1)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")

# multiplies two given numbers by grabbing the top two items in stack.
# checks to see if they are variable names or numbers and gets its true
# value if a variable name.  Throws error if two objects cannon be multiplied.
def mul():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num1 * num2)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")

# checks if two things are of equal value.
def eq():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num1 == num2)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")

# checks if a value is less than another.
def lt():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num2 < num1)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")

# checks if a value is greater than another.
def gt():
    try:
        num1 = opPop()
        num2 = opPop()
        if isinstance(num2, str):
            num2 = lookup(num2)
        if isinstance(num1, str):
            num1 = lookup(num1)
        try:
            opPush(num2 > num1)
        except:
            raise ValueError("Objects cannot be added together")
    except:
        raise ValueError("Not enough objects in stack")


# --------------------------- 25% -------------------------------------
# Array operators: define the string operators length, get, put, aload, astore
# pushes size of array to stack
def length():
    val = opPop()
    counter = 0
    # checks if val is a variable name to get from dictionary
    if isinstance(val,str):
        for dict in reversed(dictstack):
            if val in dict:
                size, list = dict[val]
                opPush(size)
    # array is given
    else:
        try:
            size, array = val
            opPush(size)
            return
        except:
            opPush(val)
            raise ValueError("Not a valid array.")
    raise ValueError("No array exists with given name: " + val)

# gets a value given an array and index
def get():
    index = opPop()
    array = opPop()
    # checks to see if its a defined variable
    if isinstance(array,str):
        narray = lookup(array)
        if narray == None:
            opPush(array)
            opPush(index)
            raise Exception("No such array exists")
        else:
            i, arr = narray
            if index > i:
                raise Exception("Out of bounds." + index + " > " + i)
            else:
                opPush(arr[index])
    else:
        # array is passed in as value
        try:
            opPush(array[1][index])
        except:
            raise Exception("Not valid index or array")

# replaces a given index to an array with a given value
def put():
    value = opPop()
    index = opPop()
    array = opPop()
    # checks to see if variable is a defined array
    if isinstance(array,str):
        narray = lookup(array)
        if narray == None:
            opPush(array)
            opPush(index)
            opPush(value)
            raise Exception("No such array exists")
        else:
            # array found, replaces value
            i, arr = narray
            if index > i:
                raise Exception("Out of bounds." + index + " > " + i)
            else:
                arr[index] = value
    else:
        try:
            # array was direcly given
            array[1][index] = value
        except:
            raise Exception("Not valid index or array")

# loads an array to the stack
def aload():
    array = opPop()
    if array[0] == '/':
        narray = lookup(array)
        if narray == None:
            opPush(array)
            raise Exception("No such array exists")
        else:
            i, arr = narray
            for elem in arr:
                opPush(elem)
            opPush(array)
    else:
        for elem in array[1]:
            opPush(elem)
        opPush(array)

# stores stack content to an pre defined array with size
def astore():
    array = opPop()
    if array[0] == '/':
        narray = lookup(array)
        if narray == None:
            opPush(array)
            raise Exception("No such array exists")
        else:
            i, arr = narray
            num = i - 1
            for elem in arr:
                arr[num] = opPop()
                num -= 1
            opPush(narray)
    else:
        num = array[0] - 1
        for elem in array[1]:
            array[1][num] = opPop()
            num -= 1
        opPush(array)



# --------------------------- 15% -------------------------------------
# Define the stack manipulation and print operators: dup, copy, pop, clear, exch, roll, stack
# duplicates top most object of stack.
def dup():
    var = opPop()
    var2 = var
    opPush(var)
    opPush(var2)

# copies n stack items
def copy():
    n = opPop()
    tmp = 0
    lst = []
    while tmp < n:
        lst.append(opPop())
        tmp += 1
    for item in reversed(lst):
        opPush(item)
    for item in reversed(lst):
        opPush(item)


def count():
    opPush(len(opstack))

def pop():
    opPop()


def clear():
    opstack.clear()


# swaps the top 2 objects in stack.
def exch():
    val1 = opPop()
    val2 = opPop()
    opPush(val1)
    opPush(val2)

#prints content of stack
def stack():
    for elem in reversed(opstack):
        if isinstance(elem,tuple):
            print(elem[1])
        else:
            print(elem)


# --------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.

def psDict():
    size = opPop()
    #d = dict.fromkeys((range(size)))
    d = {}
    opPush(d)


def begin():
    dictPush(opPop())


def end():
    dictstack.pop()


def psDef():
    value = opPop()
    name = opPop()
    if not isinstance(name, str):
        raise ValueError("Name is not instance of a string.")
    define(name, value)
