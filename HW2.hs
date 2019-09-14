merge2 :: Ord a => [a] -> [a] -> [a]
merge2 [] [] = []
merge2 (x:xs) [] = x : (merge2 xs [])
merge2 [] (b:bs) = b : (merge2 [] bs)
merge2 (x:xs) (b:bs) | (x < b) = (x : (merge2 xs (b:bs))) 
                     | otherwise  = (b : (merge2 (x:xs) bs))

myRev :: [a] -> [a] -> [a]
myRev [] acc = acc
myRev (x:xs) acc = myRev xs (x : acc)

merge2Tail :: Ord a => [a] -> [a] -> [a] -> [a]
merge2Tail accum [] [] = myRev accum []
merge2Tail accum [] (b:bs) = (merge2Tail (b:accum) [] bs)
merge2Tail accum (x:xs) [] = (merge2Tail (x:accum) xs [])
merge2Tail accum (x:xs) (b:bs) | (x < b) = (merge2Tail (x:accum) xs (b:bs))
                               | otherwise = merge2Tail (b:accum) (x:xs) bs
