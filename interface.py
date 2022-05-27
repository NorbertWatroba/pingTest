import os
import re
import json
from pick import pick


def append_validation(_user_input):
    list = _user_input.split(';')
    output = []
    for element in list:
        element = element.strip().split('/')
        if element != ['']:
            output.append({"ip_address": element[0], "name": element[1], "flag": True})
    return output


def parse_list():
    if not os.path.exists('list.JSON'):
        open('list.JSON', 'x').close()
    try:
        with open('list.JSON', 'r') as f:
            json_data = json.load(f)
            follow_list = [json_dict for json_dict in json_data]
    except json.decoder.JSONDecodeError:
        follow_list = []
    return follow_list


def add_address(follow_list):
    os.system('clear')
    print('Dodawanie'.center(50, '-'))
    while True:
        user_input = input('Podaj adresy do monitorowania:\n')
        if user_input == 'q':
            break
        elif re.match(r'((\d{1,3}\.){1,3}\d{1,3}/.+)', user_input):
            extension = append_validation(user_input)
            for ex_item in extension[::-1]:
                for item in follow_list:
                    if ex_item['name'] == item['name']:
                        item['ip_address'] = ex_item['ip_address']
                        extension.remove(ex_item)
            follow_list.extend(extension)
            with open('list.JSON', 'w') as f:
                f.write(json.dumps(follow_list, indent=2))
            break
        else:
            print('Prawidłowy format to: adres_ip/nazwa; ... (q to quit)')
    main()


def delete(follow_list):
    while True:
        os.system('clear')
        print('Usuwanie'.center(50, '-'))
        if follow_list:
            error_objects = []
            for pos, item in enumerate(follow_list, start=1):
                print(f'{pos:<2} - {item["ip_address"]:>15} / {item["name"]}')
            user_input = input('Przestań monitorować:\n')

            if user_input == 'q':
                break

            elif user_input == 'all':
                follow_list.clear()
                with open('list.JSON', 'w') as f:
                    f.write(json.dumps(follow_list, indent=2))
                break

            else:
                objects = user_input.split('; ')
                for object in objects:
                    if re.match(r'^\d+$', object):
                        if int(object) > len(follow_list):
                            print(f'index {object} does not exist\n')
                            choice = input('[c] to correct\t[q] to quit\n')
                            if choice == 'q':
                                break
                            elif choice == 'c':
                                delete(follow_list)
                        else:
                            follow_list.pop(int(object) - 1)
                            with open('list.JSON', 'w') as f:
                                f.write(json.dumps(follow_list, indent=2))

                    else:
                        present = False
                        for item in follow_list:
                            if item['name'] == object:
                                follow_list.remove(item)
                                present = True
                                with open('list.JSON', 'w') as f:
                                    f.write(json.dumps(follow_list, indent=2))
                        if not present:
                            error_objects.append(object)

                if error_objects:
                    error = ', '.join(error_objects)
                    print(f'error: Objects {error} not found')
                    choice = input('[c] to correct\t[q] to quit\n')
                    if choice == 'q':
                        break
                    elif choice == 'c':
                        delete(follow_list)
        else:
            print('Nie monitorujesz żadnych pojazdów')
            input('<exit')
            break
    main()


def main():
    follow_list = parse_list()
    os.system('clear')

    title = 'Lista akcji:'
    options = ['Dodaj', 'Usuń', 'Pokaż listę', 'Do widzenia']
    option, index = pick(options, title)
    match option:
        case 'Dodaj':
            add_address(follow_list)
        case 'Usuń':
            delete(follow_list)
        case 'Pokaż listę':
            os.system('clear')
            print('Lista'.center(50, '-'))
            if follow_list:
                for pos, item in enumerate(follow_list, start=1):
                    print(f'{pos:<2} - {item["ip_address"]:>15} / {item["name"]}')
            else:
                print('Lista jest pusta')
            input('<exit')
            main()
        case 'Do widzenia':
            exit()


if __name__ == '__main__':
    main()
