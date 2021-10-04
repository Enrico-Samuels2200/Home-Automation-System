import os
import json
import shutil
import general

json_file_name = 'app_list.json'

apps = {}
app_list = {}
remove_list = ['- shortcut.lnk', '.lnk']

# Create a json file contain a dictionary of applications names and their paths.
def write_data_file(data=''):
    with open('app_list.json', 'w') as doc:
        json.dump(data, doc)

# Reads the json file
def read_data_file():
    with open('app_list.json', 'r') as doc:
        return json.load(doc)

def update_path():
    operate_dir = r'C:\Users\admin\Desktop'
    for item in os.listdir(operate_dir):
            if item.lower().endswith('lnk'):
                try:
                    path = f'{operate_dir}\\{item}'

                    for i in remove_list:
                        if remove_list[0] in item.lower():
                            apps[item.lower().removesuffix(remove_list[0])] = path
                        else:
                            apps[item.lower().removesuffix(remove_list[1])] = path
                    

                except Exception as err:
                    print(err)

    general.write_json(json_file_name, apps)

def update_playlist():
    operate_dir = r'C:\Users\admin\Desktop\Media'
    for item in os.listdir(operate_dir):
        
        if item.lower().endswith('mp4'):
            try:
                # print(item)
                pass          

            except Exception as err:
                print(err)

    write_data_file(apps)


if __name__ == '__main__':
    update_path()