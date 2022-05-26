import os
import re
import json
from pick import pick


def append_list_validation(string):
    list = string.split(';')
    output = []
    for e in list:
        element = e.strip().split('/')
        if element != ['']:
            output.append({"ip_address": element[0], "name": element[1]})
    return output


def append_single_validation(string):
    element = string.split('/')
    output = {"ip_address": element[0], "name": element[1]}
    return output


try:
    with open('list.JSON', 'r') as f:
        json_data = json.load(f)
        follow_list = [json_dict for json_dict in json_data]
except json.decoder.JSONDecodeError:
    follow_list = []

operation_list = ['Dodaj', 'Usuń', 'Pokaż listę']

os.system('clear')

print('Witaj'.center(50, '-'))

while True:
    title = 'Witaj'
    options = ['Dodaj', 'Usuń', 'Pokaż listę']
    option, index = pick(options, title)
    match option:
        case 'Dodaj':
            print('Podaj adresy do monitorowania:')
            while True:
                string = input('')
                if string == 'q':
                    os.system('clear')
                    break
                if re.match(r'((\d{1,3}\.){1,3}\d{1,3}/.+;\s)+', string):
                    ex = append_list_validation(string)
                    for i in ex[::-1]:
                        for item in follow_list:
                            if i['name'] == item['name']:
                                item['ip_address'] = i['ip_address']
                                ex.remove(i)
                    follow_list.extend(ex)
                    with open('list.JSON', 'w') as f:
                        f.write(json.dumps(follow_list, indent=2))
                    os.system('clear')
                    break
                elif re.match(r'(\d{1,3}\.){1,3}\d{1,3}/.+', string):
                    ex = (append_single_validation(string))
                    for item in follow_list:
                        if item['name'] == ex['name']:
                            item['ip_address'] = ex['ip_address']
                            os.system('clear')
                            break

                    with open('list.JSON', 'w') as f:
                        f.write(json.dumps(follow_list, indent=2))
                    os.system('clear')
                    break
                else:
                    print('Prawidłowy format to: adres_ip/nazwa; ...')

        case 'Usuń':
            while True:
                if follow_list:
                    for pos, i in enumerate(follow_list, start=1):
                        print(f'{pos:<3} - {i["ip_address"]:>15} / {i["name"]}')
                    print('Przestań monitorować:')
                    string = input('')
                    if string == 'q':
                        os.system('clear')
                        break
                    objects = string.split('; ')
                    for o in objects:
                        present = False
                        if o == 'all':
                            follow_list.clear()
                            os.system('clear')
                            break
                        else:

                            for i in follow_list:
                                if i['name'] == o:
                                    follow_list.remove(i)
                                    present = True
                                    with open('list.JSON', 'w') as f:
                                        f.write(json.dumps(follow_list, indent=2))
                        if not present:
                            print(f'{o} nie istnieje')
                    os.system('clear')
                    break
                else:
                    print('Nie monitorujesz żadnych pojazdów')
                    os.system('clear')
                    break

        case 'Pokaż listę':

            if follow_list:
                for pos, i in enumerate(follow_list, start=1):
                    print(f'{pos} - {i["ip_address"]:>15} / {i["name"]}')
            else:
                print('Lista jest pusta')
