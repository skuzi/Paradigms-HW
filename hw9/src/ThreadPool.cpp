#include "ThreadPool.h"
#include <iostream>

void Task::wait() {
    pthread_mutex_lock(&m_mutex);

    while(!m_stop) {
        pthread_cond_wait(&m_cond, &m_mutex);
    }

    pthread_mutex_unlock(&m_mutex);
}

void* thread_action(void* pool) {
    ThreadPool* th_pool = (ThreadPool*) pool;
    while (1) {
        pthread_mutex_lock(&th_pool->m_mutex);
        while (th_pool->m_tasks.empty() && !th_pool->m_stop) {
            pthread_cond_wait(&th_pool->m_cond, &th_pool->m_mutex);
        }

        if (th_pool->m_tasks.empty()) {
            pthread_mutex_unlock(&th_pool->m_mutex);
            break;
        }
        else {
            Task* task = th_pool->m_tasks.front();

            th_pool->m_tasks.pop();
            pthread_mutex_unlock(&th_pool->m_mutex);

            task->m_func(task->m_arg);

            pthread_mutex_lock(&task->m_mutex);

            task->m_stop = 1;
            pthread_cond_broadcast(&task->m_cond);

            pthread_mutex_unlock(&task->m_mutex);
        }
    }

    return NULL;
}

ThreadPool::ThreadPool(std::size_t threads_count) {
    pthread_mutex_init(&m_mutex, NULL);
    pthread_cond_init(&m_cond, NULL);
    m_stop = 0;

    m_threads.resize(threads_count);
    for(std::size_t i = 0; i < threads_count; i++) {
        pthread_create(&m_threads[i], NULL, thread_action, this);
    }
}

ThreadPool::~ThreadPool() {
    pthread_mutex_lock(&m_mutex);
    m_stop = 1;
    pthread_cond_broadcast(&m_cond);
    pthread_mutex_unlock(&m_mutex);

    for (std::size_t i = 0; i < m_threads.size(); i++) {
        pthread_join(m_threads[i], NULL);
    }
    pthread_cond_destroy(&m_cond);
    pthread_mutex_destroy(&m_mutex);
}

void ThreadPool::submit(Task* task) {
    pthread_mutex_lock(&m_mutex);
    m_tasks.push(task);
    pthread_cond_signal(&m_cond); 
    pthread_mutex_unlock(&m_mutex); 
}

Task::Task(void (*func) (void*), void* arg) {
    pthread_mutex_init(&m_mutex, NULL);
    m_stop = 0;
    m_func = func;
    m_arg = arg;
    pthread_cond_init(&m_cond, NULL);
}

Task::Task() {
    pthread_mutex_init(&m_mutex, NULL);
    m_stop = 0;
    m_func = NULL;
    m_arg = NULL;
    pthread_cond_init(&m_cond, NULL);
}

Task::~Task() {
    pthread_mutex_destroy(&m_mutex);
    pthread_cond_destroy(&m_cond);
}