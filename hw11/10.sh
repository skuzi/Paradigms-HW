echo Hello world > file.txt
git add file.txt
echo 'echo "Add Hello world" > $1' > rebase.sh
chmod 777 rebase.sh
GIT_EDITOR=./rebase.sh git commit --amend
