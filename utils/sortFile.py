import os
import shutil
from utils import general

base_dir = os.path.dirname(os.path.abspath(__file__))
json_file_name = 'path.json'

folder_types = [
    'Images',
    'Videos',
    'Audio',
    'Documents',
    'Applications',
    'Compressed',
    'Other'
]

item_types = {
    'jpg':'Images',
    'jpeg':'Images',
    'png':'Images',
    'gif':'Images',
    'svg':'Images',
    'avi':'Videos',
    'mp4':'Videos',
    'mkv':'Videos',
    'wav':'Audio',
    'oog':'Audio',
    'mp3':'Audio',
    'csv':'Documents',
    'pdf':'Documents',
    'doc':'Documents',
    'txt':'Documents',
    'docx':'Documents',
    'rtf':'Documents',
    'exe':'Applications',
    'msi':'Applications',
    'apk':'Applications',
    'xapk':'Applications',
    '7z':'Compressed',
    'zip':'Compressed',
    'rar':'Compressed'
}

#   Check if data file exist. If does then read file for data(path)
#   If Path doesn't exist create path
#   Scan path for file types
#   Add file types to directories associated with file type

def read_data_file():
    with open('data.pydata', 'r') as doc:
        data = doc.readline()
        return data

def folder_location():
    # If has location is false user is asked to add a location.
    path = str(input('[*] Enter the location to the file: '))
    valid = os.path.exists(path)

    if valid:
        with open(f'{base_dir}/data.pydata', 'w') as doc:
            doc.write(path)
        verify_data_file()
    else:
        print('[!!] File location doesn\'t exist.')

#   Copies files if file type matches that in dictionary item_types.
def copy_file(current_dir, destination_dir):
    file_moved = False

    for item in os.listdir(current_dir):
            for file_type in item_types:
                if item.lower().endswith(file_type.lower()):
                    try:
                        selected_file = f'{current_dir}\\{item}'
                        destination = f'{destination_dir}\\{item_types[file_type]}\\'

                        shutil.move(selected_file, destination)
                        file_moved = True

                    except Exception as err:
                        print(err)
    return file_moved

def create_directory(path):
    folders = os.listdir(path)

    for name in folder_types:
        if name not in folders:
            print('yo')
            os.mkdir(f"{path}\\{name}")
            

#   If data file exist then read path and check if path is valid.
def verify_data_file():
    try:
        path = read_data_file()
        validate = os.path.exists(path)
        print(validate)

        if validate:
            # create_folders(path)
            copy_file()
            print('[*] Task Completed')
        else:
            folder_location()

    except Exception as err:
        print(err)

def manage_json_file(*args):
    data_file_exist = general.check_json(json_file_name)
    
    if data_file_exist:
        json_file = general.read_json(json_file_name)
        
        if len(json_file) >  0:
            path_key = input('Enter folder name: ').lower()
            path = input('Enter full path to a folder you wish to add: ')

            json_file[path_key] = path
            general.write_json(json_file_name, json_file)
    
        else:
            default_path = input('Enter full path to a folder you wish to store files in: ')
            general.write_json(json_file_name, {'default': default_path})    

# Method is used to get path data from json file
def manage(item_key=''):
    try:
        # Checks if a json file already exists
        data_file_exist = general.check_json(json_file_name)

        if data_file_exist:
            # Reads json file and return default path where files are saved 
            json_data = general.read_json(json_file_name)
            default = json_data['default'] if 'default' in json_data else manage_json_file()

            # Tries to create category files, if they already exist bypass
            try:
                create_directory(json_data['default'])
                
                if item_key in json_data:
                    file_moved = copy_file(json_data[item_key], json_data['default'])

                    if file_moved:
                        return 'Files successfully moved'
                    else:
                        return 'No new files were moved'
            except:
                pass

        # Create Json file if it doesn't exist
        else:
            manage_json_file()

    except Exception as err:
        print(err)

def activate(item_key):
    path_data = general.read_json(json_file_name)
    key_found = general.find_in(path_data, item_key)

    if key_found:
        feedback = manage(key_found)
        return feedback

if __name__ == '__main__':
    # verify_data_file()
    # manage('downloads')
    # manage_json_file()
    pass