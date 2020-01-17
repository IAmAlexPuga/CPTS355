#Alex Puga 011425121
import re
from HW4_part1 import *
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[\[][a-zA-Z-?0-9_\s!][a-zA-Z-?0-9_\s!]*[\]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)
# COMPLETE THIS FUNCTION
# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatch(it):
    res = []
    for c in it:
        #checks to see if c is open curly braces to create a list
        if c == '}':
            return res
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code-array for the inner 
            # parenthesis, it will be appended to the list we are constructing 
            # as a whole.
            res.append(groupMatch(it))
        else:
            res.append(helper(c))
    return False

#helper function to check if a string is a number, boolean, or user defined string
def helper(c):
    if str.isdigit(c):
        return (int(c))
    elif c[0] == '-':
        return 0 - int(c[1:])
    elif c == 'False':
        return False
    elif c == 'True':
        return True
    else:
        return c

# Helps splits the [ in an array to get the value attached
def arrayHelper(c):
    res = []
    #print(c.split(" "))
    for letter in c.split():
        if '[' in letter:
            return arrayHelper(c[1:])
        elif ']' in letter:
            res.append(helper(letter[0:-1]))
            return (len(res),res)
        else:
            res.append(helper(letter))

# COMPLETE THIS FUNCTION
# Function to parse a list of tokens and arrange the tokens between { and } braces 
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    res = []
    it = iter(L)
    # makes sure the curly braces are matching and appends to the result
    for c in it:
        if c=='}':  #non matching closing parenthesis; return false since there is 
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            res.append(groupMatch(it))
        elif c[0] == '[':
            res.append(arrayHelper(c[1:]))
        else:
            res.append(helper(c))
    return res
#checks to see if given n is a number or not
def isNumber(n):
    if str.isdigit(n) or n[0] == '-':
        return True
    return False

# Replaces any variables declared in the array and inserts its value
def evaluateArray(arr):
    size, array = arr
    for value in array:
        if isinstance(value,str):
            temp = lookup(value)
            if not temp == None:
                arr[1][arr[1].index(value)] = temp
            else:
                print("Variable" + value + " is not defined")
    return arr

# COMPLETE THIS FUNCTION 
# Write auxiliary functions if you need them. This will probably be the largest function of the whole project, 
# but it will have a very regular and obvious structure if you've followed the plan of the assignment.
def interpretSPS(code): # code is a code array
    for token in code:
        # checks to see if the given token is a number, operator, string, or variable defined
        # takes appropriate action of the token.
        if type(token) is tuple:
            opPush(evaluateArray(token))
        elif type(token) == list:
            opPush(token)
        elif isinstance(token, int) or isinstance(token,bool):
            opPush(token)
        elif token[0] == '-':
            opPush(0 - int(token[1:]))
        elif type(token) == str:

            if token in functionList:
                functionList[token]()
            elif token[0] == '/':
                opPush(token)
            else:
                value = lookup(token)
                if value == None:
                    print("Error, " + value + " does not exist")
                elif type(value) == list:
                    interpretSPS(value)
                else:
                    opPush(value)

        else:
            print("Error bug detected for " + token)

# For loop
def psFor():
    # gets the operations, stoping point, incrementor, and start of the for loop
    op = opPop()
    end = opPop()
    inc = opPop()
    start = opPop()
    # calls the helper class to execute the for loop
    forHelper(end, inc,op, start)

# recursive forloop helper method.
def forHelper(end,inc,op,start):
    # pushes the start to stack and calls interpretSPS to perform for loop operations
    # increments the start with the incrementor passed in
    opPush(start)
    interpretSPS(op)
    start += inc
    # checks to see if for loop has been satisfied
    if start == end + inc:
        return;
    forHelper(end, inc, op, start)

# post scrip if
def psIf():
    # if boolean is true then perform operations by calling interpretSPS else continue
    op = opPop()
    boolean = opPop()
    if boolean == True:
        interpretSPS(op)
    elif boolean == False:
        return
    else:
        print("Not a valid comparison command")

# Postscript if else. If boolean is true or false, peforms certain operation by calling interpretSPS
def psIfElse():
    op2 = opPop()
    op1 = opPop()
    boolean = opPop()
    if boolean == True:
        interpretSPS(op1)
    elif boolean == False:
        interpretSPS(op2)
    else:
        print("Not a valid comparison command")

functionList = {'def': psDef, 'aload': aload, 'length': length, 'for': psFor,
                'if': psIf, 'ifelse': psIfElse, 'stack': stack, 'exch': exch,
                'add': add, 'div': div, 'sub': sub, 'mul': mul, 'lt': lt,
                'eq': eq, 'gt': gt, 'get': get, 'put': put, 'astore': astore,
                'dup': dup, 'copy': copy, 'count': count, 'pop': pop, 'clear': clear,
                 'dict': psDict, 'begin': begin, 'end': end}


def interpreter(s): # s is a string
    interpretSPS(parse(tokenize(s)))


#clear opstack and dictstack
def clearStacks():
    opstack[:] = []
    dictstack[:] = []


#testing

input1 = """
        /square {dup mul} def 
        [-5 -4 3 -2 1] dup aload length 0 exch -1 1 
        {pop exch square add} for 
        55 eq stack
        """

input2 ="""
            /n 5 def
            /fact {
                0 dict begin
                /n exch def
                n 2 lt
                { 1}
                {n 1 sub fact n mul }
                ifelse
                end 
            } def
            n fact stack
            """

input3 = """
            /fact{
                0 dict
                begin
                    /n exch def
                    1
                    n -1 1 {mul} for
                end
            } def
            6 fact stack
            """

input4 = """
            /sumArray { 0 exch aload length -1 1 {pop add} for } def
            /x 5 def
            /y 10 def 
            [1 2 3 4 x] sumArray
            [x 7 8 9 y] sumArray
            [y 11 12] sumArray
            [0 0 0] astore
            stack 
        """

input5 = """
            1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq  
            stack 
            """

input6 = """
            /pow2 {1 dict begin 
                     /x exch def 
                     1 x -1 1 {pop 2 mul} for  
                   end } def
            [1 2 3 4 5 6 7] dup /A exch def
            0 1 A length 1 sub { /n exch def A n get pow2 /x exch def A n x put } for 
            A
            stack
            """
input7 = """
        [1 2 3] aload aload length count
        stack
        """
input8 = """
         1 1 10 {10 mul} for
         stack
         """
output7 = "7" \
          "3" \
          "3" \
          "2" \
          "1" \
          "3" \
          "2" \
          "1"
output8 = "100" \
          "90" \
          "80" \
          "70" \
          "60" \
          "50" \
          "40" \
          "30" \
          "20" \
          "10"
interpreter(input8)

# All test cases work!
