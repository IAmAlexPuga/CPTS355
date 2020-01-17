from functools import reduce
import os
#sprintLog
def sprintLog(sprnt):
    #newDic = {{task : worker} for worker in sprnt for task in worker }
    newDic = { }
    workers = list(sprnt.keys())
    tasks = list(sprnt.values())
    List = set()

    #grabs all the tasks and inserts to set List
    for task in tasks:
        titles = task.keys()
        for title in titles:
            if title not in List:
                List.add(title)

    #sorts the Lists contents (tasks)
    List = set(sorted(List))


    #create a temp to store all the workers for a given task
    for task in List:
        temp = {}
        i = 0
        for value in sprnt.values():
            tempValues = value.keys()
            if task in tempValues:
                temp[workers[i]] = value[task]
            i+=1
        newDic[task] = temp

    return dict(sorted(newDic.items()))

#addSprints
def addSprints(sprint1,sprint2):
    #assings first sprint to result sprint
    returnMe = sprint1
    keyList = sprint2.keys()
    #gets tasks and checks to see if each sprint is in returnMe
    for task in sprint2.keys():
        temp = sprint2[task]
        temp3 = {}
        #if task not in returnMe add the whole dic to list, else check and/or add each persons hours
        if task not in returnMe.keys():
            returnMe[task] = temp
        else:
            temp2 = sprint1[task]
            for person in temp2:
                if person in temp:
                    temp3[person] = temp2[person] + temp[person]
                else:
                    temp3[person] = temp2[person]
            for person in temp:
                if person not in temp3:
                    temp3[person] = temp[person]

            returnMe[task] = temp3

    return returnMe

#addNLogs
def addNLogs(logList):
    listOfDics = list(map(sprintLog,logList))
    #returns the requested format
    return dict(sorted(reduce(addSprints, listOfDics).items()))

#lookupVal
def lookupVal(tL,k):
    #reverse the list and starts checking from last element to first if key is contained
    for key in reversed(tL):
        if k in key:
            return key[k]

#lookupVal2
def lookupVal2(tL,k):
    v, dic = tL[-1]
    tv,tdic = tL[0]
    #makes sure not stuck in loop if key isnt found then returns none. If key found return value of key
    while (not(v,dic) == (tv,tdic)):
        if k in dic:
            return dic[k]
        else:
            tv = v
            tdic = dic
            v,dic = tL[v]
    return None

#unzip
def unzip(L):
    #grabs a list of each individual requested item and returns a tuple.
    nums = list(map((lambda x : x[0]), L))
    lett = list(map((lambda x: x[1]), L))
    dic = list(map((lambda x: x[2]), L))
    returnMe = (nums, lett, dic)
    return returnMe


#numPaths
#decreases each value of m and n one at a time. If both 1 then return 1 for successful path.
#if both are less than 1 return 0 since continuing in non exist path.
def numPaths(m,n,blocks):
    if m == 1 and n == 1:
        return 1
    if m < 1 or n < 1:
        return 0
    for (x,y) in blocks:
        if (m, n) != (x,y):
            return numPaths(m -1, n, blocks) + numPaths(m, n-1,blocks)
        else:
            return 0

#iterFile
class iterFile():
    #initilaizes iterfile
    #opens a file of given text and initializes file and path
    def __init__(self, text):
        self.file = open(text, 'r')
        self.Line = list()
        self.path = text

    #grabs a line of the file. if the line contains no more words then grab another line
    #until no more exist.
    def __next__(self):
        checker = 0
        while not self.Line:
            self.Line = (self.file.readline()).split()
            checker += 1
            if checker == 5:
                self.file.close()
                return None
        return self.Line.pop(0)

    def __iter__(self):
        return self

#grabs a list of words and checks if word already exists in a dic d.
#if not exist initializes it. If does add one more count to it
#returns a tuple.
def wordHistogram(words):

    nL = list()
    d = { }
    word = words.__next__()
    while word:
        if word in d.keys():
            d[word] = d[word] + 1
        else:
            d[word] = 1
        word = words.__next__()
    return [(key,val) for key,val in d.items()]


