echo 'echo "pick bdca292 Add file.txt\nsquash 3cea379 Crap, I have forgotten to add this line." > $1' > rebase.sh
echo 'echo "Add file.txt\Crap, I have forgotten to add this line." > $1' >> rebase.sh
chmod 777 rebase.sh
GIT_EDITOR=./rebase.sh git rebase -i