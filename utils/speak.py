import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices') 
rate = engine.getProperty('rate')   # getting details of current speaking rate
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)

def main(value='', rate=180, volume=1.0):
    engine.setProperty('rate', rate)     # setting up new voice rate
    engine.setProperty('volume', volume)
    
    engine.setProperty('voice', voices[1].id)  
    engine.say(value)

    engine.runAndWait()

if __name__ == '__main__':
    main('')