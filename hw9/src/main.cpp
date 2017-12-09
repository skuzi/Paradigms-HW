#include "ThreadPool.h" 
#include <cstdlib>
#include <ctime>
#include <utility>
#include <algorithm>
#include <iostream>

std::size_t MAX_DEPTH;

std::vector<Task> sort_tasks;

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

    Query(std::size_t l, std::size_t r, ThreadPool* th_pool, std::size_t depth = 0)
        :l(l), r(r), depth(depth)
    {
        this->th_pool = th_pool;
    }

    ~Query(){}
};

void partition(void* q) {
    Query* s = (Query*) q;

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

void qsort(void* q) {
    Query* s = (Query*) q;
    if(s->l > s->r)
        return;

    if(s->depth == MAX_DEPTH) {
        std::sort(a.begin() + s->l, a.begin() + s->r + 1);
        return;
    }

    Task partition_task(partition, q);
    sort_tasks.push_back(partition_task);

    s->th_pool->submit(&partition_task);
    std::size_t m = (s->l + s->r) / 2;

    Query left(s->l, m, s->th_pool, s->depth + 1);
    Query right(m + 1, s->r, s->th_pool, s->depth + 1);

    Task sort_left(qsort, &left);
    Task sort_right(qsort, &right);

    sort_tasks.push_back(sort_left);
    sort_tasks.push_back(sort_right);

    s->th_pool->submit(&sort_left);
    s->th_pool->submit(&sort_right);
}

void do_tasks(std::size_t thread_cnt) {
    ThreadPool pool(thread_cnt);

    Query s(0, a.size() - 1, &pool);

    Task sort_all(qsort, &s);
    sort_tasks.push_back(sort_all);
    
    pool.submit(&sort_all);

    for(std::size_t i = 0; i < sort_tasks.size(); i++) {
        sort_tasks[i].wait();
    }
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