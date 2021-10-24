# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:16:02 2021

@author: 94337
"""

import threading
import time
import numpy as np

g_Input = np.array([1.,2.,3.])
g_Output = 0
g_Sem = threading.Semaphore()
Thread_A_Run = True
Thread_B_Run = True

def Thread_A():
    global g_Input
    global g_Output
    global Thread_A_Run
    while Thread_A_Run:
        g_Output = sum(g_Input)
        print('A: g_Output = %g' % g_Output)
        print('is_alive() = %d'%Threads[1].is_alive())
        print('main=%s=%d, curr=%s=%d'%(threading.main_thread().name, threading.main_thread().ident, threading.currentThread().name, threading.currentThread().ident))
        
        g_Sem.acquire()
    

def Thread_B():
    global g_Input
    global g_Output
    global Thread_A_Run, Thread_B_Run
    global Threads
    i = 0
    g_Input = np.array([1.,2.,3.])
    while Thread_B_Run:
        i += 1
        time.sleep(0.2)
        if i > 10:
            i = 0
            g_Input += 1/3
            g_Sem.release()
        print('B: g_Output = %g' % g_Output)
        if g_Output > 20:
            Thread_A_Run = False
            Thread_B_Run = False
            break
    g_Sem.release()
        
Threads = list()
Threads.append(threading.Thread(target = Thread_A, name = 'A'))
Threads.append(threading.Thread(target = Thread_B, name = 'B'))

for thread in Threads:
    thread.setDaemon(True)
    thread.start()
print('START!!!!')
print('main=%s=%d, curr=%s=%d'%(threading.main_thread().name, threading.main_thread().ident, threading.currentThread().name, threading.currentThread().ident))
try:
    while True:
        time.sleep(0.01)
        if g_Output > 10:
            Thread_A_Run = False
            Thread_B_Run = False
            break
    print('try END!!!!')
    
    for thread in Threads:
        thread.join()
        
    print('done END!!!!')
except:
    Thread_A_Run = False
    Thread_B_Run = False
    print('yxs!!!!!!!!!!!!!!!!!!!!!!!!!!')

        

