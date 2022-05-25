import os
import re
import json


def append_list_validation(string):
    list = string.split(', ')
    output = []
    for e in list:
        element = e.split('/')
        output.append({"ip_address": element[0], "name": element[1]})
    return output


def append_single_validation(string):
    element = string.split('/')
    output = {"ip_address": element[0], "name": element[1]}
    return output


with open('list.JSON', 'r') as f:
    json_data = json.load(f)
    follow_list = [json_dict for json_dict in json_data]

operation_list = ['Dodaj', 'Usuń', 'Pokaż listę']

# os.system('cls')

print('Witaj'.center(200, '-'))

for i in range(len(operation_list)):
    print(f'{i+1} - {operation_list[i]}')
while True:
    choice = input('Wybór:\t')
    match choice:
        case '1':
            print('Podaj adresy do monitorowania:')
            while True:
                string = input('')
                if re.match(r'((\d{1,3}\.){1,3}\d{1,3}/.+,\s)+', string):
                    follow_list.extend(append_list_validation(string))
                    with open('list.JSON', 'w') as f:
                        f.write(json.dumps(follow_list, indent=2))
                    break
                elif re.match(r'(\d{1,3}\.){1,3}\d{1,3}/.+', string):
                    follow_list.append(append_single_validation(string))
                    with open('list.JSON', 'w') as f:
                        f.write(json.dumps(follow_list, indent=2))
                    break
                else:
                    print('Prawidłowy format to: adres_ip/nazwa, ...')

        case '2':
            print('Przestań monitorować:')
            while True:
                string = input('')
                objects = string.split(', ')
                for o in objects:
                    for i in follow_list:
                        if i['name'] == o:
                            follow_list.remove(i)
                            with open('list.JSON', 'w') as f:
                                f.write(json.dumps(follow_list, indent=2))
                break

        case '3':
            if follow_list:
                for pos, i in enumerate(follow_list, start=1):
                    print(f'{pos} - {i["ip_address"]:>15} / {i["name"]}')
            else:
                print('Lista jest pusta')
        case _:
            print('Wybierz z listy (1-3)')
