import os
import re
import json
from pick import pick


def append_validation(_user_input):
    list = _user_input.split('; ')
    output = []
    error_list = []
    for element in list:
        if re.match(r'(.+/(\d{1,3}\.){3}\d{1,3})', element):
            element = element.split('/')
            output.append({"ip_address": element[1], "name": element[0], "flag": True})
        else:
            error_list.append(element)
    if error_list:
        error = ', '.join(error_list)
        print(f'Incorrect input format for {error}\n'
              'Appropriate format is: name/ip_address; ...')
        input('<exit')
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
    os.system(clear)
    print(' Extend the list '.center(50, '-'))
    while True:
        user_input = input('Provide locomotives info to follow:\n')
        if user_input == 'q':
            break
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
    main()


def delete(follow_list):
    while True:
        os.system(clear)
        print(' Deleting '.center(50, '-'))
        if follow_list:
            error_objects = []
            index_list = []
            name_list = []
            for pos, item in enumerate(follow_list, start=1):
                print(f'{pos:<2} - {item["ip_address"]:>15} / {item["name"]}')
            user_input = input('Stop following:\n')

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
                        index_list.append(int(object)-1)
                    else:
                        name_list.append(object)
                if index_list:
                    index_list.sort(reverse=True)
                    for index in index_list:
                        follow_list.pop(index)
                    with open('list.JSON', 'w') as f:
                        f.write(json.dumps(follow_list, indent=2))
                if name_list:
                    for name in name_list:
                        present = False
                        for item in follow_list:
                            if item['name'] == name:
                                follow_list.remove(item)
                                present = True
                                with open('list.JSON', 'w') as f:
                                    f.write(json.dumps(follow_list, indent=2))
                        if not present:
                            error_objects.append(name)

                if error_objects:
                    error = ', '.join(error_objects)
                    print(f'error: Objects {error} not found')
                    choice = input('[c] to correct\t[q] to quit\n')
                    if choice == 'q':
                        break
                    elif choice == 'c':
                        delete(follow_list)
        else:
            print("You're not following anything")
            input('<exit')
            break
    main()


def get_label(option):
    return f'{option["ip_address"]:<15} / {option["name"]:6} - {option["flag"]}'


def show_list(follow_list):
    if follow_list:
        os.system(clear)
        selected = pick(follow_list, options_map_func=get_label, multiselect=True)
        for select in selected:
            select[0]['flag'] = not select[0]['flag']

        with open('list.JSON', 'w') as f:
            f.write(json.dumps(follow_list, indent=2))
    else:
        print("You're not following anything")
        input('<exit')
    main()


def set_frequency():
    os.system(clear)
    print('Set-frequency'.center(50, '-'))
    # config('FREQUENCY') = input('\n\nSet pinging frequency (in seconds):\n')


def main():
    follow_list = parse_list()
    os.system(clear)

    title = 'Lista akcji:'
    options = ['Add', 'Delete', 'Show the list', 'Ping frequency (coming soon)', 'Good bye!']
    option, index = pick(options, title, indicator='=>')
    match option:
        case 'Add':
            add_address(follow_list)
        case 'Delete':
            delete(follow_list)
        case 'Show the list':
            show_list(follow_list)
        case 'Ping frequency (coming soon)':
            main()
        case 'Do widzenia':
            exit()


if __name__ == '__main__':
    clear = 'clear'
    main()
