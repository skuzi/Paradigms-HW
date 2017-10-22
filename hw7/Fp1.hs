--1. Head
head' (x:_) = x
--2. Tail
tail' []  = []
tail' (_:xs) = xs
--3. Take
take' 0 xs = []
take' n [] = []
take' n (x:xs) = x:take (n-1) xs
--4. Drop
drop' 0 xs = xs
drop' _ [] = []
drop' n (x:xs) = drop (n-1) xs
--5. Filter
filter' f [] = []
filter' f (x : xs) = if(f(x)) then x:filter f xs else filter f xs
--6. Foldl
foldl' _ z [] = z
foldl' f z (x : xs) = foldl f (f z x) xs
--7. Concat
concat' [] ys = ys
concat' (x:xs) ys = x:concat' xs ys
--8. QuickSort
smaller' _ [] = []
smaller' key (x:xs) = if(x <= key) then x:smaller' key xs else smaller' key xs
greater' _ [] = []
greater' key (x:xs) = if(x > key) then x:greater' key xs else greater' key xs
quicksort' [] = []
quicksort' (x:xs) = (quicksort' (smaller' x xs)) `concat'` (x:(quicksort' (greater' x xs)))
--8'. QuicSort v2
quicksort'' [] = []
quicksort'' (x:xs) = (quicksort'' (smaller'' x xs)) `concat'` (x:(quicksort'' (greater'' x xs)))
					where 
						smaller'' _ [] = []
						smaller'' key (x:xs) = if(x <= key) then x:smaller'' key xs else smaller'' key xs
						greater'' _ [] = []
						greater'' key (x:xs) = if(x > key) then x:greater'' key xs else greater'' key xs
