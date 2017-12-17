git stash
sed -i '4d' bug.txt
git commit -am "bugfix"
git stash pop
echo Finally, finished it! >> bug.txt
git commit -am "finish"