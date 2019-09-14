-- CptS 355 - Fall 2019 Assignment 1
-- Alex Puga 011425121

module HW1
     where

import Data.Char (toUpper)

-- 1. exists
-- Since we are comparing values, we use Eq t not t -> [t] -> Bool
exists :: Eq t => t -> [t] -> Bool
exists p [] = False 
-- checks to see if value is equal to p. if it is return true 
exists p (x:xs) = if (p == x) then True
                  else (exists p xs)

-- 2. listUnion
listUnion :: Eq a => [a] -> [a] -> [a]
listUnion [] [] = []
-- alternates the lists to keep checking if one or the other has a value that is inside the other list aswell within
--itelsf
listUnion (x:xs) [] = if (exists x xs) then listUnion xs [] else x : (listUnion xs [])
listUnion [] (b:bs) = if (exists b bs) then listUnion bs [] else b : (listUnion [] bs)
listUnion (x:xs) as =  if ((exists x as) || (exists x xs) ) == True then listUnion as xs else x : (listUnion as xs) 
          
          

-- 3. replace
replace :: (Eq t1, Num t1) => t1 -> t2 -> [t2] -> [t2]
replace n xs [] = []
-- reduces n until it hits 0 and replaces the value
replace n xs (b:bs) = if (n == 0) then xs : bs
                      else (b : (replace (n - 1) xs bs))

-- Sample tests
prereqsListTest =
     [ ("CptS122" , ["CptS121"]),
     ("CptS132" , ["CptS131"]),
     ("CptS223" , ["CptS122", "MATH216"]),
     ("CptS233" , ["CptS132", "MATH216"]),
     ("CptS260" , ["CptS223", "CptS233"]),
     ("CptS315" , ["CptS223", "CptS233"]),
     ("CptS317" , ["CptS122", "CptS132", "MATH216"]),
     ("CptS321" , ["CptS223", "CptS233"]),
     ("CptS322" , ["CptS223","CptS233"]),
     ("CptS350" , ["CptS223","CptS233", "CptS317"]),
     ("CptS355" , ["CptS223"]),
     ("CptS360" , ["CptS223","CptS260"]),
     ("CptS370" , ["CptS233","CptS260"]),
     ("CptS427" , ["CptS223","CptS360", "CptS370", "MATH216", "EE234"])]

-- 4. prereqFor
prereqFor :: Eq t => [(a, [t])] -> t -> [a]
prereqFor [] str = []
-- Checks if str exists within the children list. if it does, then it adds the parent to the list
prereqFor ((p,ch):xs) str = if (exists str ch) == True then (p : prereqFor xs str) else (prereqFor xs str) 


-- 5. isPalindrome
isPalindrome :: [Char] -> Bool
isPalindrome [] = False;
-- makes a copy of the input and reverses it
-- created a helper that takes in two strings (one is the reverse of the other)
isPalindrome xs = let bs = reverse xs
                  in isPalindromeHelper xs bs
     where isPalindromeHelper [] [] = True
           isPalindromeHelper xs [] = False
           isPalindromeHelper [] bs = False
           isPalindromeHelper (x:xs) (b:bs) 
                                   -- | x /= b = False
                                   | (toUpper x == toUpper b) = (isPalindromeHelper xs bs)
                                   --it ignores white spaces
                                   | (x == ' ') = (isPalindromeHelper xs (b:bs))
                                   | (b == ' ') = (isPalindromeHelper (x:xs) bs)

-- 6. groupSumtoN
groupSumtoN :: (Ord a, Num a) => a -> [a] -> [[a]]
groupSumtoN n [] = []
groupSumtoN n iL = (helperToSum n iL [])
-- created a helper function that takes in an additional array as the output
-- reverses the last output so its in order
     where helperToSum n [] acc = [reverse(acc)]
          -- checks to see wether the sum is less than to add to the grouped array
           helperToSum n (x:xs) acc | (sum acc) + x <= n = (helperToSum n xs (x:acc))
                                    | (sum acc) + x > n = reverse(acc):(helperToSum n xs [x])




