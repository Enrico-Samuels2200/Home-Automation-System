import os
import json
import shutil
from utils import general

app_json_file = 'app_list.json'

apps = {}
app_list = {}
remove_list = ['- shortcut.lnk', '.lnk']


def update_path():
    operate_dir = r'C:\Users\admin\Desktop'
    status = ''

    for item in os.listdir(operate_dir):
            if item.lower().endswith('lnk'):
                try:
                    path = f'{operate_dir}\\{item}'

                    for i in remove_list:
                        if remove_list[0] in item.lower():
                            apps[item.lower().removesuffix(remove_list[0])] = path
                        else:
                            apps[item.lower().removesuffix(remove_list[1])] = path                
                    general.write_json(app_json_file, apps)
                    status = 'Paths has been updated'

                except Exception as err:
                    status = 'An error occured'
    
    general.talk(status)

def update_playlist():
    operate_dir = r'C:\Users\admin\Desktop\Media'
    for item in os.listdir(operate_dir):
        
        if item.lower().endswith('mp4'):
            try:
                print(item)

            except Exception as err:
                print(err)

def read_data_file():
    data = general.read_json('app_list.json')
    return data

if __name__ == '__main__':
    update_path()
    pass