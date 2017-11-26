#pragma once
#include <pthread.h>
#include <queue>
#include <vector>


struct Task {
	void wait();
    void (*m_func) (void* arg);
    void* m_arg;
    bool m_stop;
    pthread_mutex_t m_mutex;
    pthread_cond_t m_cond;
};

struct ThreadPool {

	ThreadPool(std::size_t threads_count);
	~ThreadPool();
	void submit(Task* task);
	bool m_stop;
	std::vector<pthread_t> m_threads;
	std::queue<Task*> m_tasks;
	std::vector<Task*> m_busy_tasks;
	pthread_mutex_t m_mutex;
	pthread_cond_t m_cond;
};