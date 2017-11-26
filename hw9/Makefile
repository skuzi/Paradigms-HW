EXE = pthread

CFLAGS = -pthread -Wall -Wextra -Wnull-dereference -Werror -Iinclude


all : bin $(EXE)

bin:
	mkdir bin

$(EXE): ./bin/ThreadPool.o ./bin/main.o
	g++ -pthread -Iinclude ./bin/ThreadPool.o ./bin/main.o -o $(EXE)

./bin/ThreadPool.o: ./src/ThreadPool.cpp
	g++ -c $(CFLAGS) ./src/ThreadPool.cpp -o ./bin/ThreadPool.o

./bin/main.o: ./src/main.cpp
	g++ -c $(CFLAGS) ./src/main.cpp -o ./bin/main.o
clean:
	rm -rf bin $(EXE)

.PHONY: all clean