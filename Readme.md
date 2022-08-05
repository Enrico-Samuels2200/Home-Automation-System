**Python Home Automation**

Description:
------------
This project is inetended to be a home assistant which doesn't require any internet connection reducing possibility of tracking and possible scrurity issue that comes with having a smart home. The aim was for it to be ran on a Raspberry PI, so it could control wireless devices and applications on the desktop device itself through voice commands.<br><br>

Note the application is aimed to be built for Raspberry PI, however has only been teseted on a Windows pc this far. 



Requirements:
-------------
PIP preferably latest version <a href='https://www.geeksforgeeks.org/how-to-install-pip-on-windows/#:~:text=Step%201%3A%20Download%20the%20get,where%20the%20above%20file%20exists.&text=Step%204%3A%20Now%20wait%20through%20the%20installation%20process.'>Instructions</a><br>
VoskAPI English Model <a href='https://alphacephei.com/vosk/models'>Link</a>



Setting Up:
-----------
1. Once pip is installed and the project directory is extracted, navigate into this directory via the CLI.
2. Enter the command 'pip install -r requirements.txt'.
3. Make sure to have a VoskAPI model downloaded and extracted into the project root directory the contents of the extracted file should be placed into a directory named 'model'.
4. To start the application simply enter the command 'app.py' or 'python app.py'.



Commands:
---------
There are current primary and secondary commands. Secondary commands require their primary command first be said.<br>

- Primary Command:
    Secondary command
<br>
  List of commands:
  -----------------
  - Open: The command followed by the application name will open that application. Make sure the command 'update apps' was ran at least once.

  - Update:
      1. files: If paths are set for 'sortFile.py', this command will organize all the files in the directory specified to be placed in separate sub-directories.
      2. apps: If paths are set for 'list_apps.py', this command get all the shortcuts on the desktop and add them to a JSON file.

  - Start media: Will open VLC media player if installed on pc.
  - Organize folder: Will organize all the files by their extention into directory specified for their types example 'images', 'videos', and 'documents'.

  - Switch: VLC, pause or play the media player.
  - Change: VLC, pause or play the media player.
  - Screen: VLC, change from full screen view to windowed mode and vice versa.
  - Mute: VLC, self explanatory.
  - Slient: VLC, does the exact same thing as mute.
  - Silence: VLC, does the exact same thing as mute.
  - Volume: VLC, this command followed by a value 10 - 100, will change the volume to that percentage.
  - Sound: VLC, this command followed by a value 10 - 100, will change the volume to that percentage.
  - Audio: VLC, this command followed by a value 10 - 100, will change the volume to that percentage.
  - Next: VLC, this skips to the next media file if in a playlist.
  - Back: VLC, this goes to the previous media file if in a playlist.


  - System:
      1. date: Application will speak the current date.
      2. time: Application will speak the current time.
      3. update link: Will check if JSON file exist for the 'sortFile.py' script to function properly, if not one will be created.
      4. shutdown: Will break the loop and end the application
