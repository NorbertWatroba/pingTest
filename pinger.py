from pythonping import ping
import time
import json
from concurrent.futures import ThreadPoolExecutor


def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def ping_custom(follow_list):
    for item in follow_list:
        ping(item['ip_address'], verbose=True)


def waiter():
    animation_sequence = r"|/-\\"
    idx = 0
    while True:
        print(animation_sequence[idx % len(animation_sequence)], end="\r")
        idx += 1
        time.sleep(0.1)

        if idx == len(animation_sequence):
            idx = 0


while True:
    with open('list.JSON', 'r') as f:
        json_data = json.load(f)
        follow_list = [json_dict for json_dict in json_data]
        run_io_tasks_in_parallel([
            lambda: ping_custom(follow_list),
            lambda: waiter(),
        ])

    time.sleep(7)
