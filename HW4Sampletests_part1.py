import unittest
from HW4_part1 import *

class HW4Sampletests_part1(unittest.TestCase):

    def setUp(self):
        #clear the opstack and the dictstack
        opstack [:] = []
        dictstack [:] = []     
       
    def test_lookup(self):
        #/v 3 def /v 4 def /v 5 def v
        dictPush({'/v':3})
        dictPush({'/v':4})
        dictPush({'/v':5})
        self.assertEqual(lookup('v'),5)

    def testLookup2(self):
        #/a 355 def /a [3 5 5] def a
        dictPush({'/a':355})
        dictPush({'/a':[3,5,5]})
        self.assertEqual(lookup("a"),[3,5,5])

    def testLookup3(self):
        #/a 355 def /a [3 5 5] def a
        dictPush({})
        self.assertEqual(lookup("c"),None)

    def testLookup4(self):
        #/a 355 def /a [3 5 5] def a
        dictPush({'/a':355})
        dictPush({'/d': [3, 5, 5]})
        self.assertEqual(lookup("y"), None)

    def test_define(self):
        #/n1 4 def n1
        dictPush({})
        define("/n1", 4)
        self.assertEqual(lookup("n1"),4)


    def test_define2(self):
        #/n1 4 def /n1 5 def n1
        dictPush({})
        define("/n1", 4)
        define("/n1", 5)
        self.assertEqual(lookup("n1"),5)

    def test_define3(self):
        #/n1 4 def n1
        define("/why", 4)
        define("/d", 5)
        self.assertEqual(lookup("why"),4)

    #Arithmatic operator tests
    def test_add(self):
        #9 3 add
        opPush(9)
        opPush(3)
        add()
        self.assertEqual(opPop(),12)

    def test_sub(self):
        #10 2 sub
        opPush(10)
        opPush(2)
        sub()
        self.assertEqual(opPop(),8)

    def test_sub2(self):
        opPush(0)
        opPush(0)
        sub()
        self.assertEqual(opPop(),0)

    def test_mul(self):
        #2 40 mul
        opPush(2)
        opPush(40)
        mul()
        self.assertEqual(opPop(),80)

    def test_mul2(self):
        #2 40 mul
        opPush(1)
        opPush(6)
        mul()
        self.assertEqual(opPop(),6)
   
    #Comparison operators tests
    def test_eq1(self):
        #6 6 eq
        opPush(6)
        opPush(6)
        eq()
        self.assertEqual(opPop(),True)

    def test_eq2(self):
        #[1 2 3 4] [4 3 2 1] eq
        opPush([1,2,3,4])
        opPush([4,3,2,1])
        eq()
        self.assertEqual(opPop(),False)

    def test_eq2(self):
        opPush("aaaa")
        opPush("aaaa")
        eq()
        self.assertEqual(opPop(),True)

    def test_lt(self):
        #3 6 lt
        opPush(3)
        opPush(6)
        lt()
        self.assertEqual(opPop(),True)

    def test_gt(self):
        #4 5 gt
        opPush(4)
        opPush(5)
        gt()
        self.assertEqual(opPop(),False)

    #stack manipulation functions
    def test_dup(self):
        #[3 5 5 True 4]  dup
        opPush((5,[3,5,5,True,4]))
        dup()
        isSame = opPop()[1] is opPop()[1]
        self.assertTrue(isSame)


    def test_exch(self):
        # /x 10 exch
        opPush('/x')
        opPush(10)
        exch()
        self.assertEqual(opPop(),'/x')
        self.assertEqual(opPop(),10)

    def test_pop(self):
        #10 pop
        l1 = len(opstack)
        opPush(10)
        pop()
        l2 = len(opstack)
        self.assertEqual(l1,l2)

    def test_copy(self):
        #true 1 3 4 3 copy
        opPush(True)
        opPush(1)
        opPush(3)
        opPush(4)
        opPush(3)
        copy()
        self.assertTrue(opPop()==4 and opPop()==3 and opPop()==1 and opPop()==4 and opPop()==3 and opPop()==1 and opPop()==True)

    def test_copy2(self):
        opPush(False)
        opPush(6)
        opPush(3)
        opPush(4)
        opPush(3)
        copy()
        self.assertTrue(opPop() == 4 and opPop() == 3 and opPop() == 6 and opPop() == 4 and opPop() == 3 and opPop() == 6 and opPop() == False)
        
    def test_clear(self):
        #10 /x clear
        opPush(10)
        opPush("/x")
        clear()
        self.assertEqual(len(opstack),0)

    #Array operator tests
    def test_length(self):
        #[3 5 5 True 4] length
        opPush((5,[3,5,5,True,4]))
        length()
        self.assertEqual(opPop(),5)

    def test_length2(self):
        opPush((8,[3,5,5,True,4,"dd",4,9]))
        length()
        self.assertEqual(opPop(),8)

    def test_get(self):
        #[3 5 5 True 4] 3 get
        opPush((5,[3,5,5,True,4]))
        opPush(3)
        get()
        self.assertEqual(opPop(),True)

    def test_get2(self):
        #[3 5 5 True 4] 0 get
        opPush((5,[3,5,5,True,4]))
        opPush(0)
        get()
        self.assertEqual(opPop(),3)

    def test_put1(self):
        #[3 5 5 True 4] dup 3 0 put
        opPush((5,[3,5,5,True,4]))
        dup()
        opPush(3)
        opPush(0)
        put()
        self.assertEqual(opPop()[1],[3,5,5,0,4])      

    def test_put2(self):
        #/x [3 5 5 True 4] def  x 2 0 put x
        x = (5,[3,5,5,True,4])
        define('/x',x)
        opPush(x)
        opPush(2)
        opPush(0)
        put()
        self.assertEqual(lookup('x')[1],[3,5,0,True,4])      

    def test_put3(self):
        #[3 5 5 True 4] dup /x exch def 2 0 put x
        opPush((5,[3,5,5,True,4]))
        dup()
        opPush('/x')
        exch()
        psDef()
        opPush(2)
        opPush(0)
        put()
        self.assertEqual(lookup('x')[1],[3,5,0,True,4])

    def test_put4(self):
        #[3 5 5 True 4] dup /x exch def 2 0 put x
        opPush((5,[3,5,5,True,4]))
        dup()
        opPush('/x')
        exch()
        psDef()
        opPush(3)
        opPush(False)
        put()
        self.assertEqual(lookup('x')[1],[3,5,5,False,4])

    def test_aload(self):
        #[3 5 5 True4] aload
        opPush((5,[3,5,5,True,4]))
        aload()
        self.assertTrue(opPop()[1]==[3,5,5,True,4] and opPop()== 4 and opPop()==True and opPop() == 5 and opPop() == 5 and opPop()==3)  

    def test_astore(self):
        #1 2 3 4 True [None,None,None] astore
        opPush(1)
        opPush(2)
        opPush(3)
        opPush(4)
        opPush(True)
        opPush((3,[None,None,None]))  # the array doesn't necessarily neeed to have None values. 
        astore()
        self.assertTrue(opPop()[1]==[3,4,True] and opPop()==2 and opPop()==1)  


    #dictionary stack operators
    def test_dict(self):
        #1 dict
        opPush(1)
        psDict()
        self.assertEqual(opPop(),{})

    def test_psDef(self):
        #/x 10 def /x 20 def x
        dictPush({})
        opPush("/x")
        opPush(10)
        psDef()
        opPush("/x")
        opPush(20)
        psDef()
        self.assertEqual(lookup('x'),20)

    def test_psDef2(self):
        #/x 10 def 1 dict begin /y 20 def x
        dictPush({})
        opPush("/x")
        opPush(10)
        psDef()
        dictPush({})
        opPush("/y")
        opPush(20)
        psDef()
        self.assertEqual(lookup('x'),10)

    def test_beginEnd(self):
        #/x 3 def 1 dict begin /x 4 def end x
        opPush(1)
        psDict()
        opPush("/x")
        opPush(3)
        psDef()
        opPush(1)
        psDict()
        begin()
        opPush("/x")
        opPush(4)
        psDef()
        end() 
        self.assertEqual(lookup('x'),3)

    def test_psDef3(self):
        #/x 3 def 1 dict begin /x 30 def 1 dict begin /x 300 def end x
        # define x in the bottom dictionary
        dictPush({})
        opPush("/x")
        opPush(3)
        psDef()
        # define x in the second dictionary
        dictPush({})
        opPush("/x")
        opPush(30)
        psDef()
        # define x in the third dictionary
        dictPush({})
        opPush("/x")
        opPush(300)
        psDef()
        dictPop()
        self.assertEqual(lookup('x'),30)

    #Tests to check "error checking"

    # # (4 pts) Make sure that the following test prints/raises an error message about the type of the second argument
    # #  Also make sure that the opstack content is : ['/x', 10]
    #def test_divInputs(self):
         #opPush(10)
         #opPush("/x")
         #div()
         #print(opstack)

    # # Make sure that the following test prints/raises an error message about the type of the first argument (the variable name needs be a string)
    # # 4 pts
    #Tests work, get expected results
    #def test_psDefInputs(self):
         #opPush(1)
         #opPush(10)
         #psDef()
         #print(opstack)


if __name__ == '__main__':
    unittest.main()

