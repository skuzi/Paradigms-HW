import Prelude hiding (lookup)

-- Implement a binary search tree (4 points)
-- 2 extra points for a balanced tree
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) 
                      deriving (Eq, Show)

-- “Ord k =>” requires, that the elements of type k are comparable
-- Takes a key and a tree and returns Just value if the given key is present,
-- otherwise returns Nothing
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Nil = Nothing
lookup key  (Node k v l r)
    |  key < k            = lookup key l
    |  key > k            = lookup key r
    |  key == k           = Just v

-- Takes a key, value and tree and returns a new tree with key/value pair inserted.
-- If the given key was already present, the value is updated in the new tree.
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Node k v Nil Nil
insert key value (Node k v l r) 
    |  key < k                  = Node k v (insert key value l) r
    |  key > k                  = Node k v l (insert key value r)
    |  key == k                 = Node k value l r

-- Returns a new tree without the given key
delete :: (Eq v, Ord k) => k -> BinaryTree k v -> BinaryTree k v
delete _ Nil = Nil
delete key (Node k v l r)
    |  key < k              = Node k v (delete key l) r
    |  key > k              = Node k v l (delete key r)
    |  otherwise            = merge l r

--Merges two trees such that all keys in the first tree are less then keys in the second.
merge :: Ord k => (BinaryTree k v) -> (BinaryTree k v) -> (BinaryTree k v)
merge Nil tree = tree
merge tree Nil = tree
merge (Node k1 v1 l1 r1) (Node k2 v2 l2 r2) = Node k1 v1 l1 (merge r1 (Node k2 v2 l2 r2))
