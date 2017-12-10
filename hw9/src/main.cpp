#include "ThreadPool.h" 
#include <cstdlib>
#include <ctime>
#include <utility>
#include <algorithm>
#include <iostream>
#include <atomic>

std::size_t MAX_DEPTH;

Task sort_tasks[1000000];
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

    Query(){
        th_pool = NULL;
        l = 0;
        r = 0;
    }

    ~Query(){}
};

Query left[1000000];
std::size_t last_left;
Query right[1000000];
std::size_t last_right;

void qsort(void* q) {
    Query* s = (Query*) q;
    if(s->l > s->r)
        return;

    if(s->depth == MAX_DEPTH) {
        std::sort(a.begin() + s->l, a.begin() + s->r + 1);
        return;
    }

    pthread_mutex_t mut1;
    pthread_mutex_init(&mut1, NULL);
    pthread_mutex_lock(&mut1);
    std::size_t i = s->l, j = s->r;
    //std::cout << i << ' ' << j << '\n';
    int pivot = a[(i + j + 1) / 2];
    //std::cout << "pivot is: " << pivot << '\n';
    while(i <= j) {
        while(a[i] < pivot) {
            //std::cout << "i is: " << i << '\n';
            ++i;
        }
        while(a[j] > pivot){
            //std::cout << "j is: " << j << '\n';
            --j;
        }
        if(i <= j) {
            /*puts("before: ");
            for(int t = 0; t < a.size(); t++)
                std::cout << a[t] << ' ';*/
            //puts("\n");
            std::swap(a[i], a[j]);
            ++i;
            --j;
            /*puts("after: ");
            for(int t = 0; t < a.size(); t++)
                std::cout << a[t] << ' ';
            std::cout << '\n';*/
        }
    }
    pthread_mutex_unlock(&mut1);
    pthread_mutex_destroy(&mut1);
    std::size_t m = (s->l + s->r + 1) / 2;

    pthread_mutex_t mut;
    pthread_mutex_init(&mut, NULL);
    pthread_mutex_lock(&mut);
    left[last_left++] = Query(s->th_pool, s->l, j, s->depth + 1);
    right[last_right++] = Query(s->th_pool, i, s->r, s->depth + 1);

    sort_tasks[last_task++] = Task(qsort, &left[last_left - 1]);
    sort_tasks[last_task++] = Task(qsort, &right[last_right - 1]);
    pthread_mutex_unlock(&mut);
    pthread_mutex_destroy(&mut);

    s->th_pool->submit(&sort_tasks[last_task - 1]);
    s->th_pool->submit(&sort_tasks[last_task - 2]);
}

void do_tasks(std::size_t thread_cnt) {
    std::time_t start_time = time(NULL);
    ThreadPool pool(thread_cnt);

    Query s(&pool, 0, a.size() - 1);

    sort_tasks[last_task++] = Task(qsort, &s);
    
    pool.submit(sort_tasks);

    for(std::size_t i = 0; i < last_task; i++) {
        sort_tasks[i].wait();
    }
    std::time_t end_time = time(NULL);
    std::cout << (end_time - start_time) << '\n';
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


    do_tasks(atoi(argv[1]));
    if(check(a)) {
        puts("FAIL");
        return 1;
    }

    puts("SUCCESS");
    return 0;
}