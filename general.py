import re
import json
import speak

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
        return re.compile(word).findall(command)

# Looks for command in dictionary passed in through parameters
def find_in(data, string):
    for i in data.keys():
        key_found = re.compile(i).findall(string)
        
        if key_found:
            return key_found[0]

def run_command(data={}, command=''):
    for i in data.keys():
        try:
            dict_key = re.findall(i, command)
            
            if dict_key:
                data[dict_key[0]]
        
        except Exception as err:
            print(err)
            continue

def run_speech_feedback_command(data={}, command=''):
    for i in data.keys():
        try:
            dict_key = re.findall(i, command)
            
            if dict_key:
                speak.main(data[dict_key[0]](command))
        except Exception as err:
            data[dict_key[0]]()
            continue

if __name__ == '__main__':
    pass