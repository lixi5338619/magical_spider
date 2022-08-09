from demo.runflow import magical_start,magical_request,magical_close
import time

# 各任务间互不影响，可选择使用多线程或多进程，大家自由发挥

def r1():
    project_name1 = '药监局新闻任务1'
    s1,p1 = magical_start(project_name1,'https://www.nmpa.gov.cn')
    request_list = [
        'https://www.nmpa.gov.cn/xxgk/ggtg/index.html',
        'https://www.nmpa.gov.cn/xxgk/fgwj/index.html',
        'https://www.nmpa.gov.cn/xxgk/fgwj/index.html'
    ]
    for request_url in request_list:
        print("r1:", len(magical_request(s1, p1, request_url)))
        time.sleep(5)
    magical_close(s1,p1,project_name1)

def r2():
    project_name2 = '药监局新闻任务2'
    s2,p2 = magical_start(project_name2,'https://www.nmpa.gov.cn')
    request_list = ['https://www.nmpa.gov.cn/zwgk/rshxx/index.html',
                    'https://www.nmpa.gov.cn/zwgk/xwfb/index.html',
                    'https://www.nmpa.gov.cn/zwgk/xwfb/index.html'
                    ]
    for request_url in request_list:
        print("r2:", len(magical_request(s2, p2, request_url)))
        time.sleep(5)
    magical_close(s2,p2,project_name2)


import threading
thread1 = threading.Thread(target=r1)
thread2 = threading.Thread(target=r2)
thread1.start()
thread2.start()