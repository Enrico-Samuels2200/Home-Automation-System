#!/usr/bin/env python3

import argparse
import os
import re
import queue
import sounddevice as sd
import vosk
import sys
import ast
import psutil
import requests
import importlib
import time

import date 
import use_vlc
import speak
import list_apps
import sortFile
import general

json_data_files = {
    'paths': 'path.json'
}

shutdown_command = [
    'system shutdown',
    'system shut down'
]

update_list = {
    'files': sortFile.activate,
    'apps': list_apps.update_path
}

command_list = {
    'start sonny boy': r'C:\Users\admin\Desktop\Media\Playlist\Sonny Boy.xspf',
    'start media': 'vlc',
    'organize folder': r'sortFile.py'
}

media_command_list = {
    'switch': 'toggle',
    'change': 'toggle',
    'screen': 'screen',
    'mute': 'mute',
    'silent': 'mute',
    'silence': 'mute',
    'volume': 'volume',
    'sound': 'volume',
    'audio': 'volume',
    'next': 'next',
    'back': 'back'
}

system_list = {
    'date': date.convert_date_to_text,
    'time': date.convert_time_to_text,
    'update link': sortFile.manage_json_file
}

# Checks if application is running
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            
            while True:
                data = q.get()

                if rec.AcceptWaveform(data):
                    raw_data = rec.Result()
                    command = ast.literal_eval(raw_data)['text']
                    system = general.find('system', command)
                    update = general.find('update', command)
                    media_status = "vlc.exe" in (p.name() for p in psutil.process_iter())


                    print(f'[*] Command: {command}')

                    for i in command_list.keys():
                        try:
                            if command == i:
                                command_found = True
                                print(command_found)
                                os.startfile(command_list[i])
                                break
                            elif "open" in command:
                                apps = list_apps.read_data_file()

                                for key in apps:
                                    word = re.compile(key).findall(command)
                                         
                                    if word:
                                        os.startfile(apps[word[0]])
                                        break
                                break

                            elif command == shutdown_command[0] or command == shutdown_command[1]:
                                print("\n\n[!] System shutting down")
                                parser.exit(0)
                            else:
                                #print(f"not working\nData {raw_dat}")
                                pass
                        except Exception as err:
                            print(err)
                            continue

                    # Controls for System commands/commands relate to application or other features
                    if system:
                        general.run_speech_feedback_command(system_list, command)
                    
                    if update:
                        general.run_speech_feedback_command(update_list, command)

                    # Controls for VLC Media player
                    if media_status:
                        importlib.reload(use_vlc)

                        for i in media_command_list.keys():
                            try:
                                word = re.compile(i).findall(command)
                                if word:
                                    if word[0] == 'volume' or word[0] == 'sound' or word[0] == 'audio':
                                        use_vlc.set_volume_percentage(command)
                                    elif word[0] == 'back' or word[0] == 'next':
                                        a = use_vlc.playlist_order(media_command_list[word[0]])
                                        requests.get(a)
                                    else:
                                        use_vlc.command(media_command_list[word[0]])()
                                
                            except Exception as err:
                                print(use_vlc.start_server())
                                continue
                else:
                    raw_data = rec.PartialResult()
                    print(raw_data)
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    print(l)
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
