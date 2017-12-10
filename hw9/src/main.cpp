#include "ThreadPool.h" 
#include <cstdlib>
#include <ctime>
#include <utility>
#include <list>
#include <algorithm>
#include <iostream>
#include <atomic>

std::size_t MAX_DEPTH;

std::list<Task> sort_tasks;

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

std::list<Query> left, right;


pthread_mutex_t mut;
void qsort(void* q) {
    Query* s = (Query*) q;
    if(s->l >= s->r)
        return;
    if(s->depth == MAX_DEPTH) {
        std::sort(a.begin() + s->l, a.begin() + s->r + 1);
        return;
    }
    pthread_mutex_lock(&mut);

    int pivot = a[(s->l + s->r + 1) / 2];
    auto it1 = std::partition(a.begin() + s->l, a.begin() + s->r + 1, [pivot](int i){ return i < pivot; });
    auto it2 = std::partition(it1, a.begin() + s->r + 1, [pivot](int i){ return i <= pivot; });
    
    left.push_back(Query(s->th_pool, s->l, it1 - a.begin() - 1, s->depth + 1));
    right.push_back(Query(s->th_pool, it2 - a.begin(), s->r, s->depth + 1));
    sort_tasks.push_back(Task(qsort, &left.back()));
    Task& last1 = sort_tasks.back();
    sort_tasks.push_back(Task(qsort, &right.back()));
    Task& last2 = sort_tasks.back();

    pthread_mutex_unlock(&mut);

    s->th_pool->submit(&last1);
    s->th_pool->submit(&last2);

}

void do_tasks(std::size_t thread_cnt) {
    std::time_t start_time = time(NULL);
    ThreadPool pool(thread_cnt);

    Query s(&pool, 0, a.size() - 1);

    sort_tasks.push_back(Task(qsort, &s));
    
    pool.submit(&sort_tasks.back());

    while(!sort_tasks.empty()) {
        sort_tasks.front().wait();
        sort_tasks.pop_front();
    }
    
    if(check(a))
        puts("FAIL");
    else
        puts("SUCCESS");
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

    pthread_mutex_init(&mut, NULL);

    do_tasks(atoi(argv[1]));

    pthread_mutex_destroy(&mut);    
    return 0;
}