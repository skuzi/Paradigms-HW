#include "ThreadPool.h" 
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <iostream>


int check(std::vector<int> &a) {
	for(std::size_t i = 0; i < a.size() - 1; i++) {
		if(a[i] > a[i + 1]) {
			return 1;
		}
	}
	return 0;
}

int do_tasks(std::size_t thread_cnt, std::vector<int> &a) {
	ThreadPool pool(thread_cnt);
	//TODO
	return check(a);
}

int main(int argc, char* argv[]) {
	if(argc != 4)
		return -1;
    srand(42);
	std::size_t size = atoi(argv[2]);
	std::vector<int> a(size);
	for(std::size_t i = 0; i < size; i++) {
    	a[i] = rand();
    }

    std::time_t start_time = time(NULL);

    if(do_tasks(atoi(argv[1]), a)) {

    	return -1;
    }

    std::time_t end_time = time(NULL);
    std::cout << (end_time - start_time);
    return 0;
}