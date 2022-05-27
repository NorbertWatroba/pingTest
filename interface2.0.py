import os
from pick import pick
import re
from loco import Loco


def validation(user_input):
    list = user_input.split(';')
    output = []
    for object in list:
        object = object.strip().split('/')
        if object != ['']:
            output.append(exec(f'{object[0]} = Loco({object[1]},{object[0]})'))
    return output


def add_loco(follow_list):
    os.system('clear')
    print('Adding'.center(50, '-'))
    while True:
        user_input = input('Add new locomotive to monitor:\n')
        if user_input == 'q':
            break
        elif re.match(r'(.+/(\d{1,3}\.){3}\d{1,3})+', user_input):
            extension = validation(user_input)
            for ex_item in extension[::-1]:
                for item in follow_list:
                    if ex_item['name'] == item['name']:
                        item['ip_address'] = ex_item['ip_address']
                        item['flag'] = True
                        extension.remove(ex_item)
            follow_list.extend(extension)
            break
        else:
            print('error: proper format - name/ip_address; ... (q to quit)')
    main()


def main():
    os.system('clear')

    title = 'Lista akcji:'
    options = ['Dodaj', 'Usuń', 'Pokaż listę', 'Do widzenia']
    option, index = pick(options, title)
    match option:
        case 'Dodaj':
            add_loco(follow_list)
        case 'Usuń':
            pass
        case 'Pokaż listę':
            os.system('clear')
            print('Lista'.center(50, '-'))
            if follow_list:
                for pos, item in enumerate(follow_list, start=1):
                    print(f'{pos:<2} - {str(item)}')
            else:
                print('Lista jest pusta')
            input('<exit')
            main()
        case 'Do widzenia':
            exit()


if __name__ == '__main__':
    follow_list = []
    main()
