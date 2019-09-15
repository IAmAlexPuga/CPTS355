-- CptS 355 - Fall 2019 Assignment 2
-- Please include your name and the names of the students with whom you discussed any of the problems in this homework

module HW2
     where


{- 1-  merge2 & merge2Tail & mergeN - 22% -}
--merge2
merge2 :: Ord a => [a] -> [a] -> [a]
merge2 [] [] = []
merge2 (x:xs) [] = x : (merge2 xs [])
merge2 [] (b:bs) = b : (merge2 [] bs)
merge2 (x:xs) (b:bs) | (x < b) = (x : (merge2 xs (b:bs))) 
                     | otherwise  = (b : (merge2 (x:xs) bs))

--merge2Tail
myRev :: [a] -> [a] -> [a]
myRev [] acc = acc
myRev (x:xs) acc = myRev xs (x : acc)

merge2Tail :: Ord a => [a] -> [a] -> [a] -> [a]
merge2Tail accum [] [] = myRev accum []
merge2Tail accum [] (b:bs) = (merge2Tail (b:accum) [] bs)
merge2Tail accum (x:xs) [] = (merge2Tail (x:accum) xs [])
merge2Tail accum (x:xs) (b:bs) | (x < b) = (merge2Tail (x:accum) xs (b:bs))
                               | otherwise = merge2Tail (b:accum) (x:xs) bs

--mergeN


{- 2 - getInRange & countInRange - 18% -}

--getInRange


--countInRange 



{- 3 -  addLengths & addAllLengths - 18% -}

data LengthUnit =  INCH  Int | FOOT  Int | YARD  Int
                   deriving (Show, Read, Eq)
-- addLengths 

-- addAllLengths

{-4 - sumTree and createSumTree - 22%-}

data Tree a = LEAF a | NODE a  (Tree a)  (Tree a) 
              deriving (Show, Read, Eq)
 
--sumTree


--createSumTree


{-5 - foldListTree - 20%-}
data ListTree a = ListLEAF [a] | ListNODE [(ListTree a)]
                  deriving (Show, Read, Eq)
 


{- 6- Create two tree values :  Tree Integer  and  listTree a ;  Both trees should have at least 3 levels. -}