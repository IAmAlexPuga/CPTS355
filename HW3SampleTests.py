import unittest
from HW3 import *

class HW3SampleTests(unittest.TestCase):
    def setUp(self):
        # sprintLog inputs
        self.log1 = {'John': {'task1': 5}, 'Rae': {'task1': 10, 'task2': 4}, 'Kelly': {'task1': 8, 'task3': 5}, 'Alex': {'task1': 11, 'task2': 2, 'task3': 1}, 'Aaron': {'task2': 15}, 'Ethan':{'task3': 12}, 'Helen': {'task3': 10}}
        self.log2 = {'Mark': {'task1': 5, 'task2': 2}, 'Kelly': {'task1': 10}, 'Alex': {'task1': 15, 'task2': 2}, 'Rae': {'task2': 10}, 'Aaron': {'task2': 10}, 'Helen': {'task4': 16}}
        self.log3 = {'Aaron': {'task5': 15, 'task6': 8}, 'Rae': {'task5': 20}, 'Helen': {'task6': 16}}
        self.log4 = {'Alex': {'task6': 15}, 'Kelly': {'task5': 20}, 'Helen': {'task6': 10}}
        self.log4 = {'Alex': {'task6': 15}, 'Kelly': {'task1': 20}}
        self.log5 = {'BILLY': {'task1': 15}}
        # addSprints inputs/outputs
        self.sprint1 = {'task1': {'John': 5, 'Rae': 10, 'Kelly': 8, 'Alex': 11}, 'task2': {'Rae': 4, 'Alex': 2, 'Aaron': 15}, 'task3': {'Kelly': 5, 'Alex': 1, 'Ethan': 12, 'Helen': 10}}
        self.sprint2 = {'task1': {'Mark': 5, 'Kelly': 10, 'Alex': 15}, 'task2': {'Mark': 2, 'Alex': 2, 'Rae': 10, 'Aaron': 10}, 'task4': {'Helen': 16}}
        self.addedSprints = {'task1': {'John': 5, 'Rae': 10, 'Kelly': 18, 'Alex': 26, 'Mark': 5}, 'task2': {'Rae': 14, 'Alex': 4, 'Aaron': 25, 'Mark': 2}, 'task3': {'Kelly': 5, 'Alex': 1, 'Ethan': 12, 'Helen': 10}, 'task4': {'Helen': 16}}
        self.sprint3 = {'task5': {'Aaron': 15, 'Rae': 20}, 'task6': {'Aaron': 8, 'Helen': 16}}
        self.sprint4 = {'task1': {'Kelly': 20}, 'task6': {'Alex': 15}}
        self.sprint5 = {'task1': {'Zebra':1005}}
        self.addedSprints2 = {'task5': {'Aaron': 15, 'Rae': 20}, 'task6': {'Aaron': 8, 'Helen': 16, 'Alex': 15}, 'task1': {'Kelly': 20}}
        self.addedSprints3 = {'task5': {'Aaron': 15, 'Rae': 20}, 'task6': {'Aaron': 8, 'Helen': 16, 'Alex': 15}, 'task1': {'Kelly': 20, 'Zebra': 1005}}
        # addNLogs input/output
        self.logList = [self.log1,self.log2,self.log3,self.log4]
        self.logList2 = [self.log5]
        self.logList3 = [self.log5,self.log5]
        self.sprintSummary2 = {'task1': {'BILLY': 15}}
        self.sprintSummary3 = {'task1': {'BILLY': 30}}
        self.sprintSummary = {'task1': {'John': 5, 'Rae': 10, 'Kelly': 38, 'Alex': 26, 'Mark': 5}, 'task2': {'Rae': 14, 'Alex': 4, 'Aaron': 25, 'Mark': 2}, 'task3': {'Kelly': 5, 'Alex': 1, 'Ethan': 12, 'Helen': 10}, 'task4': {'Helen': 16}, 'task5': {'Aaron': 15, 'Rae': 20}, 'task6': {'Aaron': 8, 'Helen': 16, 'Alex': 15}}
        #lookupVal inputs
        self.lookupList = [{"x":1,"y":True,"z":"found"},{"x":2},{"y":False}]
        self.lookupList2 = [{"a": 20, "v": True, "t": "wow"}, {"k": True}]
        self.lookup2List = [(0,{"x":0,"y":True,"z":"zero"}), (0,{"x":1}), (1,{"y":False}), (1,{"x":3, "z":"three"}), (2,{})]
        # iterFile output
        self.filetokens = ["CptS","355","Assignment","3","-","Python","Warmup","This","is","a","text","test","file","for","CptS","355","-","Assignment","3","-","Python","Warmup","With","some","repeated","text","for","CptS","355","-","Assignment","3","-","Python","Warmup","."]
        self.histogram = [('-', 5), ('3', 3), ('355', 3), ('Assignment', 3), ('CptS', 3), ('Python', 3), ('Warmup', 3), ('for', 2), ('text', 2), ('.', 1), ('This', 1), ('With', 1), ('a', 1), ('file', 1), ('is', 1), ('repeated', 1), ('some', 1), ('test', 1)]
        #unzip
        self.unzip1 =  ([(1,"a",{1:"a"}),(2,"b",{2:"b"}),(3,"c",{3:"c"}),(4,"d",{4:"d"})])
        self.unzip2 =  ([(10,"d",{1:"a"}),(20,"b",{2:"b"}),(30,"d",{3:"c"}),(40,"b",{4:"d"})])
        self.unzipAns1 = ([1, 2, 3, 4], ['a', 'b', 'c', 'd'], [{1: 'a'}, {2: 'b'}, {3: 'c'}, {4: 'd'}])
        self.unzipAns2 = ([10, 20, 30, 40], ['d', 'b', 'd', 'b'], [{1: 'a'}, {2: 'b'}, {3: 'c'}, {4: 'd'}])
        self.histoAns1 = [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1), ('f', 1)]
        self.histoAns2 = [('my', 1), ('name', 1), ('is', 1), ('Alex', 1), ('eof', 1)]

    def test_sprintLog(self):
        self.assertDictEqual(sprintLog(self.log1),self.sprint1)
        self.assertDictEqual(sprintLog(self.log2),self.sprint2)
        self.assertDictEqual(sprintLog(self.log3), self.sprint3)
        self.assertDictEqual(sprintLog(self.log4), self.sprint4)

    def test_addSprints(self):
        self.assertDictEqual(addSprints(self.sprint1,self.sprint2),self.addedSprints)
        self.assertDictEqual(addSprints(self.sprint3, self.sprint4), self.addedSprints2)
        self.assertDictEqual(addSprints(self.sprint3, self.sprint5), self.addedSprints3)

    def test_addNLogs(self):
        self.assertDictEqual(addNLogs(self.logList), self.sprintSummary)
        self.assertDictEqual(addNLogs(self.logList2), self.sprintSummary2)
        self.assertDictEqual(addNLogs(self.logList3), self.sprintSummary3)

    def test_lookupVal(self):
        self.assertEqual(lookupVal(self.lookupList,"x"),2)
        self.assertEqual(lookupVal(self.lookupList,"y"),False)
        self.assertEqual(lookupVal(self.lookupList,"z"),"found")
        self.assertEqual(lookupVal(self.lookupList,"t"),None)
        self.assertEqual(lookupVal(self.lookupList, "fun"), None)
        self.assertEqual(lookupVal(self.lookupList, "a"), None)

    def test_lookupVal2(self):
        self.assertEqual(lookupVal2(self.lookup2List,'y'), False)
        self.assertEqual(lookupVal2(self.lookup2List,'word'), None)

    def test_unzip(self):
        self.assertEqual(unzip(self.unzip1), self.unzipAns1)
        self.assertEqual(self.unzipAns2, unzip(self.unzip2) )
    
    def test_numPaths(self):
        self.assertEqual(numPaths(2,2,[(1,2)]), 1)
        self.assertEqual(numPaths(4,3,[(2,2)]), 4)

    def test_iterFile(self):
        mywords = iterFile("testfile.txt")
        self.assertEqual(mywords.__next__(),"CptS")  
        self.assertEqual(mywords.__next__(),"355")
        self.assertEqual(mywords.__next__(),"Assignment")
        restofFile = []
        for word in mywords:
            if word == None:
                break;
            restofFile.append(word)
        self.assertEqual(restofFile,self.filetokens[3:])

        test2 = iterFile("test2.txt")
        test3 = iterFile("test3.txt")
        self.assertEqual(test2.__next__(), "a")
        self.assertEqual(test2.__next__(), "b")
        self.assertEqual(test2.__next__(), "c")
        self.assertEqual(test2.__next__(), "d")
        self.assertEqual(test2.__next__(), "e")
        self.assertEqual(test2.__next__(), "f")

        self.assertEqual(test3.__next__(), "my")
        self.assertEqual(test3.__next__(), "name")
        self.assertEqual(test3.__next__(), "is")
        self.assertEqual(test3.__next__(), "Alex")
        self.assertEqual(test3.__next__(), "eof")
        self.assertEqual(test3.__next__(), None)

    def test_wordHistogram(self):
        self.assertEqual(wordHistogram(iterFile("test2.txt")), self.histoAns1)
        self.assertEqual(wordHistogram(iterFile("test3.txt")), self.histoAns2)

if __name__ == '__main__':
    unittest.main()
    print("Done")

