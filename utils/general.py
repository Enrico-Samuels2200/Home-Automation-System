import re
import os
import json
from utils import speak

# Finds file name and pass value into it encode as JSON format
def write_json(file_name='', value=''):
    with open(file_name, 'w') as doc:
        json.dump(value, doc)

# Reads data in JSON format and return data
def read_json(file_name=''):
    try:
        with open(file_name, 'r') as doc:
            return json.load(doc)
    
    except Exception as err:
        write_json(file_name, {})

# Attempts to read json file, if the file exist it returns True else it'll return False
def check_json(file_name=''):
    try:
        with open(file_name, 'r') as doc:
            return True
    
    except Exception as err:
        return False

# Uses regex to find specific word and return it
def find(word='', command=''):
    if word != '':
        found = re.compile(word).findall(command)
        if found:
            return found

# Looks for command in dictionary passed in through parameters
def find_in(data, string):
    for i in data.keys():
        key_found = re.compile(i).findall(string)
        
        if key_found:
            return key_found[0]

def talk(text=''):
    speak.main(text)

def run_command(data={}, command=''):
    for i in data.keys():
        try:
            dict_key = re.findall(i, command)
            
            if dict_key:
                speak.main(data[dict_key[0]](command))
        
        except Exception as err:
            print(err)
            continue

def run_speech_feedback_command(data={}, command=''):
    for i in data.keys():
        try:
            dict_key = re.findall(i, command)
            
            if dict_key:
                talk(data[dict_key[0]](command))

        except Exception as err:
            data[dict_key[0]]()
            continue

# Method is used to map out a directory and return a dictionary containing
# a tree displaying parent and child directories. Currently the method can only display 1 parent
# and all sub directories 1 level deep per a directory found in path passed into parameters
def map_directory(path):
    for (root,dirs,files) in os.walk(path):
        paths = {}

        for name in dirs:
            dir_path = f"{root}\{name}"
            dirs_exist = check_dir(dir_path)
            dir_name = os.path.dirname(f"{root}\{name}").split("\\")[-1]
            paths[name] = {}

            # If there a are sub directories found it'll map them.
            if dirs:
                for i in dirs_exist:
                    sub_path = f"{root}\{name}\{i}"                
                    paths[name][i] = sub_path
             
        # If no other directories are found takes key value and replace empty dictionary with path to directory.
        for i in paths:
            if not paths[i]:
                paths[i] = f"{root}\{i}"

        # returns the path dictionary
        return paths

if __name__ == '__main__':
    # run_speech_feedback_command(data={"apps": list_apps.update_path}, command='apps')
    pass