import re
import json
import requests
import xmltodict
import psutil

from word2number import w2n
from python_vlc_http import HttpVLC

try:
   vlc_client = HttpVLC('http://localhost:8080', '', '1234')

   volume = int(vlc_client.volume())
except:
   print('[!] Media server not detected')


def start_server():
   try:
      vlc_client = HttpVLC('http://localhost:8080', '', '1234')
      return True
   except:
      return False

# Creates a json file the temporary stores the users volume when using mute function.
def save_state(value):
   with open('vlc.json', 'w') as doc:
      settings = {
         'volume': value
      }
      
      json.dump(settings, doc)

# Reads the json file and returns the values stored in it.
def read_state():
   with open('vlc.json', 'r') as doc:
      return json.load(doc)

# Mutes the video editor
def mute():
   current_volume = int(vlc_client.volume())
   
   if current_volume != 0:
      save_state(current_volume)
      vlc_client.set_volume(0)
   else:
      new_volume = read_state()['volume'] 
      vlc_client.set_volume(new_volume/256)

# Sets the volume, converts text into integer format and then returns the percentage
# vlc_client only accepts floats 0-1 to interact with volume.
def set_volume_percentage(value):
   percentage = w2n.word_to_num(value)/100
   vlc_client.set_volume(percentage)

def playlist_order(value):
   print("Look at that value ", value)
   if value == "next":
      requests.get('http://localhost:8080/requests/status.xml?command=pl_next', auth=('', '1234'))

   if value == "back":
      requests.get('http://localhost:8080/requests/status.xml?command=pl_previous', auth=('', '1234'))
   else:
      print("[!] Command does not exist")

def command(request=''):
   switcher = {
      'screen': vlc_client.toggle_fullscreen,
      'toggle': vlc_client.pause,
      'mute': mute,
      'volume': set_volume_percentage
   }
   return switcher.get(request, "Invalid command")

def main():
   pass

if __name__ == '__main__':
   main()