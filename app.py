#!/usr/bin/env python3

import argparse
import os
import re
import queue
import sounddevice as sd
import vosk
import sys
import ast
import date
import speak

command_list = {
    "start movie": r'"C:\Users\admin\Desktop\Media\Anime\Sonny Boy\EP.1.v0.720p.mp4"',
    "start media": 'vlc',
    "organize folder": r'C:\Users\admin\Desktop\Projects\Programming\Python Projects\Directory_Organizer\sortFile.py'
}

system_list = {
    "date": date.convert_date_to_text(),
    "time": time.convert_time_to_text(),
}

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
                    keyword = re.compile('system').findall(command)
                    print(command)

                    for i in command_list.keys():
                        try:
                            if command == i:
                                command_found = True
                                print(command_found)
                                os.startfile(command_list[i])
                                break
                            elif "open" in command:
                                os.system(command.replace("open", "start"))
                                
                            elif command == "system stop":
                                print("\n\n[!] System shutting down")
                                parser.exit(0)
                            else:
                                #print(f"not working\nData {raw_dat}")
                                pass
                        except Exception as err:
                            print(err)
                            continue

                    if keyword:
                        for i in system_list.keys():
                            try:
                                word = re.compile(i).findall(command)
                                if word:
                                    speak.main(system_list[word[0]])
                            except Exception as err:
                                print(err)
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
