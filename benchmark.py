import requests
import random
import numpy as np
import timeit
import time
import re
import threading
from threading import Thread, Lock
from statistics import mean

t = 0.8 # Durchschnittliche Wartezeit
t_new = random.uniform(t * 0.8, t * 1.2)

n = 100 # Anzahl Terminals 

url_param = ["/query4_table", "/query1_chart", "/query1_table", "/query2_table", "/query5_table", "/query6_win", "/query6_loser", 
                "/query3_wahlbeteiligung/5", "/query3_direktkandidaten/5", "/query3_stimmen_entwicklung/5"]

base_path = "http://127.0.0.1:8000"

""" workload_mix = {
    "/query4_table": 0.1,
    "/query1_chart": 0.125,
    "/query1_table": 0.125,
    "/query2_table": 0.1,
    "/query5_table": 0.1, 
    "/query6_win": 0.1, 
    "/query6_loser": 0.1,
    "/query3_wahlbeteiligung/": 0.083, 
    "/query3_direktkandidaten/": 0.083, 
    "/query3_stimmen_entwicklung/": 0.083
} """


# elem = np.random.choice(url_param, p=[0.1, 0.125, 0.125, 0.1, 0.1, 0.1, 0.1, 0.083, 0.083, 0.084])

times_q1 = []
times_q2 = []
times_q3 = []
times_q4 = []
times_q5 = []
times_q6 = []

reg_q1 = "query1"
reg_q2 = "query2"
reg_q3 = "query3"
reg_q4 = "query4"
reg_q5 = "query5"
reg_q6 = "query6"

lock1 = Lock()
lock2 = Lock()
lock3 = Lock()
lock4 = Lock()
lock5 = Lock()
lock6 = Lock()

def start_function():
    for i in range(0, 500):
        choice = np.random.choice(url_param, p=[0.1, 0.125, 0.125, 0.1, 0.1, 0.1, 0.1, 0.083, 0.083, 0.084])
        start_time = timeit.default_timer()
        r = requests.get(base_path + choice)
        end_time = timeit.default_timer()
        if(re.search(reg_q1, choice)):
            with lock1:
                times_q1.append(end_time - start_time)
        elif(re.search(reg_q2, choice)):
            with lock2:
                times_q2.append(end_time - start_time)
        elif(re.search(reg_q3, choice)):
            with lock3:
                times_q3.append(end_time - start_time)
        elif(re.search(reg_q4, choice)):
            with lock4:
                times_q4.append(end_time - start_time)
        elif(re.search(reg_q5, choice)):
            with lock5:
                times_q5.append(end_time - start_time)
        elif(re.search(reg_q6, choice)):
            with lock6:
                times_q6.append(end_time - start_time)
        time.sleep(t_new)
    
def main():
    list_threads = []
    for i in range(0, n):
        t = Thread(target = start_function)
        list_threads.append(t)
        t.start()
    for i in list_threads:
        i.join()
    print(mean(times_q1))
    print(mean(times_q2))
    print(mean(times_q3))
    print(mean(times_q4))
    print(mean(times_q5))
    print(mean(times_q6))
    





if __name__ == "__main__":
    main()