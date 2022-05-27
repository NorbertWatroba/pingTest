from pythonping import ping
import time
import json
from concurrent.futures import ThreadPoolExecutor
import smtplib
import ssl
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def waiting():
    time.sleep(3600)
    global stop_threads
    stop_threads = True


def ping_custom(follow_list):
    for item in follow_list:
        response = ping(item['ip_address'], verbose=False)
        print(response.packets_lost)
        while True:
            if response.packets_lost == 0.0:
                send_mail(item['name'], item['ip_address'])
                break
            elif response.packets_lost == 1.0:
                break
    global stop_threads
    stop_threads = True


def send_mail(name, ip):
    port = 465
    host = config('EMAIL_HOST')
    password = config('PASSWORD')
    recipient = config('RECIPIENT')
    message = MIMEMultipart('alternative')
    message['Subject'] = f'New locomotive active'
    message['From'] = host
    message['TO'] = recipient
    text = f"""
    Hi!
    I'd like to inform you that {name} with address {ip} is now available!
    """
    html = f"""
<h1>Hi!</h1>
<p style="font-size:14px">I'd like to inform you that <span style="color:darkred">{name}</span> with address <span style="color:darkblue">{ip}</span> is now available!</p>"""
    plain_text = MIMEText(text, 'text')
    html_content = MIMEText(html, 'html')

    message.attach(plain_text)
    message.attach(html_content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(host, password)
        server.sendmail(host, recipient, message.as_string())


def animated_slash(speed: float):
    animation_sequence = r"|/-\\"
    idx = 0
    while True:
        global stop_threads
        print(animation_sequence[idx % len(animation_sequence)], end="\r")
        idx += 1
        time.sleep(speed)

        if idx == len(animation_sequence):
            idx = 0

        if stop_threads:
            stop_threads = False
            break


while True:
    stop_threads = False
    try:
        with open('list.JSON', 'r') as f:
            json_data = json.load(f)
            follow_list = [json_dict for json_dict in json_data]
    except json.decoder.JSONDecodeError:
        follow_list = []

    run_io_tasks_in_parallel([
        lambda: ping_custom(follow_list),
        lambda: animated_slash(0.1),
    ])

    run_io_tasks_in_parallel([
        lambda: waiting(),
        lambda: animated_slash(0.5)
    ])
