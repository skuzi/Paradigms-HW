--useful operator
(++) [] ys = ys
(++) (x : xs) ys = x : (xs ++ ys)
--1. Head
head (x : xs) = x
--2. Tail
tail []  = []
tail (x : xs) = xs
--3. Take
take 0 xs = []
take n [] = []
take n (x : xs) = [x] ++ take (n-1) xs
--4. Drop
drop 0 xs = xs
drop n [] = []
drop n (x : xs) = drop (n-1) xs
--5. Filter
filter f [] = []
filter f (x : xs) = if(f(x)) then [x] ++ filter f xs else filter f xs
--6. Foldl
foldl _ z [] = z
foldl f z (x : xs) = foldl f (f z x) xs
--7. Concat
concat xs ys = xs ++ ys
--8. QuickSort
quicksort [] = []
quicksort (x:xs) = quicksort [a | a<-xs, a <= x] ++ [x] ++ quicksort [a | a<-xs, a > x]
