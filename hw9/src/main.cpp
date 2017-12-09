#include "ThreadPool.h" 
#include <cstdlib>
#include <ctime>
#include <utility>
#include <algorithm>
#include <iostream>

std::size_t MAX_DEPTH;

Task sort_tasks[100000];
std::size_t last_task;

int check(std::vector<int> &a) {
    for(std::size_t i = 0; i < a.size() - 1; i++) {
        if(a[i] > a[i + 1]) {
            return 1;
        }
    }
    return 0;
}

std::vector<int> a;

struct Query {
    std::size_t l, r;
    ThreadPool* th_pool;
    std::size_t depth;

    Query(ThreadPool* th_pool, std::size_t l = 0, std::size_t r = 0, std::size_t depth = 0)
        :l(l), r(r), depth(depth)
    {
        this->th_pool = th_pool;
    }

    Query(){}

    ~Query(){}
};

void partition(Query* s) {
    std::size_t i = s->l, j = s->r;
    if(i > j)
        return;

    int pivot = a[(i + j) / 2];
    while(i <= j) {
        while(a[i] < pivot)
            i++;
        while(a[j] > pivot)
            j--;
        if(i <= j) {
            std::swap(a[i], a[j]);
            i++;
            j--;
        }
    }
}

Query left[10000];
std::size_t last_left;
Query right[10000];
std::size_t last_right;

void qsort(void* q) {
    Query* s = (Query*) q;
    if(s->l > s->r)
        return;

    if(s->depth == MAX_DEPTH) {
        std::sort(a.begin() + s->l, a.begin() + s->r + 1);
        return;
    }

    partition(s);
    std::size_t m = (s->l + s->r) / 2;

    left[last_left++] = Query(s->th_pool, s->l, m, s->depth + 1);
    right[last_right++] = Query(s->th_pool, m + 1, s->r, s->depth + 1);

    sort_tasks[last_task++] = Task(qsort, &left[last_left - 1]);
    sort_tasks[last_task++] = Task(qsort, &right[last_right - 1]);

    s->th_pool->submit(&sort_tasks[last_task - 1]);
    s->th_pool->submit(&sort_tasks[last_task - 2]);
}

void foo(void *) {
    puts("HELLP");
}

void do_tasks(std::size_t thread_cnt) {
    ThreadPool pool(thread_cnt);

    Query s(&pool, 0, a.size() - 1);

    sort_tasks[last_task++] = Task(qsort, &s);
    
    pool.submit(sort_tasks);

    for(std::size_t i = 0; i < last_task; i++) {
        sort_tasks[i].wait();
    }
    /*std::vector<Task> s;
    for(int i = 0; i < 5; i++) {
        s.push_back(Task(foo, NULL));
    }
    for(int i = 0; i < 5; i++) {
        pool.submit(&s[i]);
    }*/
}

int main(int argc, char* argv[]) {
    if(argc != 4)
        return -1;
    srand(42);
    std::size_t size = atoi(argv[2]);
    MAX_DEPTH = atoi(argv[3]);
    a.resize(size);
    for(std::size_t i = 0; i < size; i++) {
        a[i] = rand();
    }

    std::time_t start_time = time(NULL);

    do_tasks(atoi(argv[1]));
    if(check(a)) {
        puts("FAIL");
        return 1;
    }

    std::time_t end_time = time(NULL);
    std::cout << (end_time - start_time) << '\n';
    puts("SUCCESS");
    return 0;
}